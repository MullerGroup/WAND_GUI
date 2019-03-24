from PyQt4.QtCore import *
from PyQt4.QtGui import *
from LabeledBinaryEdit import *
import time

from ui.ui_registereditor_fileIO import Ui_RegisterEditor

class Register(QObject):
    def __init__(self, addr, name, value=0, labels=[], parent=None, readOnly=False):
        super().__init__(parent)
        self.addr = addr
        self.name = name
        self.readOnly = readOnly
        self.labels = labels
        self.defaultValue = value
        self.addrLabel = None
        self.nameLabel = None
        self.writeButton = None
        self.binEdit = None
        
    def addWidgets(self, row, layout):
        self.addrLabel = QLabel()
        self.addrLabel.setText("0x{:02X}".format(int(self.addr)))
        self.addrLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel = QPushButton()
        self.nameLabel.setText(str(self.name))
        self.nameLabel.setFlat(True)

        #self.nameLabel.setAlignment(Qt.AlignCenter)
        self.binEdit = LabeledBinaryEdit(labels=self.labels)
        self.binEdit.setValue(self.defaultValue)
        self.binEdit.setEnabled(not self.readOnly)
        self.binEdit.valueChanged.connect(self.valueChanged)
        self.nameLabel.clicked.connect(self.binEdit.toggleAll)
        self.nameLabel.setEnabled(not self.readOnly)
        layout.addWidget(self.addrLabel, row, 0)
        layout.addWidget(self.nameLabel, row, 1)
        layout.addWidget(self.binEdit, row, 2)
        self.writeButton = QCheckBox()
        self.writeButton.setText("")
        self.writeButton.setEnabled(not self.readOnly)
        layout.addWidget(self.writeButton, row, 3, Qt.AlignCenter)
        
    
    @pyqtSlot(int)
    def valueChanged(self, val):
        self.writeButton.setChecked(True)
        
    def value(self):
        return self.binEdit.value()
        
    def setValue(self, value):
        self.binEdit.setValue(value)
        self.writeButton.setChecked(False)
        
    def needsWrite(self):
        return self.writeButton.isChecked()
        
    def clearWrite(self):
        self.writeButton.setChecked(False)

