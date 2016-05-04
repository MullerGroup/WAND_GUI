from PyQt4.QtCore import *
import serial
import serial.tools.list_ports # _osx ?
from bitarray import *
import struct
import time
from enum import Enum
# from binascii import hexlify
from pylibftdi import Driver, Device
import ui.ui_DataVisualizer as ui_DataVisualizer
import DataVisualizer
import datetime

class Reg(Enum):
    ctrl = 0x00
    rst = 0x04
    n0d1 = 0x10
    n0d2 = 0x14
    n1d1 = 0x20
    n1d2 = 0x24
    req = 0xff

class streamAdcThread(QThread):

    # streamAdcData = pyqtSignal(list)
    streamChunkSize = 1
    plotChunkSize = 100
    read_count = 0

    def __init__(self):
        QThread.__init__(self)
        # print("turned ON streaming mode")
        self._running = True

    def __del__(self):
        # if CMWorker.ser._opened:
            # CMWorker()._regWr(Reg.req, 0x0000) # turn off streaming mode
        # print("turned OFF streaming mode")
        self.wait()

    def stop(self):
        # self.terminate()
        self._running = False

    def run(self):
        # make sure serial device is open
        if not CMWorker.ser._opened:
            return

        # reset
        if not self._running:
            CMWorker.ser.flush()
            self._running = True

        start = datetime.datetime.now()
        CMWorker()._regWr(Reg.req, 0x0010 | self.streamChunkSize<<16) # put CM into streaming mode for NM0 only
        # CMWorker()._regWr(Reg.req, 0x0020 | self.streamChunkSize<<16) # put CM into streaming mode for NM1 only
        # CMWorker()._regWr(Reg.req, 0x0030 | self.streamChunkSize<<16) # put CM into streaming mode for both NMs

        avg_time_fail = 0
        num_fail = 0
        out = []
        self.read_count = 0
        while self._running:
            # out = []
            # t.start()
            print((datetime.datetime.now()-start).microseconds)
            start = datetime.datetime.now()
            data = CMWorker.ser.read(128*self.streamChunkSize, timeout=None)
            # data = CMWorker.ser.read(256*self.streamChunkSize, timeout=None)
            # print("elapsed time: {}".format(t.elapsed()))
            self.read_count += len(data)
            for ct in range(0, self.streamChunkSize):
                # out.append([(data[i+1] << 8 | data[i]) & 0x7FFF for i in range(ct*128,(ct+1)*128,2)])
                # out.append([(data[i+1] << 8 | data[i]) & 0x7FFF for i in range(ct*256,(ct+1)*256,2)])
                out.append([data[i] for i in range(ct*128,(ct+1)*128)])
            # print(out)
            # print(data)
            if data[len(data)-64:len(data)]!=bytes(64):
                # failed
                # now = datetime.datetime.now()
                # elapsed = (now-start).microseconds/1000000 + (now-start).seconds
                # print("time elapsed {} s".format(elapsed))
                # avg_time_fail = (avg_time_fail*num_fail + elapsed) / (num_fail+1)
                # num_fail += 1
                # print("avg time to drop byte(s) = {} s".format(avg_time_fail))
                # print(data[64:len(data)])
                print(out[len(out)-1][64:128])
                print("read count: {} bytes, {} samples".format(self.read_count, self.read_count/128))
                self.read_count = 0
                start = datetime.datetime.now()
                print("missed byte(s) around byte {} (sample {})".format(self.read_count,self.read_count/128))
                self._running = False
                break
                CMWorker.ser.flush()
            if len(out)>=self.plotChunkSize:
                self.emit(SIGNAL('streamDataOut(PyQt_PyObject)'), out)
                # self.read_count += len(out)
                # print(out)
                out = []
                # print("request count = {}, read_count = {}".format(self.req_count/128, self.read_count))
            # if len(data):
            #     print("len(data): {}, elapsed time: {}".format(len(data), t.elapsed()))
            # previous = data[0]

        # only get here if we've called stop(), so turn off streaming mode
        CMWorker()._regWr(Reg.req, 0x0000) # turn off streaming mode


