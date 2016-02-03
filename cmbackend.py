from PyQt4.QtCore import *
import serial
import serial.tools.list_ports
from bitarray import *
import struct
import time
from enum import Enum
# from binascii import hexlify

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
    regReadData = pyqtSignal(int, int)
    adcData = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ser = serial.Serial(baudrate=1250000, timeout=1.0)
        # self.ser = serial.Serial(baudrate=115200, timeout=1.0)
        #TODO: changed timeout to float instead of int for Mac, and changed baudrate to 115200 from 1250000

    def __del__(self):
        # wait for the thread to finish before destroying object
        self.wait()

    def _regWr(self, reg, value):
        s = struct.pack(">cI", bytes([reg.value]), value)
        #print("reg wr: {}".format(s))
        self.ser.write(s)
        self.ser.flushOutput()

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

                #TODO: figure out timeout issue on Mac/Windows -- for now, I probably need to change function call

    def _regOp(self, nm, addr, data, write):
        if nm==0:
            self._regWr(Reg.n0d1, 1 if write else 0)
            self._regWr(Reg.n0d2, addr << 16 | data)
            self._regWr(Reg.ctrl, 0x1000)
            if not write:
                #self.ser.timeout(3.0)
                #self.ser.setTimeout(3)
                self._regWr(Reg.req, 0x0100)
                d = self.ser.read(4)
                #self.ser.timeout(1.0)
                #self.ser.setTimeout(1)
                if len(d) != 4 or (d[1] << 8 | d[0]) != addr:
                    raise Exception("Reg read failed: {}/4 bytes, {}".format(len(d), d))
                return d[3] << 8 | d[2]

        if nm==1:
            self._regWr(Reg.n1d1, 1 if write else 0)
            self._regWr(Reg.n1d2, addr << 16 | data)
            self._regWr(Reg.ctrl, 0x2000)
            if not write:
                #self.ser.timeout(3.0)
                #self.ser.setTimeout(3)
                self._regWr(Reg.req, 0x0200)
                d = self.ser.read(4)
                #self.ser.timeout(1.0)
                #self.ser.setTimeout(1)
                if len(d) != 4 or (d[1] << 8 | d[0]) != addr:
                    raise Exception("Reg read failed: {}/4 bytes, {}".format(len(d), d))
                return d[3] << 8 | d[2]


    def _getAdc(self, nm, N):
        if nm==0:
            out = []
            self._regWr(Reg.req, 0x0001 | (N-1)<<16)
            self.ser.flushInput()
            #self.ser.timeout(5.0+N/1000)
            #self.ser.setTimeout(5+N/1000)
            data = self.ser.read(128*N)
            if len(data) != 128*N:
                raise Exception("Failed to read from ADC: returned {}/{} bytes".format(len(data), 128*N))
            for ct in range(0,N):
                out.append([(data[i+1] << 8 | data[i]) & 0x7FFF for i in range(ct*128,(ct+1)*128,2)])
            #self.ser.timeout(1.0)
            #self.ser.setTimeout(1)
            return out

        if nm==1:
            out = []
            self._regWr(Reg.req, 0x0002 | (N-1)<<16)
            self.ser.flushInput()
            #self.ser.timeout(5.0+N/1000)
            #self.ser.setTimeout(5+N/1000)
            data = self.ser.read(128*N)
            if len(data) != 128*N:
                raise Exception("Failed to read from ADC: returned {}/{} bytes".format(len(data), 128*N))
            for ct in range(0,N):
                out.append([(data[i+1] << 8 | data[i]) & 0x7FFF for i in range(ct*128,(ct+1)*128,2)])
            #self.ser.timeout(1.0)
            #self.ser.setTimeout(1)
            return out

    @pyqtSlot(int, int)
    def readAdc(self, nm, ns):
        if not self.ser.isOpen():
            return
        self.adcData.emit(self._getAdc(nm, ns))

    @pyqtSlot()
    def refreshBoards(self):
        ports = serial.tools.list_ports.comports()
        l = [i[0] for i in ports]
        self.boardsChanged.emit(l)

    @pyqtSlot(str)
    def connectToBoard(self, board):
        self.ser.port = board
        self.ser.open()
        self.connStateChanged.emit(self.ser.isOpen())

    @pyqtSlot()
    def resetSerial(self):
        if not self.ser.isOpen():
            return
        self._resetIF()

    @pyqtSlot()
    def disconnectBoard(self):
        self.ser.close()
        self.connStateChanged.emit(self.ser.isOpen())

    @pyqtSlot(bool, bool)
    def setPwrEn(self, en1v, en3v):
        pass

    @pyqtSlot(int, int)
    def nmicCommand(self, nm, cmd):
        if not self.ser.isOpen():
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
            self.adcData.emit(self._getAdc(nm, 1000))

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
        if not self.ser.isOpen():
            return
        self._regOp(nm, addr, value, True)
        #print("Write register: {:04x} {:04x}".format(addr, value))
        self.regReadData.emit(addr, value)

    @pyqtSlot(int, int)
    def readReg(self, nm, addr):
        if not self.ser.isOpen():
            return
        ret = self._regOp(nm, addr, 0, False)
        print("Read register: {:04x} {:04x}".format(addr, ret))
        self.regReadData.emit(addr, ret)
