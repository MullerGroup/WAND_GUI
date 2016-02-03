from PyQt4.QtCore import *
from PyQt4.QtGui import *

class RoundedSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editingFinished.connect(self.fixValue)

    def fixValue(self):
        val = self.value()
        vint = round((val - self.minimum()) / self.singleStep())
        self.setValue(vint * self.singleStep() + self.minimum())

    def getAsInt(self):
        return int(round(self.value()/self.singleStep()))