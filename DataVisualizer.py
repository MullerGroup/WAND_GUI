from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from ui.ui_DataVisualizer import Ui_DataVisualizer
import numpy as np
import scipy.io
from enum import Enum
import pyqtgraph as pg

class Bands(Enum):
    DeltaLow=0
    DeltaHigh=4
    ThetaLow=4
    ThetaHigh=7
    AlphaLow=8
    AlphaHigh=15
    BetaLow=16
    BetaHigh=31
    GammaLow=32
    GammaHigh=100

class NMs(Enum):
    NM0=0
    NM1=1

# TODO: FFT output doesn't look correct

def calculateFFT(d):
    fft = np.abs(np.fft.rfft(d, n=100)) # 100 point FFT
    return fft

class DataVisualizer(QDockWidget):
    readAdc = pyqtSignal(int)

    class PlotEventFilter(QObject):
        mouseDoubleClick = pyqtSignal()
        mouseClick = pyqtSignal()
        keySpace = pyqtSignal()

        def eventFilter(self, object, event):
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Space:
                    self.keySpace.emit()
                    return True
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                self.mouseDoubleClick.emit()
                return True
            return False

# TODO: change pyqtgraph to RectMode instead of PanMode - this should allow mouse and key events inside the plot area

    def __init__(self, parent=None):
        def populate(listbox, start, stop, step):
            for i in range(start,stop+step,step):
                listbox.addItem("{}".format(i))
        super().__init__(parent)
        self.ui = Ui_DataVisualizer()
        self.ui.setupUi(self)
        self.data = []
        self.lastfile = ""
        self.numPlots = 128
        self.numPlotsDisplayed = 16
        # self.xRange = 5 # number of seconds over which to plot continuous data
        self.plots = []
        self.plotGroup = 0 # which group of numPlotsDisplayed (16) plots to display at once (0: 0-15, 1: 16-31, ...)
        self.fftPlots = []
        self.plotEn = [] # each plot can be enabled/disabled by pressing spacebar on top of it

        # self.ui.plot.scene().sigMouseClicked.connect(self.getPos)

        # self.filter = self.PlotEventFilter(self)
        # self.ui.plot.sigMouseReleased.connect(self.getPos)
        # self.ui.plot.sigMouseClicked.connect(self.getPos)
        # self.filter.keySpace.connect(self.enablePlot)
        # self.filter.mouseClick.connect(self.getPos)
        # self.filter.mouseDoubleClick.connect(self.enablePlot)

        self.setWindowTitle("Data Visualizer")

        # populate array of plots
        for i in range(0,self.numPlots):
            self.plots.append(pg.PlotItem().plot())

        self.updatePlotDisplay()

        # populate combo boxes
        # populate(self.ui.numBands, 1, 5, 1)
        # populate(self.ui.fStart1, 0, 100, 5)
        # populate(self.ui.fStart2, 0, 100, 5)
        # populate(self.ui.fStart3, 0, 100, 5)
        # populate(self.ui.fStart4, 0, 100, 5)
        # populate(self.ui.fStart5, 0, 100, 5)
        # populate(self.ui.fStop1, 0, 100, 5)
        # populate(self.ui.fStop2, 0, 100, 5)
        # populate(self.ui.fStop3, 0, 100, 5)
        # populate(self.ui.fStop4, 0, 100, 5)
        # populate(self.ui.fStop5, 0, 100, 5)

        # every time the # of bands changes, update the band selection boxes
        # self.ui.numBands.currentIndexChanged.connect(self.updateBands)
        self.ui.autorange.clicked.connect(self.updatePlot)

        # set some defaults
        # self.ui.numBands.setCurrentIndex(0)
        self.ui.autorange.setChecked(True)
        # self.updateBands()

    def setWorker(self, w):
        self.readAdc.connect(w.readAdc)
        w.adcData.connect(self.adcData)

    def updateBands(self):
        self.ui.fStart5.setEnabled(self.ui.numBands.currentIndex() >= 4)
        self.ui.fStop5.setEnabled(self.ui.numBands.currentIndex() >= 4)
        self.ui.fStart4.setEnabled(self.ui.numBands.currentIndex() >= 3)
        self.ui.fStop4.setEnabled(self.ui.numBands.currentIndex() >= 3)
        self.ui.fStart3.setEnabled(self.ui.numBands.currentIndex() >= 2)
        self.ui.fStop3.setEnabled(self.ui.numBands.currentIndex() >= 2)
        self.ui.fStart2.setEnabled(self.ui.numBands.currentIndex() >= 1)
        self.ui.fStop2.setEnabled(self.ui.numBands.currentIndex() >= 1)
        self.ui.fStart1.setEnabled(self.ui.numBands.currentIndex() >= 0)
        self.ui.fStop1.setEnabled(self.ui.numBands.currentIndex() >= 0)

    def keyPressEvent(self, QKeyEvent):
        # enable/disable plot under cursor
        if QKeyEvent.key() == Qt.Key_Space:
            print("spacebar") # TODO: implement enable/disable plots under cursor
            self.updatePlotDisplay()

        # scroll through sets of plots
        if QKeyEvent.key() == Qt.Key_PageDown:
            if self.plotGroup < (self.numPlots/self.numPlotsDisplayed) - 1:
                self.plotGroup += 1
                self.updatePlotDisplay()
        if QKeyEvent.key() == Qt.Key_PageUp:
            if self.plotGroup > 0:
                self.plotGroup -= 1
                self.updatePlotDisplay()

    # @pyqtSlot()
    # def getPos(self, event):
    #     print("hello")
    #     items = self.ui.plot.scene().items(event.scenePos())
    #     print("# of items: {}".format(items.count))
    #     print("Plots: {}".format(x for x in items if isinstance(x, pg.PlotItem)))
    #     items[0].setTitle("testing")
    #     # p = self.ui.plot.scene().mousePressEvent()
    #     # p = self.ui.plot.mapFromScene(pos)
    #     print("hello2")
    #     # p = QPoint(event.pos.x(), event.pos.y())
    #     # # p = QtGui.QCursor.pos()
    #     # print("position clicked: {}, {}".format(p.x(), p.y()))

    @pyqtSlot(list)
    def adcData(self, data):
        self.data = data
        self.updatePlot()
        if self.ui.autoBtn.isChecked():
            QTimer.singleShot(250, self.on_singleBtn_clicked())

    @pyqtSlot()
    def on_singleBtn_clicked(self):
        self.readAdc.emit(self.ui.samples.value())
        self.readAdc.emit(self.ui.samples.value())

    @pyqtSlot()

    def updatePlotDisplay(self):
       for j in reversed(range(0,4)):
            for i in reversed(range(0,4)):
                plotToDelete = self.ui.plot.getItem(j,i)
                if plotToDelete is not None:
                    self.ui.plot.removeItem(plotToDelete)

       for i in range(self.plotGroup*16, self.plotGroup*16 + self.numPlotsDisplayed):
            self.plots[i] = self.ui.plot.addPlot(row=i%4, col=int(i/4)%4)
            self.plots[i].setTitle(title='Ch {}'.format(i), size='8px')

    @pyqtSlot()
    def updatePlot(self):
        if not self.data:
            return
        data = []
        for ch in range(0,self.numPlots): # store data for all channels in array
            data.append((np.array([i[ch] for i in self.data])))

# TODO: implement scrolling, o-scope style plotting. Pre-allocate data array for self.xRange*1000 samples (xRange seconds)
# TODO: and add data to this. When you reach the end, loop back to beginning.
        for ch in range(self.plotGroup*16, self.plotGroup*16 + self.numPlotsDisplayed): # only plot currently displayed plots
            dp = data[ch]
            self.plots[ch].clear()
            # self.fftPlots[ch].clear()
            if self.plotEn[ch]:
                self.plots[ch].plot(y=dp, pen=(102,204,255))
                # self.plots[ch].plot(y=dp, pen=(ch,16)) # different color for each plot
                if self.ui.autorange.isChecked():
                    self.plots[ch].getViewBox().autoRange()
                # self.fftPlots[ch].plot(y=calculateFFT(dp), pen=(102,204,255))
                # if self.ui.autorange.isChecked():
                    # self.fftPlots[ch].getViewBox().autoRange()

