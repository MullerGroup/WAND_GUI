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

class omni_data(IsDescription):
    # data = UInt16Col(shape=(1,64))
    # data = UInt16Col(shape=(1,96))
    # 96 neural channels, 3 accelerometer channels
    data = UInt16Col(shape=(1,99))
    time = StringCol(26)

def calculateFFT(d):
    fft = np.abs(np.fft.rfft(d, n=100)) # 100 point FFT - change to be based on xRange?
    return fft

class DataVisualizer(QDockWidget):
    readAdc = pyqtSignal(int)
    streamAdc = pyqtSignal()
    testCommOn = pyqtSignal()
    testCommOff = pyqtSignal()
    setupRecording = pyqtSignal()
    enableArtifact = pyqtSignal()
    disableArtifact = pyqtSignal()
    enableInterpolate = pyqtSignal()
    disableInterpolate = pyqtSignal()

    def __init__(self, parent=None):
        def populate(listbox, start, stop, step):
            for i in range(start,stop+step,step):
                listbox.addItem("{}".format(i))
        super().__init__(parent)
        self.ui = Ui_DataVisualizer()
        self.ui.setupUi(self)
        self.data = []
        # self.numPlots = 64
        # added 3 more channels just to display accel data
        self.numPlots = 100
        self.xRange = self.ui.xRange.value() # number of ms (samples) over which to plot continuous data

        self.dataPlot = np.zeros((self.numPlots, self.ui.xRange.maximum())) # aggregation of data to plot (scrolling style)
        self.plotPointer = 0 # pointer to current x position in plot (for plotting scrolling style)

        self.numPlotsDisplayed = int(self.ui.numPlotsDisplayed.currentText())
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
        # self.connect(self.streamAdcThread, SIGNAL('streamDataOut(PyQt_PyObject)'), self.streamAdcData)

        self.file = open('gui_data.csv','w')
        self.csvfile = csv.writer(self.file)

        self.setWindowTitle("Data Visualizer")

        # populate arrays
        for i in range(0,self.numPlots):
            self.plots.append(pg.PlotItem().plot())
            self.plotEn.append(True)
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
        self.ui.artifactBtn.setEnabled(True)
        self.ui.interpolateBtn.setEnabled(True)

    def setWorker(self, w):
        self.testCommOn.connect(w.testCommOn)
        self.testCommOff.connect(w.testCommOff)
        self.setupRecording.connect(w.setupRecording)
        # self.enableArtifact.connect(w.enableArtifact)
        # self.disableArtifact.connect(w.disableArtifact)
        # self.enableInterpolate.connect(w.enableInterpolate)
        # self.disableInterpolate.connect(w.disableInterpolate)
        self.readAdc.connect(w.readAdc)
        w.adcData.connect(self.adcData)
        w.updateChannels.connect(self.updateChannels)

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

    # @pyqtSlot(list)
    # def streamAdcData(self, data):
    #     global t_start
    #     t_start = datetime.now()
    #     self.data = data
    #     if self.ui.plotEn.isChecked():
    #         self.updatePlot()

    @pyqtSlot()
    def on_singleBtn_clicked(self):
        self.readAdc.emit(self.ui.samples.value())

    @pyqtSlot()
    def on_saveBtn_clicked(self):
        filt = 'CSV files (*.csv);;All files (*.*)'
        self.file = QtGui.QFileDialog.getSaveFileName(parent=self,
                                                      caption="Select File",
                                                      filter=filt)
        self.fn = open(self.file, 'w')
        self.csvfile = csv.writer(self.fn)
        for sample in range(0, len(self.dataPlot)):
            self.csvfile.writerow(self.dataPlot[sample])

    @pyqtSlot()
    def on_streamBtn_clicked(self):
        if self.ui.streamBtn.isChecked():
            self.streamAdcThread.setup(self.ui.dispStream.isChecked(), self.ui.stim.isChecked(), self.ui.ch0.value(), self.ui.ch1.value(), self.ui.ch2.value(), self.ui.ch3.value(), self.ui.stimRep.value(), self.ui.stimDelay.value(), self.ui.artifactBtn.isChecked(), self.ui.interpolateBtn.isChecked(), self.ui.artDelay.value())
            self.streamAdcThread.start()
            self.ui.singleBtn.setDisabled(True)
            self.ui.setupRecordingBtn.setDisabled(True)
            self.ui.artifactBtn.setDisabled(True)
            self.ui.interpolateBtn.setDisabled(True)
        else:
            self.streamAdcThread.stop()

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
        for ch in range(self.topPlot, self.topPlot + self.numPlotsDisplayed):
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

