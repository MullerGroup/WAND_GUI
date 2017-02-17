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
        self.streamBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.streamBtn.setCheckable(True)
        self.streamBtn.setObjectName(_fromUtf8("streamBtn"))
        self.gridLayout.addWidget(self.streamBtn, 2, 0, 1, 1)


        self.interpolateBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.interpolateBtn.setCheckable(True)
        self.interpolateBtn.setObjectName(_fromUtf8("interpolateBtn"))
        self.gridLayout.addWidget(self.interpolateBtn, 7, 0, 1, 1)

        # self.testBtn = QtGui.QPushButton(self.dockWidgetContents)
        # self.testBtn.setCheckable(True)
        # self.testBtn.setObjectName(_fromUtf8("testBtn"))
        # self.gridLayout.addWidget(self.testBtn, 4, 0, 1, 1)

        self.plot = GraphicsLayoutWidget(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.plot.setObjectName(_fromUtf8("plot"))
        self.gridLayout.addWidget(self.plot, 1, 0, 1, 5)
        
        self.clearBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.clearBtn.setObjectName(_fromUtf8("clearBtn"))
        self.gridLayout.addWidget(self.clearBtn, 2, 1, 1, 1)

        # self.saveEn = QtGui.QCheckBox(self.dockWidgetContents)
        # self.saveEn.setCheckable(True)
        # self.saveEn.setObjectName(_fromUtf8("saveEn"))
        # self.gridLayout.addWidget(self.saveEn, 2, 1, 1, 1)
        self.autorange = QtGui.QCheckBox(self.dockWidgetContents)
        self.autorange.setObjectName(_fromUtf8("autorange"))
        self.gridLayout.addWidget(self.autorange, 2, 2, 1, 1)
        self.dispStream = QtGui.QLabel(self.dockWidgetContents)
        self.dispStream.setObjectName(_fromUtf8("dispStream"))
        self.gridLayout.addWidget(self.dispStream, 5, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.dockWidgetContents)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 3, 1, 1)
        self.xRange = QtGui.QSpinBox(self.dockWidgetContents)
        self.xRange.setMinimum(1)
        self.xRange.setMaximum(50000)
        self.xRange.setSingleStep(1000)
        self.xRange.setProperty("value", 2000)
        self.xRange.setObjectName(_fromUtf8("xRange"))
        self.gridLayout.addWidget(self.xRange, 2, 4, 1, 1)

        self.ch0 = QtGui.QSpinBox(self.dockWidgetContents)
        self.ch0.setMinimum(0)
        self.ch0.setMaximum(0)
        self.ch0.setSingleStep(1)
        self.ch0.setProperty("value", 0)
        self.ch0.setObjectName(_fromUtf8("ch0"))
        self.gridLayout.addWidget(self.ch0, 5, 1, 1, 1)

        self.ch1 = QtGui.QSpinBox(self.dockWidgetContents)
        self.ch1.setMinimum(0)
        self.ch1.setMaximum(0)
        self.ch1.setSingleStep(1)
        self.ch1.setProperty("value", 0)
        self.ch1.setObjectName(_fromUtf8("ch1"))
        self.gridLayout.addWidget(self.ch1, 5, 2, 1, 1)

        self.ch2 = QtGui.QSpinBox(self.dockWidgetContents)
        self.ch2.setMinimum(0)
        self.ch2.setMaximum(0)
        self.ch2.setSingleStep(1)
        self.ch2.setProperty("value", 0)
        self.ch2.setObjectName(_fromUtf8("ch2"))
        self.gridLayout.addWidget(self.ch2, 5, 3, 1, 1)

        self.ch3 = QtGui.QSpinBox(self.dockWidgetContents)
        self.ch3.setMinimum(0)
        self.ch3.setMaximum(0)
        self.ch3.setSingleStep(1)
        self.ch3.setProperty("value", 0)
        self.ch3.setObjectName(_fromUtf8("ch3"))
        self.gridLayout.addWidget(self.ch3, 5, 4, 1, 1)

        self.stimRep = QtGui.QSpinBox(self.dockWidgetContents)
        self.stimRep.setMinimum(1)
        self.stimRep.setMaximum(10000)
        self.stimRep.setSingleStep(1)
        self.stimRep.setProperty("value", 1)
        self.stimRep.setObjectName(_fromUtf8("stimRep"))
        self.gridLayout.addWidget(self.stimRep, 6, 1, 1, 1)

        self.stim = QtGui.QCheckBox(self.dockWidgetContents)
        self.stim.setCheckable(True)
        self.stim.setObjectName(_fromUtf8("stim"))
        self.gridLayout.addWidget(self.stim, 6, 0, 1, 1)

        self.delayLabel = QtGui.QLabel(self.dockWidgetContents)
        self.delayLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.delayLabel.setObjectName(_fromUtf8("delayLabel"))
        self.gridLayout.addWidget(self.delayLabel, 6, 2, 1, 1)

        self.stimDelay = QtGui.QSpinBox(self.dockWidgetContents)
        self.stimDelay.setMinimum(0)
        self.stimDelay.setMaximum(100000)
        self.stimDelay.setSingleStep(1)
        self.stimDelay.setProperty("value", 0)
        self.stimDelay.setObjectName(_fromUtf8("stimDelay"))
        self.gridLayout.addWidget(self.stimDelay, 6, 3, 1, 1)

        self.artDelayLabel = QtGui.QLabel(self.dockWidgetContents)
        self.artDelayLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.artDelayLabel.setObjectName(_fromUtf8("artDelayLabel"))
        self.gridLayout.addWidget(self.artDelayLabel, 7, 2, 1, 1)

        self.artDelay = QtGui.QSpinBox(self.dockWidgetContents)
        self.artDelay.setMinimum(0)
        self.artDelay.setMaximum(100000)
        self.artDelay.setSingleStep(1)
        self.artDelay.setProperty("value", 10)
        self.artDelay.setObjectName(_fromUtf8("artDelay"))
        self.gridLayout.addWidget(self.artDelay, 7, 3, 1, 1)

        self.stimOnNMLabel = QtGui.QLabel(self.dockWidgetContents)
        self.stimOnNMLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.stimOnNMLabel.setObjectName(_fromUtf8("stimOnNMLabel"))
        self.gridLayout.addWidget(self.stimOnNMLabel, 8, 2, 1, 1)

        self.stimOnNM = QtGui.QComboBox(self.dockWidgetContents)
        self.stimOnNM.setEditable(False)
        self.stimOnNM.setMaxVisibleItems(2)
        self.stimOnNM.setObjectName(_fromUtf8("stimOnNM"))
        self.stimOnNM.addItem(_fromUtf8(""))
        self.stimOnNM.addItem(_fromUtf8(""))
        self.stimOnNM.setCurrentIndex(0)
        self.gridLayout.addWidget(self.stimOnNM, 8, 3, 1, 1)

        self.impStart = QtGui.QCheckBox(self.dockWidgetContents)
        self.impStart.setObjectName(_fromUtf8("impStart"))
        self.gridLayout.addWidget(self.impStart, 8, 0, 1, 1)

        self.impDelay = QtGui.QSpinBox(self.dockWidgetContents)
        self.impDelay.setMinimum(10)
        self.impDelay.setMaximum(100000)
        self.impDelay.setSingleStep(1)
        self.impDelay.setProperty("value", 1000)
        self.impDelay.setObjectName(_fromUtf8("impDelay"))
        self.gridLayout.addWidget(self.impDelay, 8, 1, 1, 1)

        self.thresh = QtGui.QSpinBox(self.dockWidgetContents)
        self.thresh.setMinimum(10)
        self.thresh.setMaximum(100000)
        self.thresh.setSingleStep(1)
        self.thresh.setProperty("value", 1000)
        self.thresh.setObjectName(_fromUtf8("thresh"))
        self.gridLayout.addWidget(self.thresh, 8, 4, 1, 1)

        DataVisualizer.setWidget(self.dockWidgetContents)

        self.retranslateUi(DataVisualizer)
        QtCore.QMetaObject.connectSlotsByName(DataVisualizer)
        self.dispStream.setProperty("checked", True)

    def retranslateUi(self, DataVisualizer):
        DataVisualizer.setWindowTitle(_translate("DataVisualizer", "ADC Control", None))
        self.label_6.setText(_translate("DataVisualizer", "Scroll to change displayed channels,\n"
" shift+scroll to scroll faster", None))
        # self.plotEn.setText(_translate("DataVisualizer", "Plot", None))
        self.streamBtn.setText(_translate("DataVisualizer", "Stream Data", None))
        self.interpolateBtn.setText(_translate("DataVisualizer", "Interpolate Artifacts", None))
        # self.testBtn.setText(_translate("DataVisualizer", "Test Comm", None))
        self.stimOnNM.setItemText(0, _translate("DataVisualizer", "0", None))
        self.stimOnNM.setItemText(1, _translate("DataVisualizer", "1", None))
        self.clearBtn.setText(_translate("DataVisualizer", "Clear plots", None))
        # self.saveEn.setText(_translate("DataVisualizer", "Save", None))
        self.stim.setText(_translate("DataVisualizer", "Stimulate in Stream, Repeat:", None))
        self.autorange.setText(_translate("DataVisualizer", "Y Autorange", None))
        self.label_5.setText(_translate("DataVisualizer", "X-axis range (ms):", None))
        self.delayLabel.setText(_translate("DataVisualizer", "Stim Delay:", None))
        self.artDelayLabel.setText(_translate("DataVisualizer", "Artifact Delay:", None))
        self.stimOnNMLabel.setText(_translate("DataVisualizer", "Stim on NM #:", None))
        self.dispStream.setText(_translate("DataVisualizer", "Display stream data from Ch:", None))
        self.impStart.setText(_translate("DataVisualizer", "Measure Impedance w/ Delay:", None))

from pyqtgraph import GraphicsLayoutWidget
