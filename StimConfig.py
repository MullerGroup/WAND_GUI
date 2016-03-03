from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.ui_stimconfig import Ui_StimConfig
from waveformconfig import WaveformEditor
from ui.ui_stimConfig_unit import Ui_StimConfigUnit
import pickle

class WaveformList(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.list = []
        
    def rowCount(self, parent):
        if not parent.isValid(): # invalid parent means root node
            return len(self.list)
        else: # there are no children
            return 0
        
    def getRow(self, row):
        return self.list[row]
        
    def data(self, idx, role=Qt.DisplayRole):
        if (role == Qt.DisplayRole):
            return self.list[idx.row()].name
            
    def addWfm(self, wfm):
        self.beginInsertRows(QModelIndex(), self.rowCount(QModelIndex()), self.rowCount(QModelIndex()))
        self.list.append(wfm)
        wfm.dataChanged.connect(self.wfmChanged)
        self.endInsertRows()
        
    def removeWfm(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self.list[row]
        self.endRemoveRows()
        
    @pyqtSlot('QObject')
    def wfmChanged(self, wfm):
        idx = self.index(self.list.index(wfm))
        self.dataChanged.emit(idx, idx)

class Waveform(QObject):
    dataChanged = pyqtSignal(QObject)
    
    def __init__(self, name="Default Waveform", amplitude=10, shortTimeWidth=10, interphaseGapWidth=10, pulseWidth=10, setupWidth=10, nump=10, loc1=10, loc2=10):
        super().__init__()
        self.name = name 
        self.amplitude = amplitude #STIM_AMPL_x<5:0>
        self.shortTimeWidth = shortTimeWidth # SHRT_TW_x<4:0>
        self.interphaseGapWidth = interphaseGapWidth # IPH_GAPW_x<4:0>
        self.pulseWidth = pulseWidth # PW_x<4:0>
        self.setupWidth = setupWidth # SW_x<4:0>
        self.nump = nump # NUMP_x<6:0>
        self.loc1=loc1 # LOC1_x<5:0>
        self.loc2=loc2 # LOC2_x<5:0>

    def saveState(self):
        return (self.name, self.amplitude, self.shortTimeWidth, self.interphaseGapWidth, self.pulseWidth, self.setupWidth, self.nump, self.loc1, self.loc2)

    def restoreState(self, state):
        self.name, self.amplitude, self.shortTimeWidth, self.interphaseGapWidth, self.pulseWidth, self.setupWidth, self.nump, self.loc1, self.loc2 = state

    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, name):
        self._name = name
        self.dataChanged.emit(self)

    @property
    def amplitude(self):
        return self._amplitude

    @amplitude.setter
    def amplitude(self, amplitude):
        self._amplitude = amplitude
        self.dataChanged.emit(self)

    @property
    def shortTimeWidth(self):
        return self._shortTimeWidth

    @shortTimeWidth.setter
    def shortTimeWidth(self, shortTimeWidth):
        self._shortTimeWidth = shortTimeWidth
        self.dataChanged.emit(self)

    @property
    def interphaseGapWidth(self):
        return self._interphaseGapWidth

    @interphaseGapWidth.setter
    def interphaseGapWidth(self, interphaseGapWidth):
        self._interphaseGapWidth = interphaseGapWidth
        self.dataChanged.emit(self)

    @property
    def pulseWidth(self):
        return self._pulseWidth
        
    @pulseWidth.setter
    def pulseWidth(self, pulseWidth):
        self._pulseWidth = pulseWidth
        self.dataChanged.emit(self)

    @property
    def setupWidth(self):
        return self._setupWidth

    @setupWidth.setter
    def setupWidth(self, setupWidth):
        self._setupWidth = setupWidth
        self.dataChanged.emit(self)

    @property
    def nump(self):
        return self._nump

    @nump.setter
    def nump(self, nump):
        self._nump = nump
        self.dataChanged.emit(self)

    @property
    def loc1(self):
        return self._loc1

    @loc1.setter
    def loc1(self, loc1):
        self._loc1 = loc1
        self.dataChanged.emit(self)

    @property
    def loc2(self):
        return self._loc2

    @loc2.setter
    def loc2(self, loc2):
        self._loc2 = loc2
        self.dataChanged.emit(self)

class StimConfigUnit(QWidget):
    # int --> channel
    # str --> stimulator identifier A,B,C,D
    sourceChange = pyqtSignal(int, str)
    sinkChange = pyqtSignal()

    def __init__(self, nm, model, stimLabel, parent=None):
        super().__init__(parent)
        self.ui = Ui_StimConfigUnit()
        self.ui.setupUi(self)
        self.nm = nm
        self.model = model
        self.ui.wvfmBox.setModel(self.model)
        self.ui.enStim.setText("Enable")
        self.stimLabel = stimLabel
        self.ui.stimLabel.setText(self.stimLabel)
        self.stimListSource = ["Source " + str(b) for b in range((64*nm),(64*nm)+64)]
        self.stimListSink = ["Sink " + str(b) for b in range((64*nm),(64*nm)+64)]
        self.ui.Loc1Box.insertItems(0, self.stimListSource)
        self.ui.Loc2Box.insertItems(0, self.stimListSink)
       # self.ui.Loc1Box.currentIndexChanged.connect(self.on_source_changed)
       # self.ui.Loc2Box.currentIndexChanged.connect(self.on_sink_changed)
        self.waveformSelection = []
        self.sourceIndex = []
        self.sinkIndex = []

    def getState(self):
        return (self.ui.wvfmBox.currentIndex(),
                self.ui.Loc1Box.currentIndex(),
                self.ui.Loc2Box.currentIndex(),
                self.ui.enStim.isChecked())

    def loadState(self, state):
        self.ui.wvfmBox.setCurrentIndex(state[0])
        self.ui.Loc1Box.setCurrentIndex(state[1])
        self.ui.Loc2Box.setCurrentIndex(state[2])
        self.ui.enStim.setChecked(state[3])

class StimConfig(QDockWidget):
    writeReg = pyqtSignal(int, int, int)

    def __init__(self, parent=None, nm=0):
        super().__init__(parent)
        self.nm = nm
        self.ui = Ui_StimConfig()
        self.ui.setupUi(self)
        self.wfmlist = WaveformList()
        # Connect WaveformList items to dropBoxes
        self.stimLabels = ["A", "B", "C", "D"]
        self.unit = [StimConfigUnit(self.nm, self.wfmlist, self.stimLabels[b]) for b in range(0,4)]
        for b in range(0,4):
            self.ui.gridLayout.addWidget(self.unit[b], b+2, 1, 1, 6)
        [self.ui.stimMultBox.addItem(str(b) + " uA") for b in range(20,100,20)]
        [self.ui.hrcBox.addItem("VDDH - " + str(b) + " mV") for b in range(200,0,-50)]
        [self.ui.clBox.addItem("VDDM + " + str(b) + " mV") for b in range(100,500,100)]
        self.ui.stimFrequencyBox.valueChanged.connect(self.on_stimFrequencyBox_valueChanged)

        self.setWindowTitle("NM{} Stim Config".format(self.nm))

    def saveState(self):
        s = QSettings()
        cbs = [self.ui.blkAllCheck,
               self.ui.cgndCheck,
               self.ui.doffCheck,
               self.ui.gmBiasCheck,
               self.ui.gmPulseCheck,
               self.ui.gndResCheck,
               self.ui.noCheckCheck,
               self.ui.pchgModCheck,
               self.ui.pkgPdCheck,
               self.ui.pkgRetCheck,
               self.ui.polCheck,
               self.ui.prCheck,
               self.ui.refPdCheck,
               self.ui.regBiasCheck,
               self.ui.stopModeCheck,
               self.ui.testEnCheck,
               self.ui.testSelCheck]
        cmbs = [self.ui.clBox, self.ui.hrcBox, self.ui.stimMultBox]
        spins = [self.ui.nccpBox,
                 self.ui.stimBiasBox,
                 self.ui.stimFrequencyBox]
        s.beginWriteArray("stimSetup/units")
        for i in range(0,4):
            s.setArrayIndex(i)
            s.setValue("state", self.unit[i].getState())
        s.endArray()
        s.setValue("stimSetup/cbState", pickle.dumps([cb.isChecked() for cb in cbs]))
        s.setValue("stimSetup/cmbState", pickle.dumps([b.currentIndex() for b in cmbs]))
        s.setValue("stimSetup/spinState", pickle.dumps([s.value() for s in spins]))
        self.saveWfms()

    def loadState(self):
        s = QSettings()
        self.loadWfms()
        cbs = [self.ui.blkAllCheck,
               self.ui.cgndCheck,
               self.ui.doffCheck,
               self.ui.gmBiasCheck,
               self.ui.gmPulseCheck,
               self.ui.gndResCheck,
               self.ui.noCheckCheck,
               self.ui.pchgModCheck,
               self.ui.pkgPdCheck,
               self.ui.pkgRetCheck,
               self.ui.polCheck,
               self.ui.prCheck,
               self.ui.refPdCheck,
               self.ui.regBiasCheck,
               self.ui.stopModeCheck,
               self.ui.testEnCheck,
               self.ui.testSelCheck]
        cmbs = [self.ui.clBox, self.ui.hrcBox, self.ui.stimMultBox]
        spins = [self.ui.nccpBox,
                 self.ui.stimBiasBox,
                 self.ui.stimFrequencyBox]
        sz = s.beginReadArray("stimSetup/units")
        for i in range(0, sz):
            s.setArrayIndex(i)
            self.unit[i].loadState(s.value("state"))
        s.endArray()

        try:
            cbState = pickle.loads(s.value("stimSetup/cbState"))
            cmbState = pickle.loads(s.value("stimSetup/cmbState"))
            spinState = pickle.loads(s.value("stimSetup/spinState"))
        except Exception as e:
            print("failed to load stim state")
            return

        for c,ch in zip(cbs, cbState):
            c.setChecked(ch)
        for c,st in zip(cmbs, cmbState):
            c.setCurrentIndex(st)
        for c,st in zip(spins, spinState):
            c.setValue(st)

    def setWorker(self, w):
        self.writeReg.connect(w.writeReg)

    def saveWfms(self):
        s = QSettings()
        s.beginWriteArray("stimWaveforms")
        i = 0
        for wfm in self.wfmlist.list:
            s.setArrayIndex(i)
            s.setValue("wfm", pickle.dumps(wfm.saveState()))
            i += 1
        s.endArray()

    def loadWfms(self):
        s = QSettings()
        sz = s.beginReadArray("stimWaveforms")
        for i in range(0, sz):
            s.setArrayIndex(i)
            wfmState = pickle.loads(s.value("wfm"))
            wfm = Waveform()
            wfm.restoreState(wfmState)
            self.wfmlist.addWfm(wfm)
        s.endArray()

    @pyqtSlot()
    def on_stimFrequencyBox_valueChanged(self):
        # Enter stimFrequency using stimPeriod, but calculate frequency and display as prefix
        val = self.ui.stimFrequencyBox.value()
        freq = round(1e5/val)/100
        self.ui.stimFrequencyBox.setPrefix(str(freq) + " Hz (")

    @pyqtSlot()
    def on_waveformConfigButton_clicked(self):
        dlg = WaveformEditor(self.wfmlist, (self.ui.stimMultBox.currentIndex()+1)*20)
        dlg.exec()

    @pyqtSlot(int)
    def on_writeRegs_clicked(self, nm):
        for address in range(16,32):
            self.writeReg.emit(nm, address, self.createRegisterData(address))

    def createBitMask(self, bitShift, bitSpan):
        bitMask = 0
        for i in range(0, bitSpan):
            bitMask += 2**i
        bitMask = bitMask << bitShift
        return bitMask

    def makeBit(self, val, bitShift, bitSpan, lsb, minVal=0):
        bitMask = self.createBitMask(bitShift, bitSpan)
        decVal = int((val-minVal)/lsb)
        return (decVal << bitShift) & bitMask

    def val2reg_stimFreq(self, guiVal):
        bitShift = 0
        bitSpan = 10
        bitMask = self.createBitMask(bitShift, bitSpan)
        # tclk in units of ms
        tclk = 7.8125e-3
        decVal = round((1/8)*((guiVal/tclk) - 500))
        return (decVal << bitShift) & bitMask

    def createRegisterData(self, address):
        wfm = []
        for i in range(0,4):
            wfm.append(self.wfmlist.getRow(self.unit[i].ui.wvfmBox.currentIndex()))
        regVal = 0
        if address == 16:
            # STIM_CFG0
            noCheck = int(self.ui.noCheckCheck.isChecked())
            blkAll = int(self.ui.blkAllCheck.isChecked())
            stimMult_index = self.ui.stimMultBox.currentIndex()
            stimAmpB = wfm[1].amplitude
            stimAmpA = wfm[0].amplitude
            regVal = self.makeBit(noCheck,15,1,1) | self.makeBit(blkAll,14,1,1) | self.makeBit(stimMult_index,12,2,1) | self.makeBit(stimAmpB,6,6,1) | self.makeBit(stimAmpA,0,6,1)
        elif address == 17:
            # STIM_CFG1
            stopMode = int(self.ui.stopModeCheck.isChecked())
            gndRes = int(self.ui.gndResCheck.isChecked())
            pkgPd = int(self.ui.pkgPdCheck.isChecked())
            refPd = int(self.ui.refPdCheck.isChecked())
            stimAmpD = wfm[3].amplitude
            stimAmpC = wfm[2].amplitude
            regVal = self.makeBit(stopMode,15,1,1) | self.makeBit(gndRes,14,1,1) | self.makeBit(pkgPd,13,1,1) | self.makeBit(refPd,12,1,1) | self.makeBit(stimAmpD,6,6,1) | self.makeBit(stimAmpC,0,6,1)
        elif address == 18:
            # STIM_CFG2
            shortTwA = wfm[0].shortTimeWidth
            iphGapwA = wfm[0].interphaseGapWidth
            pwA = wfm[0].pulseWidth
            #print("shortTimeWidthA : {}".format(shortTwA))
            #print("shortTimeWidthA : {:016b}".format(self.makeBit(shortTwA,10,5,31.25,31.25)))
            regVal = self.makeBit(shortTwA,10,5,31.25,31.25) | self.makeBit(iphGapwA,5,5,31.25,31.25) | self.makeBit(pwA,0,5,15.625,15.625)
        elif address == 19:
            # STIM_CFG3
            shortTwB = wfm[1].shortTimeWidth
            iphGapwB = wfm[1].interphaseGapWidth
            pwB = wfm[1].pulseWidth
            #print("shortTimeWidthB : {}".format(shortTwB))
            regVal = self.makeBit(shortTwB,10,5,31.25,31.25) | self.makeBit(iphGapwB,5,5,31.25,31.25) | self.makeBit(pwB,0,5,15.625,15.625)
        elif address == 20:
            # STIM_CFG4
            shortTwC = wfm[2].shortTimeWidth
            iphGapwC = wfm[2].interphaseGapWidth
            pwC = wfm[2].pulseWidth
            #print("shortTimeWidthC : {}".format(shortTwC))
            regVal = self.makeBit(shortTwC,10,5,31.25,31.25) | self.makeBit(iphGapwC,5,5,31.25,31.25) | self.makeBit(pwC,0,5,15.625,15.625)
        elif address == 21:
            # STIM_CFG5
            shortTwD = wfm[3].shortTimeWidth
            iphGapwD = wfm[3].interphaseGapWidth
            pwD = wfm[3].pulseWidth
            #print("shortTimeWidthD : {}".format(shortTwD))
            regVal = self.makeBit(shortTwD,10,5,31.25,31.25) | self.makeBit(iphGapwD,5,5,31.25,31.25) | self.makeBit(pwD,0,5,15.625,15.625)
        elif address == 22:
            # STIM_CFG6
            swC = wfm[2].setupWidth
            swB = wfm[1].setupWidth
            swA = wfm[0].setupWidth
            regVal = self.makeBit(swC,10,5,31.25,31.25) | self.makeBit(swB,5,5,31.25,31.25) | self.makeBit(swA,0,5,31.25,31.25)
        elif address == 23:
            # STIM_CFG7
            pkgRet = int(self.ui.pkgRetCheck.isChecked())
            pchgMod = int(self.ui.pchgModCheck.isChecked())
            cgnd = int(self.ui.cgndCheck.isChecked())
            doff = int(self.ui.doffCheck.isChecked())
            pr = int(self.ui.prCheck.isChecked())
            pol = int(self.ui.polCheck.isChecked())
            cl_index = self.ui.clBox.currentIndex()
            hrc_index = self.ui.hrcBox.currentIndex()
            swD = wfm[3].setupWidth
            regVal = self.makeBit(pkgRet,14,1,1) | self.makeBit(pchgMod,13,1,1) | self.makeBit(cgnd,12,1,1) | self.makeBit(doff,11,1,1) | self.makeBit(pr,10,1,1) | self.makeBit(pol,9,1,1) | self.makeBit(cl_index,7,2,1) | self.makeBit(hrc_index,5,2,1) | self.makeBit(swD,0,5,31.25,31.25)
        elif address == 24:
            # STIM_CFG8
            enableStimA = int(self.unit[0].ui.enStim.isChecked())
            enableStimB = int(self.unit[1].ui.enStim.isChecked())
            numpA = enableStimA*wfm[0].nump
            numpB = enableStimB*wfm[1].nump
            regVal = self.makeBit(numpB,7,7,1) | self.makeBit(numpA,0,7,1)
        elif address == 25:
            # STIM_CFG9
            enableStimC = int(self.unit[2].ui.enStim.isChecked())
            enableStimD = int(self.unit[3].ui.enStim.isChecked())
            numpC = enableStimC*wfm[2].nump
            numpD = enableStimD*wfm[3].nump
            regVal = self.makeBit(numpD,7,7,1) | self.makeBit(numpC,0,7,1)
        elif address == 26:
            # STIM_CFG10
            gmPulse = int(self.ui.gmPulseCheck.isChecked())
            regBias = int(self.ui.regBiasCheck.isChecked())
            gmBias = int(self.ui.gmBiasCheck.isChecked())
            loc2A = self.unit[0].ui.Loc2Box.currentIndex()
            loc1A = self.unit[0].ui.Loc1Box.currentIndex()
            regVal = self.makeBit(gmPulse,14,1,1) | self.makeBit(regBias,13,1,1) | self.makeBit(gmBias,12,1,1) | self.makeBit(loc2A,6,6,1) | self.makeBit(loc1A,0,6,1)
        elif address == 27:
            # STIM_CFG11
            stimBias = int(self.ui.stimBiasBox.value())
            loc2B = self.unit[1].ui.Loc2Box.currentIndex()
            loc1B = self.unit[1].ui.Loc1Box.currentIndex()
            regVal = self.makeBit(stimBias,12,3,15,45) | self.makeBit(loc2B,6,6,1) | self.makeBit(loc1B,0,6,1)
        elif address == 28:
            # STIM_CFG12
            testEn = int(self.ui.testEnCheck.isChecked())
            testSel = int(self.ui.testSelCheck.isChecked())
            loc2C = self.unit[2].ui.Loc2Box.currentIndex()
            loc1C = self.unit[2].ui.Loc1Box.currentIndex()
            regVal = self.makeBit(testEn,13,1,1) | self.makeBit(testSel,12,1,1) | self.makeBit(loc2C,6,6,1) | self.makeBit(loc1C,0,6,1)
        elif address == 29:
            # STIM_CFG13
            loc2D = self.unit[3].ui.Loc2Box.currentIndex()
            loc1D = self.unit[3].ui.Loc1Box.currentIndex()
            regVal = self.makeBit(loc2D,6,6,1) | self.makeBit(loc1D,0,6,1)
        elif address == 30:
            # STIM_CFG14
            nccp = self.ui.nccpBox.value()
            #stimFreq = self.ui.stimFrequencyBox.value()
            stimFreq = self.val2reg_stimFreq(self.ui.stimFrequencyBox.value())
            regVal = self.makeBit(nccp,10,6,1) | stimFreq
        elif address == 31:
            # STIM_CFG15, reserved register, dont care
            regVal = 0
        else:
            print("ERROR createRegister : Register address invalid.")
        print("Address: {}; RegisterValue: {:016b}".format(address, regVal))
        return regVal
