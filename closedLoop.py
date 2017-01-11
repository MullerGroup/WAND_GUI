from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.ui_closedLoop import Ui_closedLoop
import datetime

class ClosedLoop(QDockWidget):

    writeCL = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_closedLoop()
        self.ui.setupUi(self)
        self.setWindowTitle("Closed Loop Config")

    def setWorker(self, w):
        self.writeCL.connect(w.writeCL)

    @pyqtSlot()
    def on_enable0_clicked(self):
        if self.ui.enable0.isChecked():
            self.ui.enable1.setDisabled(True)
            start = datetime.datetime.now()
            print("NM0 Closed Loop Enabled at: {}".format(start))
        else:
            stop = datetime.datetime.now()
            print("NM0 Closed Loop Disabled at: {}".format(stop))
            self.ui.enable1.setEnabled(True)
        self.closedLoopCmd()

    @pyqtSlot()
    def on_enable1_clicked(self):
        if self.ui.enable1.isChecked():
            self.ui.enable0.setDisabled(True)
            start = datetime.datetime.now()
            print("NM1 Closed Loop Enabled at: {}".format(start))
        else:
            stop = datetime.datetime.now()
            print("NM1 Closed Loop Disabled at: {}".format(stop))
            self.ui.enable0.setEnabled(True)
        self.closedLoopCmd()

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
        en_a = int(self.ui.ch1Enable.currentIndex() != 0)
        ch_a = self.ui.ch1.value()
        dir_a = int(self.ui.ch1Enable.currentIndex() == 1)
        thresh_a = self.ui.threshold1.value()

        en_b = int(self.ui.ch2Enable.currentIndex() != 0)
        ch_b = self.ui.ch2.value()
        dir_b = int(self.ui.ch2Enable.currentIndex() == 1)
        thresh_b = self.ui.threshold2.value()

        en_c = int(self.ui.ch3Enable.currentIndex() != 0)
        ch_c = self.ui.ch3.value()
        dir_c = int(self.ui.ch3Enable.currentIndex() == 1)
        thresh_c = self.ui.threshold3.value()

        en_d = int(self.ui.ch4Enable.currentIndex() != 0)
        ch_d = self.ui.ch4.value()
        dir_d = int(self.ui.ch4Enable.currentIndex() == 1)
        thresh_d = self.ui.threshold4.value()

        dead_len = self.ui.deadLength.value()
        rand_mode = int(self.ui.randomMode.isChecked())
        CL1_off = int(not self.ui.enable1.isChecked())
        CL0_off = int(not self.ui.enable0.isChecked())
        CL1_on = int(self.ui.enable1.isChecked())
        CL0_on = int(self.ui.enable0.isChecked())

        self.writeCL.emit(0xBB, self.makeBit(en_a,31,1,1) | self.makeBit(ch_a,24,7,1) | 
            self.makeBit(dir_a,23,1,1) | self.makeBit(thresh_a,16,7,1) |
            self.makeBit(en_b,15,1,1) | self.makeBit(ch_b,8,7,1) | 
            self.makeBit(dir_b,7,1,1) | self.makeBit(thresh_b,0,7,1))
        self.writeCL.emit(0xCC, self.makeBit(en_c,31,1,1) | self.makeBit(ch_c,24,7,1) | 
            self.makeBit(dir_c,23,1,1) | self.makeBit(thresh_c,16,7,1) |
            self.makeBit(en_d,15,1,1) | self.makeBit(ch_d,8,7,1) | 
            self.makeBit(dir_d,7,1,1) | self.makeBit(thresh_d,0,7,1))
        self.writeCL.emit(0xAA, self.makeBit(dead_len,16,16,1) | self.makeBit(rand_mode,4,1,1) |
            self.makeBit(CL1_off,3,1,1) | self.makeBit(CL1_on,2,1,1) | 
            self.makeBit(CL0_off,1,1,1) | self.makeBit(CL0_on,0,1,1))

