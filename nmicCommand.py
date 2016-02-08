from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.ui_commanddockwidget import Ui_nmicCommand
from enum import Enum

class Cmd(Enum):
    Reset = 0x01
    ClearErr = 0x02
    HvLoad = 0x03
    ImpStart = 0x04
    StimReset = 0x08
    StimStart = 0x09
    StimXfer = 0x0a

class NmicCommand(QDockWidget):
    nmicCommand = pyqtSignal(int, int)

    def __init__(self, parent=None, nm=0):
        super().__init__(parent)
        self.nm = nm
        self.ui = Ui_nmicCommand()
        self.ui.setupUi(self)
        def slotFunc(cmd):
            return lambda: self.nmicCommand.emit(nm, cmd.value)
        self.ui.reset.clicked.connect(slotFunc(Cmd.Reset))
        self.ui.clear_err.clicked.connect(slotFunc(Cmd.ClearErr))
        self.ui.hv_load.clicked.connect(slotFunc(Cmd.HvLoad))
        self.ui.imp_start.clicked.connect(slotFunc(Cmd.ImpStart))
        self.ui.stim_reset.clicked.connect(slotFunc(Cmd.StimReset))
        self.ui.stim_start.clicked.connect(slotFunc(Cmd.StimStart))
        self.ui.stim_transfer.clicked.connect(slotFunc(Cmd.StimXfer))

        self.setWindowTitle("NM{} Commands".format(self.nm))

    def setWorker(self, w):
        self.nmicCommand.connect(w.nmicCommand)