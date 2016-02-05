from PyQt4.QtCore import *
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

def calculateFFT(d):
    fft = np.abs(np.fft.rfft(d, n=100)) # 100 point FFT
    return fft

class DataVisualizer(QDockWidget):
    readAdc = pyqtSignal(int, int)

    def __init__(self, parent=None, nm=0):
        def populate(listbox, start, stop, step):
            for i in range(start,stop+step,step):
                listbox.addItem("{}".format(i))
        super().__init__(parent)
        self.nm = nm
        self.ui = Ui_DataVisualizer()
        self.ui.setupUi(self)
        self.data = []
        self.lastfile = ""
        self.numPlots = 4
        self.plots = []
        self.fftPlots = []
        self.plotEn = [] # each plot has checkbox for enabling/disabling

        # populate plots
        for i in range(0,self.numPlots):
            # self.ui.plot.addLabel(text='Ch {}'.format(i))
            self.plots.append(self.ui.plot.addPlot())
            self.plots[i].setTitle(title='Ch {}'.format(i))
            self.ui.plot.nextColumn()
            self.fftPlots.append(self.ui.plot.addPlot())
            self.fftPlots[i].setTitle(title='FFT {}'.format(i))
            self.ui.plot.nextColumn()
            if not (i+1)%8: self.ui.plot.nextRow()
            # self.plotEn[i] = True # enable all plots initially

            # self.plotEn[i].clicked.connect(self.updatePlot) # update on enable/disable
            # populate(self.plotCh[i])
            # self.plotCh[i].currentIndexChanged.connect(self.updatePlot)

        # populate combo boxes
        populate(self.ui.numBands, 1, 5, 1)
        populate(self.ui.fStart1, 0, 100, 5)
        populate(self.ui.fStart2, 0, 100, 5)
        populate(self.ui.fStart3, 0, 100, 5)
        populate(self.ui.fStart4, 0, 100, 5)
        populate(self.ui.fStart5, 0, 100, 5)
        populate(self.ui.fStop1, 0, 100, 5)
        populate(self.ui.fStop2, 0, 100, 5)
        populate(self.ui.fStop3, 0, 100, 5)
        populate(self.ui.fStop4, 0, 100, 5)
        populate(self.ui.fStop5, 0, 100, 5)

        # every time the # of bands changes, update the band selection boxes
        self.ui.numBands.currentIndexChanged.connect(self.updateBands)
        self.ui.autorange.clicked.connect(self.updatePlot)

        # set some defaults
        self.ui.numBands.setCurrentIndex(0)
        self.updateBands()

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

    @pyqtSlot(list)
    def adcData(self, data):
        self.data = data
        self.updatePlot()
        if self.ui.autoBtn.isChecked():
            QTimer.singleShot(250, self.on_singleBtn_clicked())

    @pyqtSlot()
    def on_singleBtn_clicked(self):
        self.readAdc.emit(self.nm, self.ui.samples.value())

    @pyqtSlot()
    def updatePlot(self):
        if not self.data:
            return
        data = []
        for ch in range(0,self.numPlots):
            #data.append((np.array([i[ch] for i in self.data])-32768/2)*(100e-3/32768)*1e6)
            data.append((np.array([i[ch] for i in self.data])))

        for ch in range(0, self.numPlots):
            dp = data[ch]
            self.plots[ch].clear()
            self.fftPlots[ch].clear()
            # if self.plotEn[ch].isChecked():
            self.plots[ch].plot(y=dp, pen=(102,204,255))
            if self.ui.autorange.isChecked():
                self.plots[ch].getViewBox().autoRange()
            self.fftPlots[ch].plot(y=calculateFFT(dp), pen=(102,204,255))
            if self.ui.autorange.isChecked():
                self.fftPlots[ch].getViewBox().autoRange()