#TODO: plotting crashes when decreasing x-axis range
        # if not self.data:
        #     return

        noisedata = []
        means = []


        if self.data:
            # creates structure of arrays indexed by channel first, then sample
            for ch in range(0, self.numPlots-1):
                # data.append((np.array([i[ch] for i in self.data])-32768/2)*(100e-3/32768)*1e6)
                noisedata.append((np.array([i[ch] for i in self.data])))

            for ch in range(0,95):
                means.append(np.mean(noisedata[ch]))

            for ch in range(0, self.numPlots-1):
                if self.ui.noise.isChecked():
                    d = noisedata[ch]
                    rms = np.std(d)
                    # ff = np.abs(np.fft.fft(d)) / len(d)
                    # ff[0] = 0
                    # # notch out 60 hz harmonics
                    # rms60 = 0
                    # for i in range(1, 5):
                    #     rms60 += ff[60 * i] ** 2
                    #     ff[60 * i] = 0
                    # rms60 **= 0.5
                    # rms = np.sum(ff[0:500] ** 2) ** 0.5
                    if ch < 96: print("Ch {} Noise: {:0.1f} rms".format(ch,rms))
                    #print("{}".format(dp))
                    #print("{:0.1f} rms".format(self.measureRms(dp)))

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
                # temp = self.data.pop(0) # pop data for sample = 0, 1, 2, ...
                for ch in range(0, self.numPlots-1):
                    self.dataPlot[ch][self.plotPointer] = temp[ch]
                    # self.dataPlot[ch][self.plotPointer] = temp.pop(0) # pop data for channel = 0, 1, 2, ...
                self.plotPointer += 1
            self.data = []
            for i in range(0,len(means)):
                self.dataPlot[99][i] = means[i]

        for ch in range(self.topPlot, self.topPlot + self.numPlotsDisplayed): # only plot currently displayed plots
            if ch == 99:
                dp = self.dataPlot[ch][0:95]
                self.plots[ch].clear()
                # self.fftPlots[ch].clear()
                if self.plotEn[ch]:
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

                # # formatting the data for neural/accelerometer channels
                # if ch > 95:
                #     # accelerometer data, 2's complement
                #     dp = (dp + 2**15) % 2**16 - 2**15
                # else:
                #     # neural data, sign + magnitude
                #     if dp & 2**15:
                #         # negative
                #         dp = -(dp & 0x7FFF)

                self.plots[ch].clear()
                # self.fftPlots[ch].clear()
                if self.plotEn[ch]:
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
                    # self.fftPlots[ch].plot(y=calculateFFT(dp), pen=(102,204,255))
                    # if self.ui.autorange.isChecked():
                        # self.fftPlots[ch].getViewBox().autoRange()

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
                self.dataPlot[0][self.plotPointer] = temp[0]
                self.dataPlot[1][self.plotPointer] = temp[1]
                self.dataPlot[2][self.plotPointer] = temp[2]
                self.dataPlot[3][self.plotPointer] = temp[3]
                # self.dataPlot[2][self.plotPointer] = temp[1]
                self.plotPointer += 1
            self.data = []

            # TODO: scale all y axes together? turn off auto-scale?

        # for ch in range(self.topPlot, self.topPlot + self.numPlotsDisplayed): # only plot currently displayed plots
        for ch in range(0, 4):
            if ch < 4:
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

                self.plots[ch].clear()
                # self.fftPlots[ch].clear()
                if self.plotEn[ch] and ch < 4:
                    if ch == 0 or ch == 2:
                        # self.plots[ch].plot(y=(dp * (0.00305))-50, pen=self.plotColors[ch])  # different color for each plot
                        self.plots[ch].plot(y=dp, pen=self.plotColors[ch])
                    else:
                        # self.plots[ch].plot(y=dp*(0.00305), pen=self.plotColors[ch]) # different color for each plot
                        self.plots[ch].plot(y=dp, pen=self.plotColors[ch])
                    # add back in to test new autorange
                    self.plots[ch].getViewBox().setMouseEnabled(x=True, y=True)
                    self.plots[ch].getViewBox().setMouseMode(self.plots[ch].getViewBox().RectMode)
                    if ch == 1:
                        self.plots[ch].getViewBox().setLimits(xMin=0, xMax=self.xRange, yMin=-32768, yMax=32768)
                        self.plots[ch].getViewBox().setRange(yRange=(avg-(20),avg+(20)),update=True)
                    elif ch == 2:
                        self.plots[ch].getViewBox().setLimits(xMin=0, xMax=self.xRange, yMin=-32768, yMax=32768)
                        self.plots[ch].getViewBox().setRange(yRange=(avg-(20),avg+(20)),update=True)
                    else:
                        self.plots[ch].getViewBox().setLimits(xMin=0, xMax=self.xRange, yMin=-32768, yMax=32768)
                        self.plots[ch].getViewBox().setRange(yRange=(avg-(20),avg+(20)),update=True)
                    if self.ui.autorange.isChecked():
                        # if ch > 0:
                        #     self.plots[ch].getViewBox().autoRange()
                        self.plots[ch].getViewBox().autoRange()
                        # self.fftPlots[ch].plot(y=calculateFFT(dp), pen=(102,204,255))
                        # if self.ui.autorange.isChecked():
                        # self.fftPlots[ch].getViewBox().autoRange()

                        # TODO: add FFT plotting + a way to enable/disable channels