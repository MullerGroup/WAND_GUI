from PyQt4.QtCore import *
from ok import FrontPanel
from bitarray import *
import struct
import time
# from binascii import hexlify

def check(err):
    if err != FrontPanel.NoError:
        raise Exception("opal kelly error {}".format(err))

class NMICWorker(QThread):
    connStateChanged = pyqtSignal(bool)
    boardsChanged = pyqtSignal(list)
    regReadData = pyqtSignal(int, int)
    adcData = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.fp = FrontPanel()
        self.isOpen = False

    def __del__(self):
        # wait for the thread to finish before destroying object
        self.wait()

    @staticmethod
    def _crc5(data: bitarray):
        # equivalent to initializing verifier with all-1s
        cc = 0b01100
        for b in data:
            x = (1 if b else 0) ^ (1 if cc & 0b10000 else 0)
            cc <<= 1
            cc &= 0b11111
            cc ^= x | (x << 2)
        b = bitarray()
        b.frombytes(bytes([cc]))
        return b[3:8]

    def _resetIF(self):
        # send a reset to the chip to initialize serial i/f
        check(self.fp.ActivateTriggerIn(0x40, 5))

    def _resetLogic(self):
        # i2c prescale
        check(self.fp.SetWireInValue(0x00, 10, 0xFFFF))
        # enable i2c core
        check(self.fp.SetWireInValue(0x01, 0xC000, 0xFF00))
        # set real input
        self.fp.SetWireInValue(0x02, 0x2000, 0xFFFF)
        self.fp.UpdateWireIns()
        # reset i2c and chip interfaces
        check(self.fp.ActivateTriggerIn(0x40, 6))
        check(self.fp.ActivateTriggerIn(0x40, 7))
        # reset chip serial
        self._resetIF()

    def _i2cByte(self, val, start=False, stop=False):
        # write data byte
        check(self.fp.SetWireInValue(0x01, val, 0x00FF))
        self.fp.UpdateWireIns()
        # 3:0 = START, STOP, READ, WRITE
        START, STOP, READ, WRITE = range(3,-1,-1)
        if start:
            check(self.fp.ActivateTriggerIn(0x40, START))
        check(self.fp.ActivateTriggerIn(0x40, WRITE))
        if stop:
            check(self.fp.ActivateTriggerIn(0x40, STOP))
        timeout = 0
        while True:
            self.fp.UpdateTriggerOuts()
            if self.fp.IsTriggered(0x60, 0x03):
                break
            timeout += 1
            if timeout > 100:
                self.fp.UpdateWireOuts()
                print("status: {:04x}".format(self.fp.GetWireOutValue(0x20)))
                raise Exception("i2c timeout")

    def _setLVPot(self, pot, value):
        #print(value)
        value &= 0x3FF
        pot &= 1
        self._i2cByte(val=0x50, start=True)
        self._i2cByte(val=value >> 8 | pot << 4)
        self._i2cByte(val = value & 0xFF, stop=True)

    def _setHVPot(self, value):
        #print(value)
        value &= 0x3FF
        self._i2cByte(val=0x5C, start=True)
        self._i2cByte(val=value >> 8)
        self._i2cByte(val=value & 0xFF, stop=True)

    def _setPwrEn(self, en1v, en3v):
        val = 0
        if en3v:
            val |= 0x8000
        if en1v:
            val |= 0x4000
        check(self.fp.SetWireInValue(0x02, val, 0xC000))
        self.fp.UpdateWireIns()

    def _chipTx(self, bits: bitarray):
        #print(bits)
        l = len(bits)
        b = bits.copy()
        # extend bitarray to 64 bits
        b.extend(bitarray(64-l))
        self.fp.SetWireInValue(0x06, struct.unpack(">H", b[0:16].tobytes())[0], 0xFFFF)
        self.fp.SetWireInValue(0x05, struct.unpack(">H", b[16:32].tobytes())[0], 0xFFFF)
        self.fp.SetWireInValue(0x04, struct.unpack(">H", b[32:48].tobytes())[0], 0xFFFF)
        self.fp.SetWireInValue(0x03, struct.unpack(">H", b[48:64].tobytes())[0], 0xFFFF)
        self.fp.SetWireInValue(0x02, l, 0x003F)
        self.fp.UpdateWireIns()
        self.fp.ActivateTriggerIn(0x40, 4)
        timeout = 0
        while True:
            timeout += 1
            self.fp.UpdateTriggerOuts()
            if self.fp.IsTriggered(0x60, 0x04):
                break
            if timeout > 10:
                raise Exception("timed out waiting for tx to finish")

    def _sendCmd(self, cmd):
        bits = bitarray()
        bits.frombytes(struct.pack(">H", 0x8000 | (cmd & 0x3FF) << 5))
        bits[11:16] = NMICWorker._crc5(bits[0:11])
        self._chipTx(bits)

    def _regOp(self, addr, data, write):
        bits = bitarray(2)
        bits[0] = False
        bits[1] = write
        bits.frombytes(struct.pack(">HH", addr, data))
        bits.extend(self._crc5(bits))
        self._chipTx(bits)
        if not write:
            return self._getReg()

    def _getReg(self):
        buf = bytearray(6)
        r = self.fp.ReadFromBlockPipeOut(0xa0, 6, buf)
        if r != 6:
            raise Exception("failed to read from ok pipe: {}".format(r))
        ba = bitarray()
        ba.frombytes(bytes(buf))
        #print(ba[0:2])
        #print(hexlify(ba[2:18].tobytes()))
        #print(hexlify(ba[18:34].tobytes()))
        return struct.unpack(">H", ba[18:34].tobytes())[0]

    @staticmethod
    def _unpackAdc(data: bitarray):
        # header = data[0:2]
        data = data[2:1024+2]
        return [struct.unpack(">H", data[i*16:(i+1)*16].tobytes())[0] & 0x7FFF for i in range(0,64)]

    def _getAdc(self, N):
        blkSize = 130
        buf = bytearray(blkSize*N)
        self.fp.SetTimeout(N*4)
        r = self.fp.ReadFromBlockPipeOut(0xA1, blkSize, buf)
        self.fp.SetTimeout(100)
        if r != blkSize*N:
            raise Exception("error reading from adc pipe: {}".format(r))
        out = []
        for i in range(0, N):
            bb = bitarray()
            bb.frombytes(bytes(buf[blkSize*i:blkSize*(i+1)]))
            out.append(self._unpackAdc(bb))
        return out

    @pyqtSlot(int)
    def readAdc(self, ns):
        if not self.isOpen:
            return
        self._getAdc(253)
        self.adcData.emit(self._getAdc(ns))

    @pyqtSlot()
    def refreshBoards(self):
        ct = self.fp.GetDeviceCount()
        l = []
        for i in range(0, ct):
            l.append(self.fp.GetDeviceListSerial(i))
        self.boardsChanged.emit(l)

    @pyqtSlot(str)
    def connectToBoard(self, board):
        err = self.fp.OpenBySerial(board)
        self.fp.SetTimeout(100)
        err2 = err
        if err == FrontPanel.NoError:
            err2 = self.fp.ConfigureFPGA('fpga/testboard.bit')
            self._resetLogic()
        self.isOpen = (err == FrontPanel.NoError and err2 == FrontPanel.NoError)
        if not self.isOpen:
            print("failed to open board: {}".format(err))
        self.connStateChanged.emit(self.isOpen)

    @pyqtSlot()
    def resetSerial(self):
        if not self.isOpen:
            return
        self._resetIF()

    @pyqtSlot()
    def disconnectBoard(self):
        self.fp = FrontPanel()
        self.isOpen = False
        self.connStateChanged.emit(self.isOpen)

    @pyqtSlot(bool, bool)
    def setPwrEn(self, en1v, en3v):
        if not self.isOpen:
            return
        # print(en1v, en3v)
        self._setPwrEn(en1v, en3v)

    @pyqtSlot(int)
    def nmicCommand(self, cmd):
        if not self.isOpen:
            return
        if cmd == 0x04 or cmd == 0x09: # imp_start or stim start command
            # flush adc pipe
            try:
                self._getAdc(253)
                prev = self._getAdc(400)
            except Exception:
                pass
        self._sendCmd(cmd)
        if cmd == 0x04 or cmd == 0x09:
            self.adcData.emit(prev + self._getAdc(600))

    @pyqtSlot(float)
    def setPwr3V(self, voltage):
        if not self.isOpen:
            return
        # line parameters
        a = -342
        b = 1268
        setPt = round(a*voltage+b)
        if setPt < 0:
            setPt = 0
        elif setPt > 257:
            setPt = 257
        self._setLVPot(1, int(setPt))

    @pyqtSlot(float)
    def setPwr1V(self, voltage):
        if not self.isOpen:
            return
        # line parameters
        a = -401
        b = 622
        setPt = round(a*voltage+b)
        if setPt < 0:
            setPt = 0
        elif setPt > 257:
            setPt = 257
        self._setLVPot(0, int(setPt))

    @pyqtSlot(float)
    def setPwrHV(self, voltage):
        if not self.isOpen:
            return
        # 3rd order polynomial (wtf?)
        c3 = -9.619e-1
        c2 = 32.705
        c1 = -388.9
        c0 = 1615.9
        setPt = round(c3*voltage**3+c2*voltage**2+c1*voltage+c0)
        if setPt < 0:
            setPt = 0
        elif setPt > 257:
            setPt = 257
        self._setHVPot(setPt)

    @pyqtSlot(int, int)
    def writeReg(self, addr, value):
        if not self.isOpen:
            return
        self._regOp(addr, value, True)
        #print("Write register: {:04x} {:04x}".format(addr, value))
        self.regReadData.emit(addr, value)

    @pyqtSlot(int)
    def readReg(self, addr):
        if not self.isOpen:
            return
        ret = self._regOp(addr, 0, False)
        print("Read register: {:04x} {:04x}".format(addr, ret))
        self.regReadData.emit(addr, ret)
