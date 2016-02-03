from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.ui_powercontrol import Ui_PowerControl

class PowerControl(QDockWidget):
    vdd1Changed = pyqtSignal(float)
    vdd3Changed = pyqtSignal(float)
    vddhChanged = pyqtSignal(float)
    enabledChanged = pyqtSignal(bool, bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_PowerControl()
        self.ui.setupUi(self)
        self.ui.vdd1doubleSpinBox.valueChanged.connect(self.vdd1Changed)
        self.ui.vdd3doubleSpinBox.valueChanged.connect(self.vdd3Changed)
        self.ui.vddhdoubleSpinBox.valueChanged.connect(self.vddhChanged)
        self.ui.vdd1enButton.clicked.connect(self.vddEnChanged)
        self.ui.vdd3enButton.clicked.connect(self.vddEnChanged)

    def setWorker(self, w):
        self.vdd1Changed.connect(w.setPwr1V)
        self.vdd3Changed.connect(w.setPwr3V)
        self.vddhChanged.connect(w.setPwrHV)
        self.enabledChanged.connect(w.setPwrEn)
        w.connStateChanged.connect(self.updateAll)

    @pyqtSlot()
    def updateAll(self):
        self.vdd1Changed.emit(self.ui.vdd1doubleSpinBox.value())
        self.vdd3Changed.emit(self.ui.vdd3doubleSpinBox.value())
        self.vddhChanged.emit(self.ui.vddhdoubleSpinBox.value())
        self.vddEnChanged()

    @pyqtSlot()
    def vddEnChanged(self):
        self.enabledChanged.emit(self.ui.vdd1enButton.isChecked(), self.ui.vdd3enButton.isChecked())
        

    