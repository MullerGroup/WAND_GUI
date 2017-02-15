from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.ui_closedLoop import Ui_closedLoop
import datetime
from enum import Enum
import time


# CM register addresses
class Reg(Enum):
    ctrl = 0x00
    rst = 0x04
    n0d1 = 0x10
    n0d2 = 0x14
    n1d1 = 0x20
    n1d2 = 0x24
    req = 0xff
    cl1 = 0xDD
    cl2 = 0xEE
    cl3 = 0xCC
    cl4 = 0xBB
    cl5 = 0xAB
    cl6 = 0xCD

class ClosedLoop(QDockWidget):

    writeCL = pyqtSignal(Reg, int)
    writeCLCh = pyqtSignal(int,int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_closedLoop()
        self.ui.setupUi(self)
        self.setWindowTitle("Closed Loop Config")
        self.ui.freq1.valueChanged.connect(self.on_freq1_valueChanged)
        self.ui.freq2.valueChanged.connect(self.on_freq2_valueChanged)
        self.ui.freq3.valueChanged.connect(self.on_freq3_valueChanged)
        self.ui.freq4.valueChanged.connect(self.on_freq4_valueChanged)
        self.ui.randMin.valueChanged.connect(self.on_randMin_valueChanged)
        self.ui.randMax.valueChanged.connect(self.on_randMax_valueChanged)

    def setWorker(self, w):
        self.writeCL.connect(w.writeCL)
        self.writeCLCh.connect(w.writeCLCh)

    @pyqtSlot()
    def on_enable0_clicked(self):
        if self.ui.enable0.isChecked():
            self.ui.enable1.setDisabled(True)
            start = datetime.datetime.now()
            print("NM0 Closed Loop Enabled at: {}".format(start))
            self.closedLoopCmd()
        else:
            stop = datetime.datetime.now()
            print("NM0 Closed Loop Disabled at: {}".format(stop))
            self.ui.enable1.setEnabled(True)
            self.closedLoopOff()

    @pyqtSlot()
    def on_enable1_clicked(self):
        if self.ui.enable1.isChecked():
            self.ui.enable0.setDisabled(True)
            start = datetime.datetime.now()
            print("NM1 Closed Loop Enabled at: {}".format(start))
            self.closedLoopCmd()
        else:
            stop = datetime.datetime.now()
            print("NM1 Closed Loop Disabled at: {}".format(stop))
            self.ui.enable0.setEnabled(True)
            self.closedLoopOff()

    @pyqtSlot()
    def on_freq1_valueChanged(self):
        if self.ui.freq2.value() < self.ui.freq1.value():
            self.ui.freq2.setValue(self.ui.freq1.value())

    @pyqtSlot()
    def on_freq2_valueChanged(self):
        if self.ui.freq2.value() < self.ui.freq1.value():
            self.ui.freq1.setValue(self.ui.freq2.value())

    @pyqtSlot()
    def on_freq3_valueChanged(self):
        if self.ui.freq4.value() < self.ui.freq3.value():
            self.ui.freq4.setValue(self.ui.freq3.value())

    @pyqtSlot()
    def on_freq4_valueChanged(self):
        if self.ui.freq4.value() < self.ui.freq3.value():
            self.ui.freq3.setValue(self.ui.freq4.value())

    @pyqtSlot()
    def on_randMax_valueChanged(self):
        if self.ui.randMin.value() > self.ui.randMax.value():
            self.ui.randMin.setValue(self.ui.randMax.value())

    @pyqtSlot()
    def on_randMin_valueChanged(self):
        if self.ui.randMin.value() > self.ui.randMax.value():
            self.ui.randMax.setValue(self.ui.randMin.value())

    def createBitMask(self, bitShift, bitSpan):
        bitMask = 0
        for i in range(0, bitSpan):
            bitMask += 2**i
        bitMask = bitMask << bitShift
        return bitMask

    def makeBit(self, val, bitShift, bitSpan, lsb, minVal=0):
        bitMask = self.createBitMask(bitShift, bitSpan)
        decVal = int((val-minVal)/lsb)
        return (decVal << bitShift) & bitMask

    def closedLoopCmd(self):
        en1_a = int(self.ui.ch1Enable.currentIndex() != 0)
        en2_a = int(self.ui.ch1Enable2.currentIndex() != 0)
        ch_a = self.ui.ch1.value()
        dir1_a = int(self.ui.ch1Enable.currentIndex() == 1)
        thresh1_a = self.ui.threshold1.value()
        freq1_min = int((self.ui.freq1.value()/1000)*(2**(self.ui.nfft.currentIndex() + 4)))
        freq1_max = int((self.ui.freq2.value()/1000)*(2**(self.ui.nfft.currentIndex() + 4)))

        dir2_a = int(self.ui.ch1Enable2.currentIndex() == 1)
        thresh2_a = self.ui.threshold2.value()
        freq2_min = int((self.ui.freq3.value()/1000)*(2**(self.ui.nfft.currentIndex() + 4)))
        freq2_max = int((self.ui.freq4.value()/1000)*(2**(self.ui.nfft.currentIndex() + 4)))

        # en_b = int(self.ui.ch2Enable.currentIndex() != 0)
        # ch_b = self.ui.ch2.value()
        # dir_b = int(self.ui.ch2Enable.currentIndex() == 1)
        # thresh_b = self.ui.threshold2.value()

        # en_c = int(self.ui.ch3Enable.currentIndex() != 0)
        # ch_c = self.ui.ch3.value()
        # dir_c = int(self.ui.ch3Enable.currentIndex() == 1)
        # thresh_c = self.ui.threshold3.value()

        # en_d = int(self.ui.ch4Enable.currentIndex() != 0)
        # ch_d = self.ui.ch4.value()
        # dir_d = int(self.ui.ch4Enable.currentIndex() == 1)
        # thresh_d = self.ui.threshold4.value()

        dead_len = self.ui.deadLength.value()
        rand_mode = int(self.ui.randomMode.isChecked())
        CL1_off = int(not self.ui.enable1.isChecked())
        CL0_off = int(not self.ui.enable0.isChecked())
        CL1_on = int(self.ui.enable1.isChecked())
        CL0_on = int(self.ui.enable0.isChecked())
        chStim = self.ui.chStim.value()
        fftSize = self.ui.nfft.currentIndex()

        randMin = self.ui.randMin.value()
        randMax = self.ui.randMax.value()
        andor = self.ui.andor.currentIndex()

        ch_order = int(ch_a < chStim)

        fakeStim = int(self.ui.fakeStim.isChecked())

        self.writeCLCh.emit(ch_a, chStim)
        time.sleep(0.4)
        # self.writeCLCh.emit(ch_a, chStim)


        self.writeCL.emit(Reg.cl2, self.makeBit(en1_a,31,1,1) | self.makeBit(ch_a,24,7,1) | 
            self.makeBit(dir1_a,23,1,1) | self.makeBit(thresh1_a,8,15,1) | self.makeBit(chStim,0,7,1) | 
            self.makeBit(ch_order,7,1,1))

        time.sleep(0.02)

        self.writeCL.emit(Reg.cl3, self.makeBit(freq1_max,16,10,1) | self.makeBit(freq1_min,0,10,1))

        time.sleep(0.02)

        self.writeCL.emit(Reg.cl5, self.makeBit(freq2_max,16,10,1) | self.makeBit(freq2_min,0,10,1))

        time.sleep(0.02)

        self.writeCL.emit(Reg.cl6, self.makeBit(en2_a,31,1,1) | 
            self.makeBit(dir2_a,23,1,1) | self.makeBit(thresh2_a,8,15,1) |
            self.makeBit(andor,7,1,1))

        time.sleep(0.02)

        self.writeCL.emit(Reg.cl4, self.makeBit(randMax,16,16,1) | self.makeBit(randMin,0,16,1))

        time.sleep(0.02)

        # time.sleep(0.1)

        # self.writeCL.emit(Reg.cl3, self.makeBit(en_c,31,1,1) | self.makeBit(ch_c,24,7,1) | 
        #     self.makeBit(dir_c,23,1,1) | self.makeBit(thresh_c,16,7,1) |
        #     self.makeBit(en_d,15,1,1) | self.makeBit(ch_d,8,7,1) | 
        #     self.makeBit(dir_d,7,1,1) | self.makeBit(thresh_d,0,7,1))

        self.writeCL.emit(Reg.cl1, self.makeBit(dead_len,16,16,1) | self.makeBit(rand_mode,4,1,1) |
            self.makeBit(CL1_off,3,1,1) | self.makeBit(CL1_on,2,1,1) | 
            self.makeBit(CL0_off,1,1,1) | self.makeBit(CL0_on,0,1,1) | self.makeBit(fftSize,5,3,1) |
            self.makeBit(fakeStim,8,1,1))

        time.sleep(0.02)

    def closedLoopOff(self):

        dead_len = self.ui.deadLength.value()
        rand_mode = int(self.ui.randomMode.isChecked())
        CL1_off = int(not self.ui.enable1.isChecked())
        CL0_off = int(not self.ui.enable0.isChecked())
        CL1_on = int(self.ui.enable1.isChecked())
        CL0_on = int(self.ui.enable0.isChecked())
        chStim = self.ui.chStim.value()
        fftSize = self.ui.nfft.currentIndex()
        ch_a = self.ui.ch1.value()
        ch_order = int(ch_a < chStim)
        fakeStim = int(self.ui.fakeStim.isChecked())     

        self.writeCL.emit(Reg.cl1, self.makeBit(dead_len,16,16,1) | self.makeBit(rand_mode,4,1,1) |
            self.makeBit(CL1_off,3,1,1) | self.makeBit(CL1_on,2,1,1) | 
            self.makeBit(CL0_off,1,1,1) | self.makeBit(CL0_on,0,1,1) | self.makeBit(fftSize,5,3,1) |
            self.makeBit(fakeStim,8,1,1))

        time.sleep(0.02)
