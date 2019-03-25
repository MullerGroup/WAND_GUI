from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.ui_mainwindow import Ui_MainWindow
from RegisterEditor_v2 import *
from StimConfig import *
from BoardControl import BoardControl
from cmdline import CommandLineWidget
#from nmic_registry import *
#from backend import *
from nmicCommand import NmicCommand
from DataVisualizer import DataVisualizer
from nmicConfig import *

class MainWindow(QMainWindow):   
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.worker = None

        self.DataVisualizer = DataVisualizer(self)
        self.DataVisualizer.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.DataVisualizer)

        self.nmicConfig0 = nmicConfig(self,0)
        self.nmicConfig0.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.RightDockWidgetArea, self.nmicConfig0)

        self.sConfig0 = StimConfig(self, 0)
        self.sConfig0.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.RightDockWidgetArea, self.sConfig0)

        self.nmicCommand0 = NmicCommand(self, 0)
        self.nmicCommand0.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.RightDockWidgetArea, self.nmicCommand0)

        self.regEdit0 = RegisterEditor_v2(self, 0)
        self.regEdit0.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.RightDockWidgetArea, self.regEdit0)


        # NM0 widgets grouping
        self.tabifyDockWidget(self.nmicConfig0, self.sConfig0)
        self.tabifyDockWidget(self.sConfig0, self.nmicCommand0)
        self.tabifyDockWidget(self.nmicCommand0, self.regEdit0)

        self.sConfig0.loadState()

        self.boardControl = BoardControl(self)
        self.boardControl.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.RightDockWidgetArea, self.boardControl)

        self.cmdline = CommandLineWidget(self)
        self.cmdline.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.RightDockWidgetArea, self.cmdline)

        self.tabifyDockWidget(self.boardControl, self.cmdline)

        s = QSettings("settings.plist", QSettings.NativeFormat)
        if s.value("mainwindow/geometry") is not None:
            self.restoreGeometry(s.value("mainwindow/geometry"))
        if s.value("mainwindow/state") is not None:
            self.restoreState(s.value("mainwindow/state"))
        # run loadState when the event loop starts
        QTimer.singleShot(0, self.loadState)

    def setWorker(self, worker):
        self.worker = worker
        self.nmicCommand0.setWorker(worker)
        self.boardControl.setWorker(worker)
        self.regEdit0.setWorker(worker)
        self.sConfig0.setWorker(worker)
        self.DataVisualizer.setWorker(worker)
        self.nmicConfig0.setWorker(worker)


    @pyqtSlot()
    def loadState(self):
        s = QSettings("settings.plist", QSettings.NativeFormat)
        if s.value("mainwindow/state") is not None:
            self.restoreState(s.value("mainwindow/state"))

    def closeEvent(self, event):
        self.sConfig0.saveState()
        self.regEdit0.saveSettings()
        s = QSettings("settings.plist", QSettings.NativeFormat)
        s.setValue("mainwindow/geometry", self.saveGeometry())
        s.setValue("mainwindow/state", self.saveState())
        super().closeEvent(event)

