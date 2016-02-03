from PyQt4.QtCore import *
from PyQt4.QtGui import *

class LabeledBinaryEdit(QWidget):
    valueChanged = pyqtSignal(int)
    
    def __init__(self, parent=None, bits=16, labels=[]):
        super().__init__(parent)
        self.bits = bits
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(-1, 0, -1, 0)
        self.buttons = []
        col = 0
        for l in labels:
            lbl = QLabel()
            lbl.setText(l[0])
            lbl.setFrameShape(QFrame.Box)
            lbl.setAlignment(Qt.AlignCenter)
            if l[0] != "":
                lbl.setStyleSheet("QLabel { background-color: rgb(202,255,192); }")
            self.layout.addWidget(lbl, 0, col, 1, l[1])
            col += l[1]
        for i in range(0, bits):
            cb = QCheckBox(self)
            cb.setText("")
            self.layout.addWidget(cb,1,i, Qt.AlignCenter)
            self.buttons.append(cb)
            cb.toggled.connect(self.buttonsChanged)
            # if ((i+1) % 4 == 0 and i != (self.bits-1)):
            #     line = QFrame(self)
            #     line.setFrameShadow(QFrame.Raised)
            #     line.setFrameShape(QFrame.VLine)
            #     line.setFrameShadow(QFrame.Sunken)
            #     self.layout.addWidget(line)
        
    @pyqtSlot()
    def buttonsChanged(self):
        self.valueChanged.emit(self.value())

    @pyqtSlot()
    def toggleAll(self):
        newState = True
        if self.buttons[0].isChecked():
            newState = False
        for b in self.buttons:
            b.setChecked(newState)
    
    def value(self):
        val = 0
        for i in range(0, self.bits):
            if self.buttons[i].isChecked():
                val |= 1<<(self.bits-1-i)
        return val
    
    def setValue(self, value):
        for i in range(0,self.bits):
            self.buttons[i].setChecked(value & (1<<(self.bits - i - 1)) != 0)

    