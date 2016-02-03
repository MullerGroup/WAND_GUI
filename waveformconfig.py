from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.ui_wfmdialog import Ui_WaveformDialog
import StimConfig

class WaveformEditor(QDialog):
    def __init__(self, model, amplLsb, parent=None):
        super().__init__(parent)
        self.ui = Ui_WaveformDialog()
        self.ui.setupUi(self)
        self.ui.amplitudeBox.setSingleStep(amplLsb)
        self.ui.amplitudeBox.setMaximum(amplLsb*(2**6-1))
        self.ui.NameEdit.textChanged.connect(self.onObjEdited)
        self.ui.pulseWidthBox.valueChanged.connect(self.onObjEdited)
        self.ui.amplitudeBox.valueChanged.connect(self.onObjEdited)
        self.ui.shortTimeWidthBox.valueChanged.connect(self.onObjEdited)
        self.ui.interphaseGapWidthBox.valueChanged.connect(self.onObjEdited)
        self.ui.setupWidthBox.valueChanged.connect(self.onObjEdited)
        self.ui.numberOfPulsesBox.valueChanged.connect(self.onObjEdited)
        self.model = model
        self.ui.waveformList.setModel(self.model)
        self.ui.waveformList.selectionModel().currentRowChanged.connect(self.onRowChanged)
        self.ui.waveformList.setCurrentIndex(self.model.index(0))
        self.blockEditing = False
        
        s = QSettings()
        if s.value("waveformeditor/geometry") is not None:
            self.setGeometry(s.value("waveformeditor/geometry", type=QRect))
            self.ui.splitter.restoreState(s.value("waveformeditor/splitterstate"))

    @pyqtSlot()
    def on_addWaveformButton_clicked(self):
        self.model.addWfm(StimConfig.Waveform())
        
    @pyqtSlot()
    def on_delWaveformButton_clicked(self):        
        ci = self.ui.waveformList.currentIndex()
        if ci.isValid():
            confirm = QMessageBox(QMessageBox.Warning, "Delete waveform?", "Do you really want to delete the waveform '{}'?".format(self.model.data(ci)), QMessageBox.Yes|QMessageBox.No)
            confirm.setDefaultButton(QMessageBox.No)
            confirm.exec()
            if confirm.result() == QMessageBox.Yes:
                self.model.removeWfm(ci.row())
    
    @pyqtSlot()
    def onObjEdited(self):
        ci = self.ui.waveformList.currentIndex()
        if ci.isValid() and not self.blockEditing:
            obj = self.model.getRow(ci.row())
            obj.name = self.ui.NameEdit.text()
            obj.amplitude = round(self.ui.amplitudeBox.value() / self.ui.amplitudeBox.singleStep())
            obj.shortTimeWidth = self.ui.shortTimeWidthBox.value()
            obj.interphaseGapWidth = self.ui.interphaseGapWidthBox.value()
            obj.pulseWidth = self.ui.pulseWidthBox.value()
            obj.setupWidth = self.ui.setupWidthBox.value()
            obj.nump = self.ui.numberOfPulsesBox.value()

    # Load currentWaveform in display window
    @pyqtSlot(QModelIndex, QModelIndex)
    def onRowChanged(self, current, previous):
        obj = self.model.getRow(current.row())
        self.blockEditing = True    # prevent changing values from triggering model update
        self.ui.NameEdit.setText(obj.name)
        self.ui.amplitudeBox.setValue(obj.amplitude * self.ui.amplitudeBox.singleStep())
        self.ui.shortTimeWidthBox.setValue(obj.shortTimeWidth)
        self.ui.interphaseGapWidthBox.setValue(obj.interphaseGapWidth)
        self.ui.pulseWidthBox.setValue(obj.pulseWidth)
        self.ui.setupWidthBox.setValue(obj.setupWidth)
        self.ui.numberOfPulsesBox.setValue(obj.nump)
        self.blockEditing = False

    # Load/Save dialog geometry/state
    def done(self, result):
        s = QSettings()
        s.setValue("waveformeditor/splitterstate", self.ui.splitter.saveState())
        s.setValue("waveformeditor/geometry", self.geometry())
        super().done(result)


