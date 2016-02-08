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

class NMs(Enum):
    NM0=0
    NM1=1

# TODO: FFT output doesn't look correct

def calculateFFT(d):
    fft = np.abs(np.fft.rfft(d, n=100)) # 100 point FFT
    return fft

class DataVisualizer(QDockWidget):
    readAdc = pyqtSignal(int)

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
        self.plots = []
        self.fftPlots = []
        self.plotEn = [] # each plot has checkbox for enabling/disabling

        self.setWindowTitle("Data Visualizer")

        # populate plots
        for i in range(0,self.numPlots):
            # self.ui.plot.addLabel(text='Ch {}'.format(i))
            self.plots.append(self.ui.plot.addPlot())
            self.plots[i].setTitle(title='Ch {}'.format(i))
            self.ui.plot.nextColumn()
            # self.fftPlots.append(self.ui.plot.addPlot())
            # self.fftPlots[i].setTitle(title='FFT {}'.format(i))
            # self.ui.plot.nextColumn()
            if not (i+1)%16: self.ui.plot.nextRow()
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
        self.ui.autorange.setChecked(True)
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

# TODO:
    '''
adcData gets called from cmbackend each time Update button is pressed. This means that every time it is
called, updatePlot is also called but on both modules!
this is kind of a moot problem, because I should actually change the plot GUI to have all channels.
whenever you want to read some adc data, the NMIC spits out all channels so that they're synced in time.
I need to ensure that whenever I get data, both NMs send their data out so that they're also synced with each other.
This needs to be handled GUI/CM side.

Solution: make 1 widget with all 128 channels, with single Update button.
When this is pressed, request data from both NMs at the same time, and return it.
Channels are then numbered 0-127, which can be represented as nm*64+i for i in range (0, 64)
That is, channels 0-63 correspond to nm=0 and channels 64-127 correspond to nm=1

Finally, I can get rid of the original ADC Control module and just have 1 single Data Visualization module
'''
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

