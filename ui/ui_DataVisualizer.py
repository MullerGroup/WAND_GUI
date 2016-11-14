# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/DataVisualizer.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DataVisualizer(object):
    def setupUi(self, DataVisualizer):
        DataVisualizer.setObjectName(_fromUtf8("DataVisualizer"))
        DataVisualizer.resize(919, 617)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DataVisualizer.sizePolicy().hasHeightForWidth())
        DataVisualizer.setSizePolicy(sizePolicy)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_6 = QtGui.QLabel(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Helvetica"))
        font.setPointSize(18)
        font.setItalic(True)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 3)
        # self.plotEn = QtGui.QCheckBox(self.dockWidgetContents)
        # self.plotEn.setCheckable(True)
        # self.plotEn.setObjectName(_fromUtf8("plotEn"))
        # self.gridLayout.addWidget(self.plotEn, 2, 2, 1, 1)
        self.saveBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.widget = self.gridLayout.addWidget(self.saveBtn, 2, 1, 1, 1)
        self.streamBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.streamBtn.setCheckable(True)
        self.streamBtn.setObjectName(_fromUtf8("streamBtn"))
        self.gridLayout.addWidget(self.streamBtn, 2, 0, 1, 1)
        self.artifactBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.artifactBtn.setCheckable(True)
        self.artifactBtn.setObjectName(_fromUtf8("artifactBtn"))
        self.gridLayout.addWidget(self.artifactBtn, 6, 2, 1, 1)
        # self.testBtn = QtGui.QPushButton(self.dockWidgetContents)
        # self.testBtn.setCheckable(True)
        # self.testBtn.setObjectName(_fromUtf8("testBtn"))
        # self.gridLayout.addWidget(self.testBtn, 4, 0, 1, 1)
        self.setupRecordingBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.setupRecordingBtn.setObjectName(_fromUtf8("setupRecordingBtn"))
        self.gridLayout.addWidget(self.setupRecordingBtn, 4, 0, 1, 1)
        self.plot = GraphicsLayoutWidget(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.plot.setObjectName(_fromUtf8("plot"))
        self.gridLayout.addWidget(self.plot, 1, 0, 1, 5)
        self.numPlotsDisplayed = QtGui.QComboBox(self.dockWidgetContents)
        self.numPlotsDisplayed.setEditable(False)
        self.numPlotsDisplayed.setMaxVisibleItems(5)
        self.numPlotsDisplayed.setObjectName(_fromUtf8("numPlotsDisplayed"))
        self.numPlotsDisplayed.addItem(_fromUtf8(""))
        self.numPlotsDisplayed.addItem(_fromUtf8(""))
        self.numPlotsDisplayed.addItem(_fromUtf8(""))
        self.numPlotsDisplayed.addItem(_fromUtf8(""))
        self.numPlotsDisplayed.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.numPlotsDisplayed, 2, 4, 1, 1)
        self.clearBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.clearBtn.setObjectName(_fromUtf8("clearBtn"))
        self.gridLayout.addWidget(self.clearBtn, 2, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.dockWidgetContents)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 3, 1, 1)
        # self.saveEn = QtGui.QCheckBox(self.dockWidgetContents)
        # self.saveEn.setCheckable(True)
        # self.saveEn.setObjectName(_fromUtf8("saveEn"))
        # self.gridLayout.addWidget(self.saveEn, 2, 1, 1, 1)
        self.autorange = QtGui.QCheckBox(self.dockWidgetContents)
        self.autorange.setObjectName(_fromUtf8("autorange"))
        self.gridLayout.addWidget(self.autorange, 3, 1, 1, 1)
        self.dispStream = QtGui.QCheckBox(self.dockWidgetContents)
        self.dispStream.setObjectName(_fromUtf8("dispStream"))
        self.gridLayout.addWidget(self.dispStream, 5, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.dockWidgetContents)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 3, 3, 1, 1)
        self.xRange = QtGui.QSpinBox(self.dockWidgetContents)
        self.xRange.setMinimum(1)
        self.xRange.setMaximum(50000)
        self.xRange.setSingleStep(1000)
        self.xRange.setProperty("value", 2000)
        self.xRange.setObjectName(_fromUtf8("xRange"))
        self.gridLayout.addWidget(self.xRange, 3, 4, 1, 1)

        self.ch0 = QtGui.QSpinBox(self.dockWidgetContents)
        self.ch0.setMinimum(0)
        self.ch0.setMaximum(98)
        self.ch0.setSingleStep(1)
        self.ch0.setProperty("value", 28)
        self.ch0.setObjectName(_fromUtf8("ch0"))
        self.gridLayout.addWidget(self.ch0, 5, 1, 1, 1)

        self.ch1 = QtGui.QSpinBox(self.dockWidgetContents)
        self.ch1.setMinimum(0)
        self.ch1.setMaximum(98)
        self.ch1.setSingleStep(1)
        self.ch1.setProperty("value", 29)
        self.ch1.setObjectName(_fromUtf8("ch1"))
        self.gridLayout.addWidget(self.ch1, 5, 2, 1, 1)

        self.ch2 = QtGui.QSpinBox(self.dockWidgetContents)
        self.ch2.setMinimum(0)
        self.ch2.setMaximum(98)
        self.ch2.setSingleStep(1)
        self.ch2.setProperty("value", 98)
        self.ch2.setObjectName(_fromUtf8("ch2"))
        self.gridLayout.addWidget(self.ch2, 5, 3, 1, 1)

        self.ch3 = QtGui.QSpinBox(self.dockWidgetContents)
        self.ch3.setMinimum(0)
        self.ch3.setMaximum(98)
        self.ch3.setSingleStep(1)
        self.ch3.setProperty("value", 97)
        self.ch3.setObjectName(_fromUtf8("ch3"))
        self.gridLayout.addWidget(self.ch3, 5, 4, 1, 1)

        self.stimRep = QtGui.QSpinBox(self.dockWidgetContents)
        self.stimRep.setMinimum(1)
        self.stimRep.setMaximum(255)
        self.stimRep.setSingleStep(1)
        self.stimRep.setProperty("value", 1)
        self.stimRep.setObjectName(_fromUtf8("stimRep"))
        self.gridLayout.addWidget(self.stimRep, 6, 1, 1, 1)

        self.singleBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.singleBtn.setObjectName(_fromUtf8("singleBtn"))
        self.gridLayout.addWidget(self.singleBtn, 3, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 4, 3, 1, 1)
        self.samples = QtGui.QSpinBox(self.dockWidgetContents)
        self.samples.setMinimum(1)
        self.samples.setMaximum(50000)
        self.samples.setSingleStep(100)
        self.samples.setProperty("value", 2000)
        self.samples.setObjectName(_fromUtf8("samples"))
        self.gridLayout.addWidget(self.samples, 4, 4, 1, 1)
        self.noise = QtGui.QCheckBox(self.dockWidgetContents)
        self.noise.setCheckable(True)
        self.noise.setObjectName(_fromUtf8("noise"))
        self.gridLayout.addWidget(self.noise, 3, 2, 1, 1)
        self.stim = QtGui.QCheckBox(self.dockWidgetContents)
        self.stim.setCheckable(True)
        self.stim.setObjectName(_fromUtf8("stim"))
        self.gridLayout.addWidget(self.stim, 6, 0, 1, 1)

        self.delayLabel = QtGui.QLabel(self.dockWidgetContents)
        self.delayLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.delayLabel.setObjectName(_fromUtf8("delayLabel"))
        self.gridLayout.addWidget(self.delayLabel, 6, 3, 1, 1)

        self.stimDelay = QtGui.QSpinBox(self.dockWidgetContents)
        self.stimDelay.setMinimum(10)
        self.stimDelay.setMaximum(10000)
        self.stimDelay.setSingleStep(1)
        self.stimDelay.setProperty("value", 1000)
        self.stimDelay.setObjectName(_fromUtf8("stimDelay"))
        self.gridLayout.addWidget(self.stimDelay, 6, 4, 1, 1)

        DataVisualizer.setWidget(self.dockWidgetContents)

        self.retranslateUi(DataVisualizer)
        self.numPlotsDisplayed.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(DataVisualizer)
        self.dispStream.setProperty("checked", True)

    def retranslateUi(self, DataVisualizer):
        DataVisualizer.setWindowTitle(_translate("DataVisualizer", "ADC Control", None))
        self.label_6.setText(_translate("DataVisualizer", "Scroll to change displayed channels,\n"
" shift+scroll to scroll faster", None))
        # self.plotEn.setText(_translate("DataVisualizer", "Plot", None))
        self.saveBtn.setText(_translate("DataVisualizer", "Save Plots", None))
        self.streamBtn.setText(_translate("DataVisualizer", "Stream Data", None))
        self.artifactBtn.setText(_translate("DataVisualizer", "Remove Artifacts", None))
        # self.testBtn.setText(_translate("DataVisualizer", "Test Comm", None))
        self.setupRecordingBtn.setText(_translate("DataVisualizer", "Setup Recording", None))
        self.numPlotsDisplayed.setItemText(0, _translate("DataVisualizer", "1", None))
        self.numPlotsDisplayed.setItemText(1, _translate("DataVisualizer", "2", None))
        self.numPlotsDisplayed.setItemText(2, _translate("DataVisualizer", "4", None))
        self.numPlotsDisplayed.setItemText(3, _translate("DataVisualizer", "8", None))
        self.numPlotsDisplayed.setItemText(4, _translate("DataVisualizer", "16", None))
        self.clearBtn.setText(_translate("DataVisualizer", "Clear plots", None))
        self.label_4.setText(_translate("DataVisualizer", "Plots", None))
        # self.saveEn.setText(_translate("DataVisualizer", "Save", None))
        self.noise.setText(_translate("DataVisualizer", "Print Noise + THD", None))
        self.stim.setText(_translate("DataVisualizer", "Stimulate in Stream, Repeat:", None))
        self.autorange.setText(_translate("DataVisualizer", "Autorange", None))
        self.label_5.setText(_translate("DataVisualizer", "X-axis range (ms):", None))
        self.singleBtn.setText(_translate("DataVisualizer", "Update", None))
        self.label_3.setText(_translate("DataVisualizer", "Samples:", None))
        self.delayLabel.setText(_translate("DataVisualizer", "Stim Delay:", None))
        self.dispStream.setText(_translate("DataVisualizer", "Display stream data from Ch:", None))

from pyqtgraph import GraphicsLayoutWidget
