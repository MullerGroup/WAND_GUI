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

class omni_data(IsDescription):
    # data = UInt16Col(shape=(1,64))
    # data = UInt16Col(shape=(1,96))
    # 96 neural channels, 3 accelerometer channels
    data = UInt16Col(shape=(1,99))
    time = StringCol(26)


# TODO: FFT output doesn't look correct
def calculateFFT(d):
    fft = np.abs(np.fft.rfft(d, n=100)) # 100 point FFT - change to be based on xRange?
    return fft

class DataVisualizer(QDockWidget):
    readAdc = pyqtSignal(int)
    streamAdc = pyqtSignal()
    testCommOn = pyqtSignal()
    testCommOff = pyqtSignal()

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
        self.numPlots = 99
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
        self.connect(self.streamAdcThread, SIGNAL('streamDataOut(PyQt_PyObject)'), self.streamAdcData)

        # hdf5 data storage
        # TODO: add save file text box
        # self.saveFile = tables.open_file("test.hdf", mode="w", title="Test")
        # self.dataGroup = self.saveFile.create_group("/", name='dataGroup', title='Recorded Data Group')
        # self.dataTable = self.saveFile.create_table(self.dataGroup, name='dataTable', title='Recorded Data Table', description=omni_data)

        self.file = open('gui_data.csv','w')
        self.csvfile = csv.writer(self.file)

        self.setWindowTitle("Data Visualizer")

        # populate arrays
        for i in range(0,self.numPlots):
            self.plots.append(pg.PlotItem().plot())
            self.plotEn.append(True)
            self.plotColors.append(pg.intColor(i%16,16))

        self.updatePlotDisplay()

        # every time the # of bands changes, update the band selection boxes
        # self.ui.numBands.currentIndexChanged.connect(self.updateBands)

        self.ui.autorange.clicked.connect(self.updatePlot)
        self.ui.numPlotsDisplayed.currentIndexChanged.connect(self.updatePlotDisplay)
        self.ui.xRange.valueChanged.connect(self.updatePlotDisplay)
        self.ui.clearBtn.clicked.connect(self.clearPlots)

        # set some defaults
        # self.ui.numBands.setCurrentIndex(0)
        self.ui.autorange.setChecked(True)
        self.ui.plotEn.setChecked(True)
        # self.updateBands()

    @pyqtSlot()
    def streamingDone(self):
        self.ui.singleBtn.setEnabled(True)

    def setWorker(self, w):
        self.testCommOn.connect(w.testCommOn)
        self.testCommOff.connect(w.testCommOff)
        self.readAdc.connect(w.readAdc)
        w.adcData.connect(self.adcData)
        w.updateChannels.connect(self.updateChannels)

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
        if self.ui.saveEn.isChecked():
            self.saveData()
        if self.ui.plotEn.isChecked():
            self.updatePlot()

    @pyqtSlot(list)
    def streamAdcData(self, data):
        global t_start
        t_start = datetime.now()
        self.data = data
        if self.ui.plotEn.isChecked():
            self.updatePlot()

    @pyqtSlot()
    def on_singleBtn_clicked(self):

        # add in save file dialog
        if self.ui.saveEn.isChecked():
            filt = 'CSV files (*.csv);;All files (*.*)'
            self.file = QtGui.QFileDialog.getSaveFileName(parent=self,
                                                   caption="Select File",
                                                   filter=filt)
            self.fn = open(self.file, 'w')
            self.csvfile = csv.writer(self.fn)
        self.readAdc.emit(self.ui.samples.value())

    @pyqtSlot()
    def on_streamBtn_clicked(self):
        if self.ui.streamBtn.isChecked():
            self.streamAdcThread.start()
            self.ui.singleBtn.setDisabled(True)
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
    # def saveData(self):
    #     for sample in range(0,len(self.data)):
    #         #Creates a row in the data table for a sample
    #         data_point = self.dataTable.row
    #         #Sets the time of the beginning of the sample
    #         t_elapsed = datetime.now()
    #         #The following three lines add values into the row of the data table for this sample
    #         #Start of the data of sample, t_start set in streamAdcdata(self, data)
    #         data_point['start of data'] = t_start
    #         #time since the start of the data is the difference between t_elapsed and t_start
    #         data_point['time since start of data'] = str(int(t_elapsed.day) - int(data_point['start of sample'].day)) + ' days ' + str(int(t_elapsed.hour) - int(data_point['start of sample'].hour)) + ' hours ' + str(int(t_elapsed.minute) - int(data_point['start of sample'].minute)) + ' minutes ' + str(int(t_elapsed.second) - int(data_point['start of sample'].second)) + ' seconds'
    #         #Adds the data into the row of the data table for this sample
    #         data_point['data'] = self.data[sample]
    #         data_point.append()
    #     self.dataTable.flush

    def saveData(self):
        for sample in range(0, len(self.data)):
            self.csvfile.writerow(self.data[sample])

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

            self.plots[i].setLabel('left', text="Ch {}".format(plotChannel))
            # self.plots[i].setTitle(title='Ch {}'.format(i), size='10px')

#TODO: implement fft plotting. Can place plots in col=1

        # need to also replot the data
        self.updatePlot()

    @pyqtSlot()
    def updatePlot(self):

# TODO: plotted data is lost when updatePlot is called and there is no new data. Need to remove the return statement and always replot stored data array(s)

#TODO: plotting crashes when decreasing x-axis range
        # if not self.data:
        #     return

        noisedata = []


        if self.data:
            # creates structure of arrays indexed by channel first, then sample
            for ch in range(0, self.numPlots):
                # data.append((np.array([i[ch] for i in self.data])-32768/2)*(100e-3/32768)*1e6)
                noisedata.append((np.array([i[ch] for i in self.data])))

            for ch in range(0, self.numPlots):
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

                if self.ui.thd.isChecked():
                    d = noisedata[ch]

                    indx = 11
                    dfft = np.abs(np.fft.fft(d))
                    fund = dfft[indx]
                    dist = 0
                    for i in range(2, 32):
                        dist += dfft[i * indx] ** 2
                    db =  20 * np.log10(dist ** 0.5 / fund)
                    if ch < 96: print("Ch {} THD: {:0.0f} dB".format(ch,db))

            for t in range(0, len(self.data)):
                if self.plotPointer == self.xRange:
                    self.plotPointer = 0
                temp = self.data[t]
                # temp = self.data.pop(0) # pop data for sample = 0, 1, 2, ...
                for ch in range(0, self.numPlots):
                    self.dataPlot[ch][self.plotPointer] = temp[ch]
                    # self.dataPlot[ch][self.plotPointer] = temp.pop(0) # pop data for channel = 0, 1, 2, ...
                self.plotPointer += 1
            self.data = []

# TODO: scale all y axes together? turn off auto-scale?

        for ch in range(self.topPlot, self.topPlot + self.numPlotsDisplayed): # only plot currently displayed plots
            dp = self.dataPlot[ch][0:self.xRange]

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
                if self.ui.autorange.isChecked():
                    self.plots[ch].getViewBox().autoRange()
                # self.fftPlots[ch].plot(y=calculateFFT(dp), pen=(102,204,255))
                # if self.ui.autorange.isChecked():
                    # self.fftPlots[ch].getViewBox().autoRange()

# TODO: add FFT plotting + a way to enable/disable channels
