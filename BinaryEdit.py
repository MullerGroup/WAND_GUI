from PyQt4.QtCore import *
from PyQt4.QtGui import *

class BinaryEdit(QWidget):
    valueChanged = pyqtSignal(int)
    
    def __init__(self, parent=None, bits=16):
        super().__init__(parent)
        self.bits = bits
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(-1, 0, -1, 0)
        self.buttons = []
        for i in range(0, bits):
            cb = QCheckBox(self)
            cb.setText("")
            self.layout.addWidget(cb)
            self.buttons.append(cb)
            cb.toggled.connect(self.buttonsChanged)
            if ((i+1) % 4 == 0 and i != (self.bits-1)):
                line = QFrame(self)
                line.setFrameShadow(QFrame.Raised)
                line.setFrameShape(QFrame.VLine)
                line.setFrameShadow(QFrame.Sunken)
                self.layout.addWidget(line)
        
    @pyqtSlot()
    def buttonsChanged(self):
        self.valueChanged.emit(self.value())
    
    def value(self):
        val = 0
        for i in range(0, self.bits):
            if self.buttons[i].isChecked():
                val |= 1<<(self.bits-1-i)
        return val
    
    def setValue(self, value):
        for i in range(0,self.bits):
            self.buttons[i].setChecked(value & (1<<(self.bits - i - 1)) != 0)

    