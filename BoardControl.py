from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.ui_boardcontrol import Ui_BoardControl
import time

class BoardControl(QDockWidget):
    refreshBoards = pyqtSignal()
    connectToBoard = pyqtSignal(str)
    disconnectBoard = pyqtSignal(str)
    resetSerial = pyqtSignal()
    flushCommandFifo = pyqtSignal()
    flushDataFifo = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_BoardControl()
        self.ui.setupUi(self)
        # self.ui.disconnBtn.clicked.connect(self.disconnectBoard)
        self.ui.refreshBtn.clicked.connect(self.refreshBoards)

    def setWorker(self, worker):
        self.refreshBoards.connect(worker.refreshBoards)
        self.connectToBoard.connect(worker.connectToBoard)
        self.disconnectBoard.connect(worker.disconnectBoard)
        self.resetSerial.connect(worker.resetSerial)
        self.connect = self.flushCommandFifo.connect(worker.flushCommandFifo)
        self.flushDataFifo.connect(worker.flushDataFifo)
        worker.boardsChanged.connect(self.boardsChanged)
        worker.connStateChanged.connect(self.connStateChanged)
        self.refreshBoards.emit()

    @pyqtSlot(list)
    def boardsChanged(self, boardList):
        for i in range(0, self.ui.selectBox.count()):
            self.ui.selectBox.removeItem(i)
        self.ui.selectBox.insertItems(0, boardList)

    @pyqtSlot(bool)
    def connStateChanged(self, connected):
        self.ui.connectBtn.setEnabled(not connected)
        self.ui.disconnBtn.setEnabled(connected)
        self.ui.refreshBtn.setEnabled(not connected)
        self.ui.selectBox.setEnabled(not connected)

    @pyqtSlot()
    def on_connectBtn_clicked(self):
        currBoard = self.ui.selectBox.currentText()
        if currBoard:
            self.connectToBoard.emit(currBoard)

    @pyqtSlot()
    def on_disconnBtn_clicked(self):
        currBoard = self.ui.selectBox.currentText()
        if currBoard:
            self.disconnectBoard.emit(currBoard)

    @pyqtSlot()
    def on_flushCommandBtn_clicked(self):
        self.flushCommandFifo.emit()

    @pyqtSlot()
    def on_flushDataBtn_clicked(self):
        self.flushDataFifo.emit()

    @pyqtSlot()
    def on_resetBtn_clicked(self):
        self.resetSerial.emit()