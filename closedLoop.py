from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.ui_closedLoop import Ui_closedLoop
import datetime

class ClosedLoop(QDockWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_closedLoop()
        self.ui.setupUi(self)
        self.setWindowTitle("Closed Loop Config")

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