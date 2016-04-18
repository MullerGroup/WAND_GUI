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
    data = UInt16Col(shape=(1,2))
    time = StringCol(26)


# TODO: FFT output doesn't look correct
def calculateFFT(d):
    fft = np.abs(np.fft.rfft(d, n=100)) # 100 point FFT - change to be based on xRange?
    return fft

class DataVisualizer(QDockWidget):
    readAdc = pyqtSignal(int)
    streamAdc = pyqtSignal()
    setStreamBool = pyqtSignal(bool)

    def __init__(self, parent=None):
        def populate(listbox, start, stop, step):
            for i in range(start,stop+step,step):
                listbox.addItem("{}".format(i))
        super().__init__(parent)
        self.ui = Ui_DataVisualizer()
        self.ui.setupUi(self)
        self.data = []
        self.numPlots = 64
        self.xRange = self.ui.xRange.value() # number of ms (samples) over which to plot continuous data

        self.dataPlot = np.zeros((self.numPlots, self.ui.xRange.maximum())) # aggregation of data to plot (scrolling style)
        self.plotPointer = 0 # pointer to current x position in plot (for plotting scrolling style)

        self.numPlotsDisplayed = int(self.ui.numPlotsDisplayed.currentText())
        self.plots = [] # stores pyqtgraph objects
        self.topPlot = 0 # which channel to begin display w/ (used for scrolling through plots)
        self.fftPlots = []
        self.plotEn = [] # each plot can be enabled/disabled by pressing spacebar on top of it
        self.plotColors = []

        self.streamEn = False

        # hdf5 data storage
        # TODO: add save file text box + checkbox on GUI
        self.saveFile = tables.open_file("test.hdf", mode="w", title="Test")
        self.dataGroup = self.saveFile.create_group("/", name='dataGroup', title='Recorded Data Group')
        self.dataTable = self.saveFile.create_table(self.dataGroup, name='dataTable', title='Recorded Data Table', description=omni_data)

        self.setWindowTitle("Data Visualizer")

        # populate arrays
        for i in range(0,self.numPlots):
            self.plots.append(pg.PlotItem().plot())
            self.plotEn.append(True)
            self.plotColors.append(pg.intColor(i%16,16))

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
        self.ui.numPlotsDisplayed.currentIndexChanged.connect(self.updatePlotDisplay)
        self.ui.xRange.valueChanged.connect(self.updatePlotDisplay)
        self.ui.clearBtn.clicked.connect(self.clearPlots)

        # set some defaults
        # self.ui.numBands.setCurrentIndex(0)
        self.ui.autorange.setChecked(True)
        self.ui.plotEn.setChecked(True)
        # self.updateBands()

    def setWorker(self, w):
        self.readAdc.connect(w.readAdc)
        w.adcData.connect(self.adcData)
        self.streamAdc.connect(w.streamAdc)
        self.setStreamBool.connect(w.setStreamBool)
        w.streamAdcData.connect(self.streamAdcData)

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

# TODO: add labels on GUI to explain how to scroll around plots
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

    @pyqtSlot(list)
    def adcData(self, data):
        self.data = data
        if self.ui.saveEn.isChecked():
            self.saveData()
        if self.ui.plotEn.isChecked():
            self.updatePlot()
        # if self.ui.streamBtn.isChecked():
        #     try:
        #         self.on_singleBtn_clicked()
        #         # QTimer.singleShot(self.ui.samples.value(), self.on_singleBtn_clicked())
        #     except:
        #         pass # used to suppress "error" message from singleShot
            #TODO: data acquisition/plotting stops if UART doesn't receive all bytes - it should just continue after the failed read?

    @pyqtSlot(list)
    def streamAdcData(self, data):
        self.data = data
        if self.ui.saveEn.isChecked():
            self.saveData()
        if self.ui.plotEn.isChecked():
            self.updatePlot()

    @pyqtSlot()
    def on_singleBtn_clicked(self):
        self.readAdc.emit(self.ui.samples.value())

    @pyqtSlot()
    def on_streamBtn_clicked(self):
        print("clicked stream btn")
        self.streamEn = self.ui.streamBtn.isChecked()
        print("DataVis.streamEn = {}".format(self.streamEn))
        self.setStreamBool.emit(self.streamEn)
        print("emitted setStreamBool")
        if self.streamEn:
            self.streamAdc.emit()
            print("emitted streamAdc")

    def saveData(self):
        for sample in range(0,len(self.data)):
            data_point = self.dataTable.row
            data_point['time'] = str(datetime.now())
            data_point['data'] = self.data[sample]
            data_point.append()
        self.dataTable.flush

# # appends new data to hdf5 file
#     def saveData(self):
#         old_size = self.h5Data.shape[1]
#         new_size = old_size+len(self.data)
#         self.h5Data.resize((self.numPlots,new_size))
#         for sample in range(0,self.ui.samples.value()): # TODO: change samples.value() to len(self.data[0]) ?
#             for ch in range(0,self.numPlots):
#                 self.h5Data[ch,old_size+sample] = self.data[sample][ch]

    @pyqtSlot()
    def clearPlots(self):
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
            self.plots[i].setLabel('left', text="Ch {}".format(i))
            # self.plots[i].setTitle(title='Ch {}'.format(i), size='10px')

#TODO: implement fft plotting. Can place plots in col=1

        # need to also replot the data
        self.updatePlot()

    @pyqtSlot()
    def updatePlot(self):

# TODO: plotted data is lost when updatePlot is called and there is no new data. Need to remove the return statement and always replot stored data array(s)

#TODO: button to clear plots
#TODO: checkboxes for plotting/saving/both
        if not self.data:
            return
        if self.data:
            for t in range(0, len(self.data)):
                if self.plotPointer == self.xRange:
                    self.plotPointer = 0
                temp = self.data[t]
                # temp = self.data.pop(0) # pop data for sample = 0, 1, 2, ...
                for ch in range(0, self.numPlots):
                    self.dataPlot[ch][self.plotPointer] = temp[ch]
                    # self.dataPlot[ch][self.plotPointer] = temp.pop(0) # pop data for channel = 0, 1, 2, ...
                self.plotPointer += 1

# TODO: scale all y axes together? turn off auto-scale?

        for ch in range(self.topPlot, self.topPlot + self.numPlotsDisplayed): # only plot currently displayed plots
            dp = self.dataPlot[ch][0:self.xRange]
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
