from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.ui_DataVisualizer import Ui_DataVisualizer
import numpy as np
import scipy.io

def measureDist(d):
    indx = 11
    dfft = np.abs(np.fft.fft(d))
    fund = dfft[indx]
    dist = 0
    for i in range(2,32):
        dist += dfft[i*indx]**2
    return 20*np.log10(dist**0.5/fund)

def measureRms(d):
    ff = np.abs(np.fft.fft(d))/len(d)
    ff[0] = 0
    # notch out 60 hz harmonics
    rms60 = 0
    for i in range(1,5):
        rms60 += ff[60*i]**2
        ff[60*i] = 0
    rms60 **= 0.5
    rms = np.sum(ff[0:500]**2)**0.5
    # print("RMS: {}   60 Hz: {}".format(rms, rms60))
    #rms_full = np.std(d)
    #print("RMS: {}".format(rms_full))
    return rms

def calculateFFT(d):
    fft = np.abs(np.fft.rfft(d, n=100)) # 100 point FFT
    return fft

class DataVisualizer(QDockWidget):
    readAdc = pyqtSignal(int, int)

    def __init__(self, parent=None, nm=0):
        def populate(listbox):
            for i in range(0,64):
                listbox.addItem("{}".format(i))
        super().__init__(parent)
        self.nm = nm
        self.ui = Ui_DataVisualizer()
        self.ui.setupUi(self)
        self.data = []
        self.lastfile = ""
        self.numPlots = 64
        self.plots = []

        # for i in range(0,self.numPlots)
        #     self.plotCh[i] = self.ui.
        self.plotCh = [self.ui.chanA, self.ui.chanB, self.ui.chanC, self.ui.chanD]
        self.plotEn = [self.ui.plotA, self.ui.plotB, self.ui.plotC, self.ui.plotD]
        self.plotLbl = [(self.ui.chA_rms, self.ui.chA_thd), (self.ui.chB_rms, self.ui.chB_thd),
                        (self.ui.chC_rms, self.ui.chC_thd), (self.ui.chD_rms, self.ui.chD_thd)]
        for i in range(0,self.numPlots):
            self.plots.append(self.ui.plot.addPlot())
            self.ui.plot.nextRow()
            self.plotEn[i].clicked.connect(self.updatePlot)
            populate(self.plotCh[i])
            self.plotCh[i].currentIndexChanged.connect(self.updatePlot)
        self.ui.autorange.clicked.connect(self.updatePlot)
        self.ui.plotrms.clicked.connect(self.updatePlot)
        self.ui.plotmean.clicked.connect(self.updatePlot)
        self.ui.plotTHD.clicked.connect(self.updatePlot)

    def setWorker(self, w):
        self.readAdc.connect(w.readAdc)
        w.adcData.connect(self.adcData)

    @pyqtSlot(list)
    def adcData(self, nm, data):
        self.data = data
        self.updatePlot()
        if self.ui.autoBtn.isChecked():
            QTimer.singleShot(250, self.on_singleBtn_clicked(nm))

    #TODO: check that the use of nm is correct in above and below

    @pyqtSlot(int)
    def on_singleBtn_clicked(self, nm):
        self.readAdc.emit(nm, self.ui.samples.value())

    @pyqtSlot()
    def on_saveMatBtn_clicked(self):
        if not self.data:
            return
        data = []
        for ch in range(0,64):
            #data.append((np.array([i[ch] for i in self.data])-32768/2)*(100e-3/32768)*1e6)
            data.append((np.array([i[ch] for i in self.data])))
        data = np.array(data)
        fn = QFileDialog.getSaveFileName(self, caption='Save .mat file', filter='*.mat', directory=self.lastfile)
        self.lastfile = fn
        if fn:
            scipy.io.savemat(fn, dict(chan_data=data))

    @pyqtSlot()
    def updatePlot(self):
        if not self.data:
            return
        chA = self.ui.chanA.currentIndex()
        chB = self.ui.chanB.currentIndex()
        data = []
        for ch in range(0,64):
            #data.append((np.array([i[ch] for i in self.data])-32768/2)*(100e-3/32768)*1e6)
            data.append((np.array([i[ch] for i in self.data])))



        means = np.array([np.mean(data[i]) for i in range(0,64)])
        rms = np.array([np.std(data[i]) for i in range(0,64)])
        #print("Mean A: {}; mean B: {}, rms A: {}, rms B: {}, rms A-B: {}".format(np.mean(dataA),
        #                                                            np.mean(dataB),
        #                                                            np.std(dataA),
        #                                                            np.std(dataB),
        #                                                            np.std(dataA-dataB)))

        def calcTHD(d):
            indx = 11
            dfft = np.abs(np.fft.fft(d))/1000
            fund = dfft[indx]
            dist = 0
            for i in range(2,32):
                dist += dfft[i*indx]**2
            return 10*np.log10(dist/fund**2)

        for i in range(0, self.numPlots):
            ch = self.plotCh[i].currentIndex()
            dp = data[ch]
            try:
                self.plotLbl[i][0].setText("{:0.1f} rms".format(measureRms(dp)))
                self.plotLbl[i][1].setText("{:0.0f} dB".format(measureDist(dp)))
            except Exception:
                pass
            self.plots[i].clear()
            if self.plotEn[i].isChecked():
                self.plots[i].plot(y=dp, pen=(102,204,255))
                if self.ui.autorange.isChecked():
                    self.plots[i].getViewBox().autoRange()

        if self.ui.plotrms.isChecked():
            self.plots[0].plot(y=rms, pen='y')
            self.plots[0].plot(y=[10 for i in range(0,64)], pen='r')
            ct = 0
            for i in range(0,64):
                if 0.1 < rms[i] < 6 and 17000 > means[i] > 16000:
                    print("Ch {}: rms {:.2f} / mean {:.0f}".format(i, rms[i], means[i]))
                    ct += 1
            print("{} good channels".format(ct))
            print("")
            if self.ui.autorange.isChecked():
                    self.plots[0].getViewBox().autoRange()
        if self.ui.plotmean.isChecked():
            self.plots[0].plot(y=means, pen='w')
            if self.ui.autorange.isChecked():
                    self.plots[0].getViewBox().autoRange()
        if self.ui.plotTHD.isChecked():
            dist = []
            level = -38
            count = 0
            for i in range(0,64):
                thd = calcTHD(data[i])
                dist.append(thd)
                if thd < level:
                    print("Ch {}: THD {:.1f} dB".format(i,thd))
                    count += 1
            print("{} channels with < {} dB THD".format(count,level))
            self.plots[0].plot(y=dist, pen='w')
            self.plots[0].plot(y=[level for i in range(0,64)], pen='r')
            if self.ui.autorange.isChecked():
                    self.plots[0].getViewBox().autoRange()


