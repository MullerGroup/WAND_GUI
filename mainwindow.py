from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.ui_mainwindow import Ui_MainWindow
from RegisterEditor import *
from PowerControl import *
from StimConfig import *
from BoardControl import BoardControl
from adccontrol import AdcControl
from cmdline import CommandLineWidget
#from nmic_registry import *
#from backend import *
from nmicCommand import NmicCommand
from DataVisualizer import DataVisualizer

class MainWindow(QMainWindow):   
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.worker = None

        self.DataVisualizer = DataVisualizer(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.DataVisualizer)
        
        self.regEdit0 = RegisterEditor(self, 0)
        self.addDockWidget(Qt.RightDockWidgetArea, self.regEdit0)

        self.regEdit1 = RegisterEditor(self, 1)
        self.addDockWidget(Qt.RightDockWidgetArea, self.regEdit1)

        self.sConfig0 = StimConfig(self, 0)
        self.addDockWidget(Qt.RightDockWidgetArea, self.sConfig0)

        self.sConfig1 = StimConfig(self, 1)
        self.addDockWidget(Qt.RightDockWidgetArea, self.sConfig1)

        self.nmicCommand0 = NmicCommand(self, 0)
        self.addDockWidget(Qt.RightDockWidgetArea, self.nmicCommand0)

        self.nmicCommand1 = NmicCommand(self, 1)
        self.addDockWidget(Qt.RightDockWidgetArea, self.nmicCommand1)

        # self.adcControl0 = AdcControl(self, 0)
        # self.addDockWidget(Qt.RightDockWidgetArea, self.adcControl0)
        #
        # self.adcControl1 = AdcControl(self, 1)
        # self.addDockWidget(Qt.RightDockWidgetArea, self.adcControl1)

        # NM0 widgets grouping
        self.tabifyDockWidget(self.regEdit0, self.regEdit1)
        self.tabifyDockWidget(self.regEdit1, self.sConfig0)
        self.tabifyDockWidget(self.sConfig0, self.sConfig1)
        self.tabifyDockWidget(self.sConfig1, self.nmicCommand0)
        self.tabifyDockWidget(self.nmicCommand0, self.nmicCommand1)
        # self.tabifyDockWidget(self.nmicCommand1, self.adcControl0)
        # self.tabifyDockWidget(self.adcControl0, self.adcControl1)

        self.sConfig0.loadState()
        self.sConfig1.loadState()

        self.boardControl = BoardControl(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.boardControl)

        self.cmdline = CommandLineWidget(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.cmdline)

        self.tabifyDockWidget(self.boardControl, self.cmdline)

        s = QSettings()
        if s.value("mainwindow/geometry") is not None:
            self.restoreGeometry(s.value("mainwindow/geometry"))
            self.restoreState(s.value("mainwindow/state"))
        # run loadState when the event loop starts
        QTimer.singleShot(0, self.loadState)

    def setWorker(self, worker):
        self.worker = worker
        self.nmicCommand0.setWorker(worker)
        self.nmicCommand1.setWorker(worker)
        self.boardControl.setWorker(worker)
#        self.pControl.setWorker(worker)
        self.regEdit0.setWorker(worker)
        self.regEdit1.setWorker(worker)
        self.sConfig0.setWorker(worker)
        self.sConfig1.setWorker(worker)
        # self.adcControl0.setWorker(worker)
        # self.adcControl1.setWorker(worker)
        self.DataVisualizer.setWorker(worker)


    @pyqtSlot()
    def loadState(self):
        s = QSettings()
        if s.value("mainwindow/state") is not None:
            self.restoreState(s.value("mainwindow/state"))

    def closeEvent(self, event):
        self.sConfig0.saveState()
        self.sConfig1.saveState()
        self.regEdit0.saveSettings()
        self.regEdit1.saveSettings()
        s = QSettings()
        s.setValue("mainwindow/geometry", self.saveGeometry())
        s.setValue("mainwindow/state", self.saveState())
        super().closeEvent(event)

