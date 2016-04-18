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

class Reg(Enum):
    ctrl = 0x00
    rst = 0x04
    n0d1 = 0x10
    n0d2 = 0x14
    n1d1 = 0x20
    n1d2 = 0x24
    req = 0xff

class CMWorker(QThread):
    connStateChanged = pyqtSignal(bool)
    boardsChanged = pyqtSignal(list)
    regReadData = pyqtSignal(int, int, int)
    adcData = pyqtSignal(list)
    streamAdcData = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.ser = serial.Serial(baudrate=1000000, timeout=1)
        self.ser = Device(lazy_open=True) # chunk size = 4 since register reads are 4 byte reads
        self.streamEn = False
        self.streamChunkSize = 10

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

# ser.read returns prematurely with less data than expected (even before timeout)
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
        self._regWr(Reg.req, 0x0001 | (N-1)<<16) # request N samples from both NMs
        # self.ser.flush_input()
        # self.ser.setTimeout(5+(N)/1000)
        t = QElapsedTimer()
        t.start()
        data = self.ser.read(128*N, timeout=5+(N)/1000) # read all channels - 2 NMs * 64 channels per NM * 2 bytes per channel
        print("elapsed time: {}".format(t.elapsed()))
        if len(data) != 128*N:
            raise Exception("Failed to read from ADC: returned {}/{} bytes. Missing: {} bytes ({} samples).".format(len(data), 128*N, 128*N-len(data), (128*N-len(data))/128))
        for ct in range(0,N):
            out.append([(data[i+1] << 8 | data[i]) & 0x7FFF for i in range(ct*128,(ct+1)*128,2)])
        # self.ser.setTimeout(1)
        return out

    # setter for self.streamEn. Needed so that we can set it to false and break out of loop inside streamAdc()
    @pyqtSlot(bool)
    def setStreamBool(self, streamEn):
        self.streamEn = streamEn
        print("cmbackend.streamEn = {}".format(self.streamEn)) #true

    @pyqtSlot(bool)
    def streamAdc(self):
        if not self.ser._opened:
            return
        t = QElapsedTimer()
        self._regWr(Reg.req, 0x0010 | (self.streamChunkSize)<<16) # put CM into streaming mode for NM0 only
        # self._regWr(Reg.req, 0x0020 | (self.streamChunkSize)<<16) # put CM into streaming mode for NM1 only
        # self._regWr(Reg.req, 0x0030 | (self.streamChunkSize)<<16) # put CM into streaming mode for both NMs
        while self.streamEn:
            out = []
            t.start()
            data = self.ser.read(128*self.streamChunkSize, timeout=None)
            for ct in range(0, self.streamChunkSize):
                out.append([(data[i+1] << 8 | data[i]) & 0x7FFF for i in range(ct*128,(ct+1)*128,2)])
            self.streamAdcData.emit(out)
            # if len(data):
            #     print("elapsed time: {}".format(t.elapsed()))
            # print("cmbackend.DataVis.streamEn = {}".format(DataVisualizer.DataVisualizer.streamEn)) #false
            # print("cmbackend.streamEn = {}".format(self.streamEn)) #true
            if not self.streamEn:
                self._regWr(Reg.req, 0x0000) # turn off streaming mode
                print("stopped")
                break

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