class RegisterEditor_v2(QDockWidget):
    # nm, addr, data
    writeReg = pyqtSignal(int, int, int)
    readReg = pyqtSignal(int, int)

    def __init__(self, parent=None, nm=0):
        super().__init__(parent)
        self.nm = nm
        self.ui = Ui_RegisterEditor()
        self.ui.setupUi(self)
        self.regs = [ Register(0x00, "CHIP_ID",    0X0000, [("CHIP_ID", 8),("CHIP_REV1",4),("CHIP_REV2",4)], self, True),
                      Register(0x01, "STATUS",     0x0000, [("STIM_ACTV",1),("",8),("ERR_POR",1),("ERR_CRC",1),("ERR_CFG",1),("ERR_COMP",4)], self, True),
                      Register(0x02, "PWR_CONFIG", 0x0000, [("HI_PWR_EN",1),("HV_CLKSHDN",1),("LV_CLKSEL",2),("HV_CLKSEL",3),("HV_TRI",1),("HV_DIS",1),("HV_VOLT",2),("FORCE_CP",1),("FORCE_LDO",1),("FORCE_POR3",1),("FORCE_POR1",1),("LV_RATIO",1)], self),
                      Register(0x03, "TEST_SEL",   0x0000, [("BG_SF_EN",1),("AN_SF_EN",1),("HV_SF_EN",1),("HV_TEST_SEL",2),("AN_TEST_SEL",2),("BG_TEST_SEL",3),("DTEST_SEL",6)], self),
                      Register(0x04, "REC_EN0",    0x0000, [(str(i),1) for i in range(15,-1,-1)], self),
                      Register(0x05, "REC_EN1",    0x0000, [(str(i),1) for i in range(31,15,-1)], self),
                      Register(0x06, "REC_EN2",    0x0000, [(str(i),1) for i in range(47,31,-1)], self),
                      Register(0x07, "REC_EN3",    0x0000, [(str(i),1) for i in range(63,47,-1)], self),
                      Register(0x08, "IMP_EN0",    0x0000, [(str(i),1) for i in range(15,-1,-1)], self),
                      Register(0x09, "IMP_EN1",    0x0000, [(str(i),1) for i in range(31,15,-1)], self),
                      Register(0x0A, "IMP_EN2",    0x0000, [(str(i),1) for i in range(47,31,-1)], self),
                      Register(0x0B, "IMP_EN3",    0x0000, [(str(i),1) for i in range(63,47,-1)], self),
                      Register(0x0C, "REC_CONFIG", 0x0000, [("CHOP_CLK",2),("CAP_GAIN",3),("RST_WIDTH",2),("",1),("REC_EN",1),("Z_MAG",3),("GM_RST",1),("EN_LDO",1),("SYNC_MODE",1),("WIDE_IN",1)], self),
                      Register(0x0D, "SYS_CONFIG", 0x0000, [("CLK_OUT_EN",1),("REC_STIM_BIAS",1),("REC_CURR_GEN",3),("BG_CLK",1),("BG_CAL",2),("IMP_CYCLES",4),("TX_DRIVE",4)], self),
                      Register(0x0E, "NULL",       0x0000, [("",16)], self, True),
                      Register(0x0F, "SCRATCH",    0x0000, [("SCRATCH",16)], self),
                      Register(0x10, "STIM_CFG0",  0x0000, [("NOCHECK",1),("BLK_ALL",1),("STIM_MULT",2),("STIM_AMP_B",6),("STIM_AMP_A",6)], self),
                      Register(0x11, "STIM_CFG1",  0x0000, [("STOP_MODE",1),("GND_RES",1),("PKG_PD",1),("REF_PD",1),("STIM_AMP_D",6),("STIM_AMP_C",6)], self),
                      Register(0x12, "STIM_CFG2",  0x0000, [("",1),("SHRT_TW_A",5),("IPH_GAPW_A",5),("PW_A",5)], self),
                      Register(0x13, "STIM_CFG3",  0x0000, [("",1),("SHRT_TW_B",5),("IPH_GAPW_B",5),("PW_B",5)], self),
                      Register(0x14, "STIM_CFG4",  0x0000, [("",1),("SHRT_TW_C",5),("IPH_GAPW_C",5),("PW_C",5)], self),
                      Register(0x15, "STIM_CFG5",  0x0000, [("",1),("SHRT_TW_D",5),("IPH_GAPW_D",5),("PW_D",5)], self),
                      Register(0x16, "STIM_CFG6",  0x0000, [("",1),("SW_C",5),("SW_B",5),("SW_A",5)], self),
                      Register(0x17, "STIM_CFG7",  0x0000, [("",1),("PKG_RET",1),("PCHGMOD",1),("CGND",1),("DOFF",1),("PR",1),("POL",1),("CL",2),("HRC",2),("SW_D",5)], self),
                      Register(0x18, "STIM_CFG8",  0x0000, [("",2),("NUMP_B",7),("NUMP_A",7)], self),
                      Register(0x19, "STIM_CFG9",  0x0000, [("",2),("NUMP_D",7),("NUMP_C",7)], self),
                      Register(0x1A, "STIM_CFG10", 0x0000, [("",1),("GMPULSE",1),("REGBIAS",1),("GMBIAS",1),("LOC2_A",6),("LOC1_A",6)], self),
                      Register(0x1B, "STIM_CFG11", 0x0000, [("",1),("STIMBIAS",3),("LOC2_B",6),("LOC1_B",6)], self),
                      Register(0x1C, "STIM_CFG12", 0x0000, [("",2),("TESTEN",1),("TESTSEL",1),("LOC2_C",6),("LOC1_C",6)], self),
                      Register(0x1D, "STIM_CFG13", 0x0000, [("",4),("LOC2_D",6),("LOC1_D",6)], self),
                      Register(0x1E, "STIM_CFG14", 0x0000, [("NCCP",6),("STIM_FREQ",10)], self),
                      Register(0x1F, "STIM_CFG15", 0x0000, [("",16)], self, True)
                    ]
        row = 2
        for r in self.regs:
            r.addWidgets(row, self.ui.gridLayout)
            line = QFrame()
            line.setFrameShadow(QFrame.Raised)
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            self.ui.gridLayout.addWidget(line, row+1, 0, 1, 4)
            row += 2
        self.ui.gridLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), row, 0, 1, 4)
        self.restoreSettings()

        self.setWindowTitle("NM{} Registers".format(self.nm))

    def setWorker(self, w):
        self.readReg.connect(w.readReg)
        self.writeReg.connect(w.writeReg)
        w.regReadData.connect(self.regReadData)
        w.saveRegs.connect(self.saveRegs)

    def saveSettings(self):
        s = QSettings("settings.plist", QSettings.NativeFormat)
        s.beginWriteArray("regEdit/values{}".format(self.nm))
        i = 0
        for r in self.regs:
            s.setArrayIndex(i)
            s.setValue("addr", r.addr)
            s.setValue("data", r.value())
            i += 1
        s.endArray()

    def restoreSettings(self):
        s = QSettings("settings.plist", QSettings.NativeFormat)
        sz = s.beginReadArray("regEdit/values{}".format(self.nm))
        for i in range(0, sz):
            s.setArrayIndex(i)
            a = s.value("addr")
            if self.regs[i].addr == a:
                d = s.value("data")
                self.regs[i].setValue(d)
        s.endArray()


    @pyqtSlot(int, int, int)
    def regReadData(self, nm, addr, data):
        if not self.nm==nm:
            return
        self.regs[addr].setValue(data)

    @pyqtSlot(str, int)
    def saveRegs(self, fn, nm_num):
        if self.nm != nm_num:
            return
        print('reg edit call {}'.format(self.nm))
        if not fn:
            return
        fh = open(fn,"a")

        fh.write('NM{} Registers:\n\n'.format(self.nm))

        for index in range(len(self.regs)):
            fh.write("%s=%04X\n" % (self.regs[index].name, self.regs[index].value()))

        fh.write('\n\n')

        if self.nm == 0:
            fh.write('Notes:\n\n')
            notes, ok = QInputDialog.getText(self, 'Notes', 'Enter notes for stream: ')
            if ok:
                fh.write(str(notes))

        fh.close()
        # for r in self.regs:
        #     if r.needsWrite():
        #         print("Write {} to reg {}".format(r.value(), r.name))
        #         r.clearWrite()


    @pyqtSlot()
    def on_readButton_clicked(self):
        for r in self.regs:
            # if (r.addr == 0x00):
            #     self.readReg.emit(self.nm, r.addr)
            self.readReg.emit(self.nm, r.addr)
            # time.sleep(0.1)
        # self.readReg.emit(self.nm, self.regs[0].addr)

    @pyqtSlot()
    def on_writeButton_clicked(self):
        for r in self.regs:
            if r.needsWrite():
                self.writeReg.emit(self.nm, r.addr, r.value())
                r.clearWrite()
                time.sleep(0.1)

    @pyqtSlot()
    def on_writeAllBtn_clicked(self):
        for r in self.regs:
            if not r.readOnly:
                self.writeReg.emit(self.nm, r.addr, r.value())
                r.clearWrite()
                time.sleep(0.1)

    @pyqtSlot()
    def on_txtReadButton_clicked(self):
        fn = QFileDialog.getOpenFileName()
        if not fn:
            return
        with open(fn) as fobj:
            for line in fobj:
                print(line.rstrip())
    
    @pyqtSlot()
    def on_txtWriteButton_clicked(self):
        fn = QFileDialog.getSaveFileName()
        if not fn:
            return
        fh = open(fn,"w")
        for index in range(len(self.regs)):
            fh.write("%s=%04X\n" % (self.regs[index].name, self.regs[index].value()))
        fh.close()
        for r in self.regs:
            if r.needsWrite():
                print("Write {} to reg {}".format(r.value(), r.name))
                r.clearWrite()
