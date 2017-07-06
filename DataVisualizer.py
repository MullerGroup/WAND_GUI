from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from ui.ui_DataVisualizer import Ui_DataVisualizer
import numpy as np
import scipy.io
from enum import Enum
import pyqtgraph as pg
import tables
from tables import *
from datetime import datetime
import time
# import QThread
import cmbackend
import csv
from numpy import arange


# CM register addresses
class Reg(Enum):
    ctrl = 0x00
    rst = 0x04
    n0d1 = 0x10
    n0d2 = 0x14
    n1d1 = 0x20
    n1d2 = 0x24
    req = 0xff
    cl1 = 0xDD
    cl2 = 0xEE
    cl3 = 0xCC
    cl4 = 0xBB
    cl5 = 0xAB
    cl6 = 0xCD

class omni_data(IsDescription):
    # data = UInt16Col(shape=(1,64))
    # data = UInt16Col(shape=(1,96))
    # 96 neural channels, 3 accelerometer channels
    data = UInt16Col(shape=(1,5))
    time = StringCol(26)

def calculateFFT(d):
    fft = np.abs(np.fft.rfft(d, n=100)) # 100 point FFT - change to be based on xRange?
    return fft

class DataVisualizer(QDockWidget):
    readAdc = pyqtSignal(int)
    streamAdc = pyqtSignal()
    enableArtifact = pyqtSignal()
    disableArtifact = pyqtSignal()
    enableInterpolate = pyqtSignal()
    disableInterpolate = pyqtSignal()
    regFile = pyqtSignal(str)

    deadlen = (0 >> 16) & 0xFFFF
    fakestim = (0 >> 8) & 0x01
    fftsize = (0 >> 5) & 0x07
    randmode = (0 >> 4) & 0x01
    en1 = (0 >> 2) & 0x01
    en0 = 0 & 0x01
    enA = (0 >> 31) & 0x01
    chctrl = (0 >> 24) & 0x7F
    dirA = (0>>23) & 0x01
    threshA = (0 >> 8) & 0x7FFF
    chorder = (0 >> 7) & 0x01
    chstim = 0 & 0x7F
    freqmaxA = (0 >> 16) & 0x3FF
    freqminA = 0 & 0x3FF
    randMax = (0 >> 16) & 0xFF
    randMin = 0 & 0xFF
    freqmaxB = (0 >> 16) & 0x3FF
    freqminB = 0 & 0x3FF
    enB = (0 >> 31) & 0x01
    dirB = (0 >> 23) & 0x01
    threshB = (0 >> 8) & 0x7FFF
    andor = (0 >> 7) & 0x01
    mag_dataA = 0
    mag_dataB = 0
    derivative = 0
    derivativeB = 0
    signA = 0
    signB = 0

    def __init__(self, parent=None):
        def populate(listbox, start, stop, step):
            for i in range(start,stop+step,step):
                listbox.addItem("{}".format(i))
        super().__init__(parent)
        self.ui = Ui_DataVisualizer()
        self.ui.setupUi(self)
        self.data = []
        self.fft_data = []
        self.mag_dataA = 0
        self.mag_dataB = 0
        # self.numPlots = 64
        # added 3 more channels just to display accel data
        self.numPlots = 5
        self.xRange = self.ui.xRange.value() # number of ms (samples) over which to plot continuous data

        self.dataPlot = np.zeros((self.numPlots, self.ui.xRange.maximum())) # aggregation of data to plot (scrolling style)
        self.plotPointer = 0 # pointer to current x position in plot (for plotting scrolling style)

        self.numPlotsDisplayed = 4
        self.plots = [] # stores pyqtgraph objects
        self.topPlot = 0 # which channel to begin display w/ (used for scrolling through plots)
        self.fftPlots = []
        self.plotEn = [] # each plot can be enabled/disabled by pressing spacebar on top of it
        self.plotColors = []
        self.enabledChannels = [65535,65535,65535,65535,65535,65535,0,0]

        # initialize streaming mode thread
        self.streamAdcThread = cmbackend.streamAdcThread()
        self.connect(self.streamAdcThread, SIGNAL("finished()"), self.streamingDone)
        self.streamAdcThread.streamAdcData.connect(self.streamAdcData)
        self.streamAdcThread.plotfft.connect(self.plotfft)
        self.streamAdcThread.plotmag.connect(self.plotmag)
        # self.connect(self.streamAdcThread, SIGNAL('streamDataOut(PyQt_PyObject)'), self.streamAdcData)

        # self.file = open('gui_data.csv','w')
        # self.csvfile = csv.writer(self.file)

        self.setWindowTitle("Data Visualizer")

        # populate arrays
        for i in range(0,self.numPlots):
            self.plots.append(pg.PlotItem().plot())
            self.plotEn.append(True)
            self.plotColors.append(pg.intColor(i%16,16))

        self.updatePlotDisplay()

        self.ui.autorange.clicked.connect(self.updatePlotStream)
        self.ui.xRange.valueChanged.connect(self.updatePlotDisplay)
        self.ui.clearBtn.clicked.connect(self.clearPlots)

        # set some defaults
        self.ui.autorange.setChecked(True)

    @pyqtSlot()
    def streamingDone(self):
        self.ui.interpolateBtn.setEnabled(True)

    def setWorker(self, w):
        # self.enableArtifact.connect(w.enableArtifact)
        # self.disableArtifact.connect(w.disableArtifact)
        # self.enableInterpolate.connect(w.enableInterpolate)
        # self.disableInterpolate.connect(w.disableInterpolate)
        w.updateChannels.connect(self.updateChannels)
        w.writeCLInfo.connect(self.writeCLInfo)
        self.regFile.connect(w.regFile)

    def wheelEvent(self, QWheelEvent):
        # scrolling through plots
        modifiers = QApplication.keyboardModifiers()

        # fast scroll
        if modifiers == QtCore.Qt.ShiftModifier:
            if QWheelEvent.delta() < 0: # scroll down
                if self.topPlot+2*self.numPlotsDisplayed < self.numPlots:
                    self.topPlot += self.numPlotsDisplayed
                else:
                    self.topPlot = self.numPlots-self.numPlotsDisplayed
                self.updatePlotDisplay()
            if QWheelEvent.delta() > 0: # scroll up
                if self.topPlot > self.numPlotsDisplayed:
                    self.topPlot -= self.numPlotsDisplayed
                else:
                    self.topPlot = 0
                self.updatePlotDisplay()

        # slow scroll
        else:
            if QWheelEvent.delta() < 0: # scroll down
                if self.topPlot+self.numPlotsDisplayed < self.numPlots:
                    self.topPlot += 1
                    self.updatePlotDisplay()
            if QWheelEvent.delta() > 0: # scroll up
                if self.topPlot > 0:
                    self.topPlot -= 1
                    self.updatePlotDisplay()

    def measureDist(d):
        indx = 11
        dfft = np.abs(np.fft.fft(d))
        fund = dfft[indx]
        dist = 0
        for i in range(2, 32):
            dist += dfft[i * indx] ** 2
        return 20 * np.log10(dist ** 0.5 / fund)

    def measureRms(d):
        ff = np.abs(np.fft.fft(d)) / len(d)
        ff[0] = 0
        # notch out 60 hz harmonics
        rms60 = 0
        for i in range(1, 5):
            rms60 += ff[60 * i] ** 2
            ff[60 * i] = 0
        rms60 **= 0.5
        rms = np.sum(ff[0:500] ** 2) ** 0.5
        # print("RMS: {}   60 Hz: {}".format(rms, rms60))
        # rms_full = np.std(d)
        # print("RMS: {}".format(rms_full))
        return rms

    @pyqtSlot(list)
    def updateChannels(self,chan):
        self.enabledChannels = chan

    @pyqtSlot(int, int)
    def writeCLInfo(self,addr,value):
        if addr == Reg.cl1:
            self.deadlen = (value >> 16) & 0xFFFF
            self.fakestim = (value >> 8) & 0x01
            self.derivative = (value >> 9) & 0x01
            self.derivativeB = (value >> 10) & 0x01
            self.fftsize = (value >> 5) & 0x07
            self.randmode = (value >> 4) & 0x01
            self.en1 = (value >> 2) & 0x01
            self.en0 = value & 0x01
            if (self.en1 == 1) or (self.en0 == 1):
                self.streamAdcThread.writeCLInfo(self.deadlen, self.fakestim, self.fftsize, self.randmode, self.en1, self.en0,
                    self.enA, self.chctrl, self.dirA, self.threshA, self.chorder, self.chstim,
                    self.freqmaxA, self.freqminA, self.randMax, self.randMin, self.freqmaxB, self.freqminB,
                    self.enB, self.dirB, self.threshB, self.andor, self.derivative, self.signA, self.signB, self.derivativeB)

        elif addr == Reg.cl2:
            self.enA = 1
            self.chctrl = (value >> 24) & 0x7F
            self.dirA = (value>>23) & 0x01
            self.threshA = (value >> 8) & 0x7FFF
            self.signA = (value >> 31) & 0x01
            self.chorder = (value >> 7) & 0x01
            self.chstim = value & 0x7F
        elif addr == Reg.cl3:
            self.freqmaxA = (value >> 16) & 0x3FF
            self.freqminA = value & 0x3FF
        elif addr == Reg.cl4:
            self.randMax = (value >> 16) & 0xFF
            self.randMin = value & 0xFF
        elif addr == Reg.cl5:
            self.freqmaxB = (value >> 16) & 0x3FF
            self.freqminB = value & 0x3FF
        elif addr == Reg.cl6:
            self.enB = (value >> 31) & 0x01
            self.dirB = (value >> 23) & 0x01
            self.threshB = (value >> 8) & 0x7FFF
            self.signB = (value >> 24) & 0x01
            self.andor = (value >> 7) & 0x01


    @pyqtSlot(list)
    def streamAdcData(self, data):
        self.data = data
        self.updatePlotStream()

    @pyqtSlot(list)
    def plotfft(self,fft_data):
        # self.fft_data = fft_data
        # self.fft_data = []
        # temp = []
        # n = len(fft_data)
        # if (n & (n-1) == 0):
        #     indexs = arange(n)
        #     for i in self.bit_reverse_traverse(indexs):
        #         temp.append(fft_data[i])
        #     for i in range(0,int(n/2)):
        #         self.fft_data.append(temp[i])
        #     for i in range(0,int(n/2)):
        #         if temp[n-i-1] > self.fft_data[i]:
        #             self.fft_data[i] = temp[n-i-1]

        self.fft_data = []
        temp = []
        n = len(fft_data)
        if (n & (n-1) == 0):
            for i in range(0,int(n/2)):
                self.fft_data.append(fft_data[i])
            for i in range(0,int(n/2)):
                if fft_data[n-i-1] > self.fft_data[i]:
                    self.fft_data[i] = fft_data[n-i-1]

    @pyqtSlot(list)
    def plotmag(self,mag_data):
        # self.mag_data = mag_data
        # n = len(mag_data)
        # for i in range(0,int(n/2)):
        #     self.mag_data.append(mag_data[i])
        # for i in range(0,int(n/2)):
        #     if mag_data[n-i-1] > self.mag_data[i]:
        #         self.mag_data[i] = mag_data[n-i-1]
        # self.mag_data = []
        # temp = []
        # n = len(mag_data)
        # if (n & (n-1) == 0):
        #     for i in range(0,int(n/2)):
        #         self.mag_data.append(mag_data[i])
        if len(mag_data) == 2**(self.fftsize + 3):
            # self.mag_dataA = 30
            # for i in list(range(self.freqminA,freqmaxA+1,1)):
            #     self.mag_dataA = self.mag_dataA + mag_data[i]
            # self.mag_dataB = 20
            # for i in list(range(self.freqminB,freqmaxB+1,1)):
            #     self.mag_dataB = self.mag_dataB + mag_data[i]
            self.mag_dataA = sum(list(mag_data[i] for i in list(range(self.freqminA,self.freqmaxA+1,1))))
            self.mag_dataB = sum(list(mag_data[i] for i in list(range(self.freqminB,self.freqmaxB+1,1))))
    # @pyqtSlot(list)
    # def bit_reverse_traverse(self,a):
    #     n = a.shape[0]
    #     assert(not n&(n-1)) # assert that n is a power of 2

    #     if n == 1:
    #         yield a[0]
    #     else:
    #         even_index = arange(n/2)*2
    #         odd_index = arange(n/2)*2 + 1
    #         for even in self.bit_reverse_traverse(a[even_index.astype(int)]):
    #             yield even
    #         for odd in self.bit_reverse_traverse(a[odd_index.astype(int)]):
    #             yield odd

    # @pyqtSlot(list)
    # def streamAdcData(self, data):
    #     global t_start
    #     t_start = datetime.now()
    #     self.data = data
    #     if self.ui.plotEn.isChecked():
    #         self.updatePlot()

    @pyqtSlot()
    def on_streamBtn_clicked(self):
        if self.ui.streamBtn.isChecked():
            print("stream started with nmStim value  {}".format(self.ui.stimOnNM.currentIndex()))
            self.streamAdcThread.setup(True, self.ui.stim.isChecked(), self.ui.ch0.value(), self.ui.ch1.value(), self.ui.ch2.value(), self.ui.ch3.value(), self.ui.stimRep.value(), self.ui.stimDelay.value(), False, self.ui.interpolateBtn.isChecked(), self.ui.artDelay.value(), self.ui.stimOnNM.currentIndex(), self.ui.impStart.isChecked(), self.ui.impDelay.value())
            self.streamAdcThread.start()
            self.ui.interpolateBtn.setDisabled(True)
            self.updatePlotDisplay()
        else:
            filename = self.streamAdcThread.stop()
            self.regFile.emit(filename)

    @pyqtSlot()
    def on_testBtn_clicked(self):
        if self.ui.testBtn.isChecked():
            #print("Test Comm On")
            self.testCommOn.emit()
        else:
            #print("Test Comm Off")
            self.testCommOff.emit()

    @pyqtSlot()
    def clearPlots(self):
        self.fft_data = []
        self.plotPointer = 0
        self.dataPlot = np.zeros(
            (self.numPlots, self.ui.xRange.maximum()))  # aggregation of data to plot (scrolling style)
        for ch in range(self.topPlot, self.topPlot + self.numPlotsDisplayed):
            self.plots[ch].clear()

    @pyqtSlot()
    def updatePlotDisplay(self):
        for j in reversed(range(0,self.numPlotsDisplayed)):
            plotToDelete = self.ui.plot.getItem(j,0)
            if plotToDelete is not None:
                self.ui.plot.removeItem(plotToDelete)

        self.numPlotsDisplayed = 4
        self.xRange = self.ui.xRange.value()
        if self.topPlot+self.numPlotsDisplayed > self.numPlots:
            self.topPlot = self.numPlots - self.numPlotsDisplayed
        for i in range(self.topPlot, self.topPlot + self.numPlotsDisplayed):
            viewBox = pg.ViewBox(enableMouse=False)
            viewBox.setRange(xRange=[0,self.xRange])
            self.plots[i] = self.ui.plot.addPlot(row=i-self.topPlot, col=0, viewBox=viewBox)
            # count = 0
            # plotChannel = 'Off'
            # for chan in range(0,128):
            #     if format(self.enabledChannels[int(chan/16)],"16b")[15-(chan%16)] == '1':
            #         count = count + 1
            #         if count == i + 1:
            #             plotChannel = chan
            # if i == 99:
            #     self.plots[i].setLabel('left', text='Means')
            # elif i < 99 and i > 95:
            #     self.plots[i].setLabel('left', text='Ramp')
            # else:
            #     self.plots[i].setLabel('left', text="Ch {}".format(plotChannel))
            # self.plots[i].setTitle(title='Ch {}'.format(i), size='10px')
            if i == self.topPlot:
                self.plots[i].setLabel('left', text="Ch {}".format(min(self.chstim, self.chctrl)))
            if i == self.topPlot + 1:
                self.plots[i].setLabel('left', text="Ch {}".format(max(self.chstim, self.chctrl)))

        # need to also replot the data

    @pyqtSlot()
    def updatePlotStream(self):
        if self.data:
            # loop through samples
            for t in range(0, len(self.data)):
                if self.plotPointer == self.xRange:
                    self.plotPointer = 0
                # grab specific sample
                temp = self.data[t]
                # temp = self.data.pop(0) # pop data for sample = 0, 1, 2, ...
                # for ch in range(0, 2):
                #     self.dataPlot[ch][self.plotPointer] = temp[ch]
                # self.dataPlot[ch][self.plotPointer] = temp.pop(0) # pop data for channel = 0, 1, 2, ...
                if self.chorder == 1:
                    self.dataPlot[0][self.plotPointer] = temp[0] & 0x7FFF
                    self.dataPlot[1][self.plotPointer] = temp[1]
                else:
                    self.dataPlot[0][self.plotPointer] = temp[0]
                    self.dataPlot[1][self.plotPointer] = temp[1] & 0x7FFF
                
                # print("{}".format(self.mag_dataA))
                if self.plotPointer > 2**(self.fftsize + 3):
                    self.dataPlot[2][self.plotPointer - 2**(self.fftsize + 3) - 1] = self.mag_dataA
                    self.dataPlot[3][self.plotPointer - 2**(self.fftsize + 3) - 1] = self.mag_dataB
                else:
                    self.dataPlot[2][self.plotPointer + self.xRange - 2**(self.fftsize + 3)-1] = self.mag_dataA
                    self.dataPlot[3][self.plotPointer + self.xRange - 2**(self.fftsize + 3)-1] = self.mag_dataB
                # self.dataPlot[2][self.plotPointer] = temp[2]
                # self.dataPlot[3][self.plotPointer] = temp[2]
                # self.dataPlot[4][self.plotPointer] = temp[4]
                # self.dataPlot[2][self.plotPointer] = temp[1]
                self.plotPointer += 1
            self.data = []

            # TODO: scale all y axes together? turn off auto-scale?

        # for ch in range(self.topPlot, self.topPlot + self.numPlotsDisplayed): # only plot currently displayed plots
        for ch in range(0, self.numPlotsDisplayed):
            if ch < 5:
                dp = self.dataPlot[ch][0:self.xRange]
                # add back in to test new autorange

                # fft = scipy.fft(dp)
                # bp = fft[:]
                # for i in range(len(bp)):
                #     if i in notch or i > 240 or i < 1:
                #         bp[i] = 0
                # dp = np.real(scipy.ifft(bp))

                # if ch == 1:
                #     dp = signal.filtfilt(self.b, self.a, dp)
                #     dp = signal.filtfilt(self.c, self.d, dp)
                #     dp = signal.filtfilt(self.e, self.f, dp)
                    # diffs = np.diff(dp)
                    # if self.countDown == 0 and (
                    #     self.ui.noise.isChecked() or self.ui.thd.isChecked()) and self.plotPointer > 59 and min(
                    #         diffs[self.plotPointer - 60:self.plotPointer - 40]) < -15:
                    #     if self.plotPointer - 40 < self.lastPulse:
                    #         bpm = round(60 * 1000 / ((self.xRange + self.plotPointer - 40) - self.lastPulse))
                    #     else:
                    #         bpm = round(60 * 1000 / (self.plotPointer - 40 - self.lastPulse))
                    #     if bpm < 120 and bpm > 40:
                    #         print('BPM = {}'.format(bpm))
                    #         self.lastPulse = self.plotPointer - 40
                    #         self.countDown = 4
                    #         if self.ui.thd.isChecked():
                    #             self.pulseStim.emit()
                # elif ch == 2:
                #     dp = signal.filtfilt(self.b, self.a, dp)
                #     dp = signal.filtfilt(self.c, self.d, dp)
                #     dp = signal.filtfilt(self.e, self.f, dp)
                #     dp = np.diff(dp)

                #     if self.countDown == 0 and (self.ui.noise.isChecked() or self.ui.thd.isChecked()) and self.plotPointer > 59 and min(dp[self.plotPointer - 60:self.plotPointer-40]) < -15:
                #         if self.plotPointer - 40 < self.lastPulse:
                #             bpm = round(60 * 1000 / ((self.xRange + self.plotPointer - 40) - self.lastPulse))
                #         else:
                #             bpm = round(60 * 1000 / (self.plotPointer - 40 - self.lastPulse))
                #         if bpm < 120 and bpm > 40:
                #             print('BPM = {}'.format(bpm))
                #             self.lastPulse = self.plotPointer - 40
                #             self.countDown = 4
                #             if self.ui.thd.isChecked():
                #                 self.pulseStim.emit()
                if len(dp) != 0:
                    avg = np.mean(dp)
                    sd = np.std(dp)
                    if sd < 10:
                        sd = 10

                # # formatting the data for neural/accelerometer channels
                # if ch > 95:
                #     # accelerometer data, 2's complement
                #     dp = (dp + 2**15) % 2**16 - 2**15
                # else:
                #     # neural data, sign + magnitude
                #     if dp & 2**15:
                #         # negative
                #         dp = -(dp & 0x7FFF)

                self.plots[self.topPlot+ch].clear()
                # self.fftPlots[ch].clear()
                if self.plotEn[self.topPlot+ch]:
                    # if ch == 2:
                    #     freq = list(range(0,len(dp)))
                    #     for i in range(0,len(dp)):
                    #         freq[i] = freq[i]*1000/(2*len(dp))
                    #     # for i in range(0,len(dp)):
                    #     #     dp[i] = 10*np.log10(dp[i])
                    #     if len(dp) != 0:
                    #         dp[0]=0
                    #     self.plots[self.topPlot+ch].plot(x=freq, y=dp, pen=self.plotColors[self.topPlot+ch])
                    #     # self.plots[self.topPlot+ch].plot(y=dp, pen=self.plotColors[self.topPlot+ch])
                    #     # add back in to test new autorange
                    #     self.plots[self.topPlot+ch].getViewBox().setMouseEnabled(x=True, y=True)
                    #     self.plots[self.topPlot+ch].getViewBox().setMouseMode(self.plots[self.topPlot+ch].getViewBox().RectMode)

                    #     self.plots[self.topPlot+ch].getViewBox().setLimits(xMin=0, xMax=500, yMin=0, yMax=20000000)
                    A = list(range(0,len(dp)))
                    B = list(range(0,len(dp)))
                    for i in range(0,len(dp)):
                        if self.signA == 0:
                            A[i] = self.threshA*64
                        else:
                            A[i] = -self.threshA*64
                        if self.signB == 0:
                            B[i] = self.threshB*64
                        else:
                            B[i] = -self.threshB*64
                    if ch == 2 or ch == 3:
                        self.plots[self.topPlot+ch].plot(y=dp, pen=self.plotColors[self.topPlot+ch])
                        # self.plots[self.topPlot+ch].plot(y=dp, pen=self.plotColors[self.topPlot+ch])
                        self.plots[self.topPlot+ch].getViewBox().setMouseEnabled(x=True, y=True)
                        self.plots[self.topPlot+ch].getViewBox().setMouseMode(self.plots[self.topPlot+ch].getViewBox().RectMode)
                        if self.derivative == 0:
                            if ch == 2:
                                self.plots[self.topPlot+ch].plot(y=A)
                                self.plots[self.topPlot+ch].getViewBox().setLimits(xMin=0, xMax=self.xRange, yMin=0, yMax=2*self.threshA*64)
                                self.plots[self.topPlot+ch].getViewBox().setRange(yRange=(0,2*self.threshA*64),update=True)
                        if self.derivativeB == 0:
                            if ch == 3:
                                self.plots[self.topPlot+ch].plot(y=B)
                                self.plots[self.topPlot+ch].getViewBox().setLimits(xMin=0, xMax=self.xRange, yMin=0, yMax=2*self.threshB*64)
                                self.plots[self.topPlot+ch].getViewBox().setRange(yRange=(0,2*self.threshB*64),update=True)
                    else:
                        self.plots[self.topPlot+ch].plot(y=dp, pen=self.plotColors[self.topPlot+ch])
                        # add back in to test new autorange
                        self.plots[self.topPlot+ch].getViewBox().setMouseEnabled(x=True, y=True)
                        self.plots[self.topPlot+ch].getViewBox().setMouseMode(self.plots[self.topPlot+ch].getViewBox().RectMode)
                        self.plots[self.topPlot+ch].getViewBox().setLimits(xMin=0, xMax=self.xRange, yMin=0, yMax=32768)
                        self.plots[self.topPlot+ch].getViewBox().setRange(yRange=(avg-(sd*2),avg+(sd*2)),update=True)
                    if self.ui.autorange.isChecked():
                        # if ch > 0:
                        #     self.plots[ch].getViewBox().autoRange()
                        if ch != 2 and ch != 3:
                            self.plots[self.topPlot+ch].getViewBox().autoRange()
                            # self.fftPlots[ch].plot(y=calculateFFT(dp), pen=(102,204,255))
                            # if self.ui.autorange.isChecked():
                            # self.fftPlots[ch].getViewBox().autoRange()

                            # TODO: add FFT plotting + a way to enable/disable channels
            
