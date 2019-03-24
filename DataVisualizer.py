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

class DataVisualizer(QDockWidget):
    readAdc = pyqtSignal(int)
    streamAdc = pyqtSignal()
    testCommOn = pyqtSignal()
    testCommOff = pyqtSignal()
    setupRecording = pyqtSignal()
    setupStim = pyqtSignal()
    enableArtifact = pyqtSignal()
    disableArtifact = pyqtSignal()
    enableInterpolate = pyqtSignal()
    disableInterpolate = pyqtSignal()
    regFile = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DataVisualizer()
        self.ui.setupUi(self)

        self.data = []
        self.numPlots = 4
        self.xRange = self.ui.xRange.value() # number of ms (samples) over which to plot continuous data

        self.dataPlot = np.zeros((self.numPlots, self.ui.xRange.maximum())) # aggregation of data to plot (scrolling style)
        self.plotPointer = 0 # pointer to current x position in plot (for plotting scrolling style)

        self.plots = [] # stores pyqtgraph objects
        self.plotColors = []

        # initialize streaming mode thread
        self.streamAdcThread = cmbackend.streamAdcThread()
        self.connect(self.streamAdcThread, SIGNAL("finished()"), self.streamingDone)
        self.streamAdcThread.streamAdcData.connect(self.streamAdcData)

        self.setWindowTitle("Data Visualizer")

        # populate arrays
        for i in range(0,self.numPlots):
            self.plots.append(pg.PlotItem().plot())
            self.plotColors.append(pg.intColor(i%16,16))

        self.updatePlotDisplay()

        self.ui.autorange.clicked.connect(self.updatePlot)
        self.ui.numPlotsDisplayed.currentIndexChanged.connect(self.updatePlotDisplay)
        self.ui.xRange.valueChanged.connect(self.updatePlotDisplay)
        self.ui.clearBtn.clicked.connect(self.clearPlots)

        # set some defaults
        self.ui.autorange.setChecked(True)

    @pyqtSlot()
    def streamingDone(self):
        self.ui.singleBtn.setEnabled(True)
        self.ui.setupRecordingBtn.setEnabled(True)
        self.ui.setupStimBtn.setEnabled(True)
        if not self.ui.interpolateBtn.isChecked():
            self.ui.artifactBtn.setEnabled(True)
        if not self.ui.artifactBtn.isChecked():
            self.ui.interpolateBtn.setEnabled(True)

    def setWorker(self, w):
        self.testCommOn.connect(w.testCommOn)
        self.testCommOff.connect(w.testCommOff)
        self.setupRecording.connect(w.setupRecording)
        self.setupStim.connect(w.setupStim)
        # self.enableArtifact.connect(w.enableArtifact)
        # self.disableArtifact.connect(w.disableArtifact)
        # self.enableInterpolate.connect(w.enableInterpolate)
        # self.disableInterpolate.connect(w.disableInterpolate)
        self.readAdc.connect(w.readAdc)
        self.regFile.connect(w.regFile)
        w.adcData.connect(self.adcData)
        w.updateChannels.connect(self.updateChannels)

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

    @pyqtSlot(list)
    def adcData(self, data):
        global t_start
        t_start = datetime.now()
        self.data = data
        self.updatePlot()

    @pyqtSlot(list)
    def streamAdcData(self, data):
        self.data = data
        self.updatePlotStream()

    @pyqtSlot()
    def on_streamBtn_clicked(self):
        if self.ui.streamBtn.isChecked():
            print("stream started with nmStim value  {}".format(self.ui.stimOnNM.currentIndex()))
            self.streamAdcThread.setup(self.ui.dispStream.isChecked(), self.ui.stim.isChecked(), self.ui.ch0.value(), self.ui.ch1.value(), self.ui.ch2.value(), self.ui.ch3.value(), self.ui.stimRep.value(), self.ui.stimDelay.value(), self.ui.artifactBtn.isChecked(), self.ui.interpolateBtn.isChecked(), self.ui.artDelay.value(), self.ui.stimOnNM.currentIndex(), self.ui.impStart.isChecked(), self.ui.impDelay.value())
            self.streamAdcThread.start()
            self.ui.singleBtn.setDisabled(True)
            self.ui.setupRecordingBtn.setDisabled(True)
            self.ui.setupStimBtn.setDisabled(True)
            self.ui.artifactBtn.setDisabled(True)
            self.ui.interpolateBtn.setDisabled(True)
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
    def on_setupRecordingBtn_clicked(self):
        self.setupRecording.emit()

    @pyqtSlot()
    def on_setupStimBtn_clicked(self):
        self.setupStim.emit()


    @pyqtSlot()
    def on_artifactBtn_clicked(self):
        if self.ui.artifactBtn.isChecked():
            # self.enableArtifact.emit()
            self.ui.interpolateBtn.setDisabled(True)
        else:
            # self.disableArtifact.emit()
            self.ui.interpolateBtn.setEnabled(True)


    @pyqtSlot()
    def on_interpolateBtn_clicked(self):
        if self.ui.interpolateBtn.isChecked():
            # self.enableInterpolate.emit()
            self.ui.artifactBtn.setDisabled(True)
        else:
            # self.disableInterpolate.emit()
            self.ui.artifactBtn.setEnabled(True)

    @pyqtSlot()
    def clearPlots(self):
        self.plotPointer = 0
        self.dataPlot = np.zeros(
            (self.numPlots, self.ui.xRange.maximum()))  # aggregation of data to plot (scrolling style)
        for ch in range(0, self.numPlotsDisplayed):
            self.plots[ch].clear()

    @pyqtSlot()
    def updatePlotDisplay(self):
        for j in reversed(range(0,self.numPlotsDisplayed)):
            plotToDelete = self.ui.plot.getItem(j,0)
            if plotToDelete is not None:
                self.ui.plot.removeItem(plotToDelete)

        self.numPlotsDisplayed = int(self.ui.numPlotsDisplayed.currentText())
        self.xRange = self.ui.xRange.value()
        if self.topPlot+self.numPlotsDisplayed > self.numPlots:
            self.topPlot = self.numPlots - self.numPlotsDisplayed
        for i in range(self.topPlot, self.topPlot + self.numPlotsDisplayed):
            viewBox = pg.ViewBox(enableMouse=False)
            viewBox.setRange(xRange=[0,self.xRange])
            self.plots[i] = self.ui.plot.addPlot(row=i-self.topPlot, col=0, viewBox=viewBox)
            count = 0
            plotChannel = 'Off'
            for chan in range(0,128):
                if format(self.enabledChannels[int(chan/16)],"16b")[15-(chan%16)] == '1':
                    count = count + 1
                    if count == i + 1:
                        plotChannel = chan
            if i == 99:
                self.plots[i].setLabel('left', text='Means')
            elif i < 99 and i > 95:
                self.plots[i].setLabel('left', text='Ramp')
            else:
                self.plots[i].setLabel('left', text="Ch {}".format(plotChannel))
            # self.plots[i].setTitle(title='Ch {}'.format(i), size='10px')

        # need to also replot the data
        self.updatePlot()

    @pyqtSlot()
    def updatePlot(self):
        noisedata = []
        means = []
        good_ch = 0

        if self.data:
            # creates structure of arrays indexed by channel first, then sample
            for ch in range(0, self.numPlots-1):
                noisedata.append((np.array([i[ch] for i in self.data])))

            for ch in range(0,95):
                means.append(np.mean(noisedata[ch]))

            for ch in range(0,95):
                if means[ch] < ((2**15) - self.ui.thresh.value()) and means[ch] > self.ui.thresh.value():
                    good_ch = good_ch + 1
                    print(ch)
            print(good_ch)
            print(self.ui.thresh.value())

            for ch in range(0, self.numPlots-1):
                if self.ui.noise.isChecked():
                    d = noisedata[ch]
                    rms = np.std(d)

                    if ch < 96: print("Ch {} Noise: {:0.1f} rms".format(ch,rms))


                    indx = 11
                    dfft = np.abs(np.fft.fft(d))
                    fund = dfft[indx]
                    dist = 0
                    for i in range(2, 32):
                        dist += dfft[i * indx] ** 2
                    db = 20 * np.log10(dist ** 0.5 / fund)
                    if ch < 96: print("Ch {} THD: {:0.0f} dB".format(ch, db))


            for t in range(0, len(self.data)):
                if self.plotPointer == self.xRange:
                    self.plotPointer = 0
                temp = self.data[t]
                for ch in range(0, self.numPlots-1):
                    self.dataPlot[ch][self.plotPointer] = temp[ch]
                self.plotPointer += 1
            self.data = []
            for i in range(0,len(means)):
                self.dataPlot[99][i] = means[i]

        for ch in range(self.topPlot, self.topPlot + self.numPlotsDisplayed): # only plot currently displayed plots
            if ch == 99:
                dp = self.dataPlot[ch][0:95]
                self.plots[ch].clear()
                self.plots[ch].plot(y=dp, pen=self.plotColors[ch])  # different color for each plot
                self.plots[ch].getViewBox().setLimits(xMin=0, xMax=95, yMin=-100, yMax=32868)
                self.plots[ch].getViewBox().setRange(yRange=(-100, 32868), update=True)
            else:
                dp = self.dataPlot[ch][0:self.xRange]
                # add back in to test new autorange
                avg = np.mean(dp)
                sd = np.std(dp)
                if sd < 10:
                    sd = 10

                self.plots[ch].clear()
                self.plots[ch].plot(y=dp, pen=self.plotColors[ch]) # different color for each plot
                # add back in to test new autorange
                self.plots[ch].getViewBox().setMouseEnabled(x=True,y=True)
                self.plots[ch].getViewBox().setMouseMode(self.plots[ch].getViewBox().RectMode)
                if ch < 99 and ch > 95:
                    self.plots[ch].getViewBox().setLimits(xMin=0,xMax=self.xRange,yMin=-100,yMax=65636)
                else:
                    self.plots[ch].getViewBox().setLimits(xMin=0, xMax=self.xRange, yMin=-100, yMax=32868)
                self.plots[ch].getViewBox().setRange(yRange=(avg-(2.5*sd),avg+(2.5*sd)),update=True)
                if self.ui.autorange.isChecked():
                    self.plots[ch].getViewBox().autoRange()

    @pyqtSlot()
    def updatePlotStream(self):
        if self.data:
            # loop through samples
            for t in range(0, len(self.data)):
                if self.plotPointer == self.xRange:
                    self.plotPointer = 0
                # grab specific sample
                temp = self.data[t]
                self.dataPlot[0][self.plotPointer] = temp[0]
                self.dataPlot[1][self.plotPointer] = temp[1]
                self.dataPlot[2][self.plotPointer] = temp[2]
                self.dataPlot[3][self.plotPointer] = temp[3]
                self.plotPointer += 1
            self.data = []

        for ch in range(0, 4):
            if ch < 4:
                dp = self.dataPlot[ch][0:self.xRange]

                avg = np.mean(dp)
                sd = np.std(dp)
                if sd < 10:
                    sd = 10

                self.plots[ch].clear()
                if ch < 4:
                    if ch == 0 or ch == 2:
                        self.plots[ch].plot(y=dp, pen=self.plotColors[ch])
                    else:
                        self.plots[ch].plot(y=dp, pen=self.plotColors[ch])
                    # add back in to test new autorange
                    self.plots[ch].getViewBox().setMouseEnabled(x=True, y=True)
                    self.plots[ch].getViewBox().setMouseMode(self.plots[ch].getViewBox().RectMode)
                    if ch == 1:
                        self.plots[ch].getViewBox().setLimits(xMin=0, xMax=self.xRange, yMin=-32768, yMax=32768)
                        self.plots[ch].getViewBox().setRange(yRange=(avg-(sd*2),avg+(sd*2)),update=True)
                    elif ch == 2:
                        self.plots[ch].getViewBox().setLimits(xMin=0, xMax=self.xRange, yMin=-32768, yMax=32768)
                        self.plots[ch].getViewBox().setRange(yRange=(avg-(sd*2),avg+(sd*2)),update=True)
                    else:
                        self.plots[ch].getViewBox().setLimits(xMin=0, xMax=self.xRange, yMin=-32768, yMax=32768)
                        self.plots[ch].getViewBox().setRange(yRange=(avg-(sd*2),avg+(sd*2)),update=True)
                    if self.ui.autorange.isChecked():
                        self.plots[ch].getViewBox().autoRange()