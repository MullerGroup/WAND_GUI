from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.ui_nmicConfig import Ui_nmicConfig
from enum import Enum

class Cmd(Enum):
    Reset = 0x01
    ClearErr = 0x02
    HvLoad = 0x03
    ImpStart = 0x04
    StimReset = 0x08
    StimStart = 0x09
    StimXfer = 0x0a

class nmicConfig(QDockWidget):
    setWideIn = pyqtSignal(int, bool)
    enableHV = pyqtSignal(int)
    setZmeasure = pyqtSignal(int, int, int)

    def __init__(self, parent=None, nm=0):
        super().__init__(parent)
        self.nm = nm
        self.ui = Ui_nmicConfig()
        self.ui.setupUi(self)
        
        self.setWindowTitle("NM{} Configuration".format(self.nm))

    def setWorker(self, w):
        self.setWideIn.connect(w.setWideIn)
        self.enableHV.connect(w.enableHV)
        self.setZmeasure.connect(w.setZmeasure)

    @pyqtSlot()
    def on_wideIn_clicked(self):
        self.setWideIn.emit(self.nm, self.ui.wideIn.isChecked())

    @pyqtSlot()
    def on_hvEn_clicked(self):
        self.enableHV.emit(self.nm)

    @pyqtSlot()
    def on_zSet_clicked(self):
        self.setZmeasure.emit(self.nm, self.ui.zMag.currentIndex(), self.ui.zCycle.value())