class CMWorker(QThread):
    connStateChanged = pyqtSignal(bool)
    boardsChanged = pyqtSignal(list)
    regReadData = pyqtSignal(int, int, int)
    adcData = pyqtSignal(list)

    ser = Device(lazy_open=True)

    def __init__(self, parent=None):
        super().__init__(parent)

    def __del__(self):
        # wait for the thread to finish before destroying object
        self.wait()

    def _regWr(self, reg, value):
        s = struct.pack(">cI", bytes([reg.value]), value)
        print("reg wr: {}".format(s))
        # print("reg wr: {:04x} {:04x}".format(reg.value, value))
        self.ser.write(s)
        # self.ser.flushOutput()

    def _resetIF(self):
        # reset AM
        self._regWr(Reg.ctrl, 0x103)
        # reset all NMs
        self._regWr(Reg.rst, 0xFFFF)
        self._regWr(Reg.ctrl, 0x102)

    def _sendCmd(self, nm, cmd):
        if nm==0:
            self._regWr(Reg.n0d2, 1<<10 | (cmd & 0x3FF))
            self._regWr(Reg.ctrl, 0x1010)
        if nm==1:
            self._regWr(Reg.n1d2, 1<<10 | (cmd & 0x3FF))
            self._regWr(Reg.ctrl, 0x2020)

    def _regOp(self, nm, addr, data, write):
        if nm==0:
            self._regWr(Reg.n0d1, 1 if write else 0)
            self._regWr(Reg.n0d2, addr << 16 | data)
            self._regWr(Reg.ctrl, 0x1000)
            if not write:
                # self.ser.setTimeout(3)
                self._regWr(Reg.req, 0x0100)
                d = self.ser.read(4, timeout=3)
                # self.ser.setTimeout(1)
                if len(d) != 4 or (d[1] << 8 | d[0]) != addr:
                    raise Exception("Reg read failed: {}/4 bytes, {}".format(len(d), d))
                return d[3] << 8 | d[2]

        if nm==1:
            self._regWr(Reg.n1d1, 1 if write else 0)
            self._regWr(Reg.n1d2, addr << 16 | data)
            self._regWr(Reg.ctrl, 0x2000)
            if not write:
                # self.ser.setTimeout(3)
                self._regWr(Reg.req, 0x0200)
                d = self.ser.read(4, timeout=3)
                # self.ser.setTimeout(1)
                if len(d) != 4 or (d[1] << 8 | d[0]) != addr:
                    raise Exception("Reg read failed: {}/4 bytes, {}".format(len(d), d))
                return d[3] << 8 | d[2]

    def _getAdc(self, N):
        # out = []
        # self._regWr(Reg.req, 0x0003 | (N-1)<<16) # request N samples from both NMs
        # # self.ser.flush_input()
        # # self.ser.setTimeout(5+(2*N)/1000)
        # # data = []
        # # while len(data) < 256*N:
        # #     print("bytes in data: {}, bytes requested: {}".format(len(data),256*N-len(data)))
        # #     data.append(self.ser.read(256*N-len(data), timeout=5+(2*N)/1000))
        # # data = []
        # # if len(data) < 256*N:
        # #     data.append(self.ser)
        # # data = self.ser.read(256*N)
        # # while len(data) < 256*N:
        # #     print(len(data))
        # # data.append(temp)
        # # data = b''.append(temp)
        # # data = self.ser.read(256*N, timeout=0)
        # t = QElapsedTimer()
        # t.start()
        # data = self.ser.read(256*N, timeout=5+(2*N)/1000) # read all channels - 2 NMs * 64 channels per NM * 2 bytes per channel
        # print("elapsed time: {}".format(t.elapsed()))
        # if len(data) != 256*N:
        #     raise Exception("Failed to read from ADC: returned {}/{} bytes".format(len(data), 256*N))
        # for ct in range(0,N):
        #     out.append([(data[i+1] << 8 | data[i]) & 0x7FFF for i in range(ct*256,(ct+1)*256,2)])
        # # self.ser.setTimeout(1)
        # return out

        out = []
        # self._regWr(Reg.req, 0x0010 | N<<16)
        self._regWr(Reg.req, 0x0001 | (N-1)<<16) # request N samples from both NMs
        # t = QElapsedTimer()
        # t.start()
        data = self.ser.read(128*N, timeout=5+(N)/1000) # read all channels - 2 NMs * 64 channels per NM * 2 bytes per channel
        # print("elapsed time: {}".format(t.elapsed()))
        if len(data) != 128*N:
            print(data)
            self.flushDataFifo() # assume we missed sample(s), and flush FIFO on FTDI
            raise Exception("Failed to read from ADC: returned {}/{} bytes. Missing: {} bytes ({} samples).".format(len(data), 128*N, 128*N-len(data), (128*N-len(data))/128))
        # print(data)
        for ct in range(0,N):
            # out.append([(data[i+1] << 8 | data[i]) & 0x7FFF for i in range(ct*128,(ct+1)*128,2)])
            out.append([data[i] for i in range(ct*128,(ct+1)*128)])
        # print(out)
        return out

    @pyqtSlot(int)
    def readAdc(self, ns):
        if not self.ser._opened:
            return
        self.adcData.emit(self._getAdc(ns))

    @pyqtSlot()
    def refreshBoards(self):
        dev_list = []
        for device in Driver().list_devices():
            vendor, product, serial = map(lambda x: x.decode('latin1'), device)
            dev_list.append(serial)
        # ports = serial.tools.list_ports.comports()
        # l = [i[0] for i in dev_list]
        self.boardsChanged.emit(dev_list)
        # print(self.ser._opened)


    @pyqtSlot(str)
    def connectToBoard(self, board):
        self.ser.open()
        self.ser.flush()
        print("Connected to FTDI and flushed FIFOs")
        # self.ser.port = board
        # self.ser.open()
        self.connStateChanged.emit(self.ser._opened)
        # print(self.ser._opened)

# flush_input() flushes FTDI Rx buffer (commands)
# flush_output() flushes FTDI Tx buffer (data from CM)

    @pyqtSlot()
    def flushCommandFifo(self):
        if not self.ser._opened:
            return
        self.ser.flush_input()
        print("Flushed FTDI input (command) FIFO")

    @pyqtSlot()
    def flushDataFifo(self):
        if not self.ser._opened:
            return
        self.ser.flush_output()
        print("Flushed FTDI output (data) FIFO")

    @pyqtSlot()
    def resetSerial(self):
        if not self.ser._opened:
            return
        self._resetIF()

    @pyqtSlot()
    def disconnectBoard(self):
        self.ser.close()
        self.connStateChanged.emit(self.ser._opened)
        # print(self.ser._opened)

    @pyqtSlot(bool, bool)
    def setPwrEn(self, en1v, en3v):
        pass

    @pyqtSlot(int, int)
    def nmicCommand(self, nm, cmd):
        if not self.ser._opened:
            return
        #if cmd == 0x04 or cmd == 0x09: # imp_start or stim start command
        #    # if recording is disabled, don't abort on timeout
        #    prev = None
        #    try:
        #        prev = self._getAdc(400)
        #    except Exception:
        #        pass
        self._sendCmd(nm, cmd)
        if (cmd == 0x04 or cmd == 0x09):
            self.adcData.emit(self._getAdc(1000))

    @pyqtSlot(float)
    def setPwr3V(self, voltage):
        pass

    @pyqtSlot(float)
    def setPwr1V(self, voltage):
        pass

    @pyqtSlot(float)
    def setPwrHV(self, voltage):
        pass

    @pyqtSlot(int, int, int)
    def writeReg(self, nm, addr, value):
        if not self.ser._opened:
            return
        self._regOp(nm, addr, value, True)
        #print("Write register: {:04x} {:04x}".format(addr, value))
        self.regReadData.emit(nm, addr, value)

    @pyqtSlot(int, int)
    def readReg(self, nm, addr):
        if not self.ser._opened:
            return
        ret = self._regOp(nm, addr, 0, False)
        print("Read register from NM {}: {:04x} {:04x}".format(nm, addr, ret))
        self.regReadData.emit(nm, addr, ret)
