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

        # Row 0

        self.plot = GraphicsLayoutWidget(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.plot.setObjectName(_fromUtf8("plot"))
        self.gridLayout.addWidget(self.plot, 0, 0, 1, 5)

        # Row 1

        self.streamBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.streamBtn.setCheckable(True)
        self.streamBtn.setObjectName(_fromUtf8("streamBtn"))
        self.gridLayout.addWidget(self.streamBtn, 1, 0, 1, 1)

        self.clearBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.clearBtn.setObjectName(_fromUtf8("clearBtn"))
        self.gridLayout.addWidget(self.clearBtn, 1, 1, 1, 1)

        self.autorange = QtGui.QCheckBox(self.dockWidgetContents)
        self.autorange.setObjectName(_fromUtf8("autorange"))
        self.gridLayout.addWidget(self.autorange, 1, 2, 1, 1)

        self.xRangeLabel = QtGui.QLabel(self.dockWidgetContents)
        self.xRangeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.xRangeLabel.setObjectName(_fromUtf8("xRangeLabel"))
        self.gridLayout.addWidget(self.xRangeLabel, 1, 3, 1, 1)

        self.xRange = QtGui.QSpinBox(self.dockWidgetContents)
        self.xRange.setMinimum(1)
        self.xRange.setMaximum(50000)
        self.xRange.setSingleStep(1000)
        self.xRange.setProperty("value", 2000)
        self.xRange.setObjectName(_fromUtf8("xRange"))
        self.gridLayout.addWidget(self.xRange, 1, 4, 1, 1)

        # Row 2

        self.dispStream = QtGui.QCheckBox(self.dockWidgetContents)
        self.dispStream.setObjectName(_fromUtf8("dispStream"))
        self.gridLayout.addWidget(self.dispStream, 2, 0, 1, 1)
        self.dispStream.setProperty("checked", True)

        self.ch0 = QtGui.QSpinBox(self.dockWidgetContents)
        self.ch0.setMinimum(0)
        self.ch0.setMaximum(63)
        self.ch0.setSingleStep(1)
        self.ch0.setProperty("value", 0)
        self.ch0.setObjectName(_fromUtf8("ch0"))
        self.gridLayout.addWidget(self.ch0, 2, 1, 1, 1)

        self.ch1 = QtGui.QSpinBox(self.dockWidgetContents)
        self.ch1.setMinimum(0)
        self.ch1.setMaximum(63)
        self.ch1.setSingleStep(1)
        self.ch1.setProperty("value", 1)
        self.ch1.setObjectName(_fromUtf8("ch1"))
        self.gridLayout.addWidget(self.ch1, 2, 2, 1, 1)

        self.ch2 = QtGui.QSpinBox(self.dockWidgetContents)
        self.ch2.setMinimum(0)
        self.ch2.setMaximum(63)
        self.ch2.setSingleStep(1)
        self.ch2.setProperty("value", 2)
        self.ch2.setObjectName(_fromUtf8("ch2"))
        self.gridLayout.addWidget(self.ch2, 2, 3, 1, 1)

        self.ch3 = QtGui.QSpinBox(self.dockWidgetContents)
        self.ch3.setMinimum(0)
        self.ch3.setMaximum(63)
        self.ch3.setSingleStep(1)
        self.ch3.setProperty("value", 3)
        self.ch3.setObjectName(_fromUtf8("ch3"))
        self.gridLayout.addWidget(self.ch3, 2, 4, 1, 1)

        # Row 3

        self.line = QtGui.QFrame(self.dockWidgetContents);
        self.line.setObjectName(_fromUtf8("line"))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.gridLayout.addWidget(self.line,3, 0, 1, 5)

        # Row 4

        self.stim = QtGui.QCheckBox(self.dockWidgetContents)
        self.stim.setCheckable(True)
        self.stim.setObjectName(_fromUtf8("stim"))
        self.gridLayout.addWidget(self.stim, 4, 0, 1, 1)

        self.stimRep = QtGui.QSpinBox(self.dockWidgetContents)
        self.stimRep.setMinimum(1)
        self.stimRep.setMaximum(10000)
        self.stimRep.setSingleStep(1)
        self.stimRep.setProperty("value", 1)
        self.stimRep.setObjectName(_fromUtf8("stimRep"))
        self.gridLayout.addWidget(self.stimRep, 4, 1, 1, 1)

        self.delayLabel = QtGui.QLabel(self.dockWidgetContents)
        self.delayLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.delayLabel.setObjectName(_fromUtf8("delayLabel"))
        self.gridLayout.addWidget(self.delayLabel, 4, 2, 1, 1)

        self.stimDelay = QtGui.QSpinBox(self.dockWidgetContents)
        self.stimDelay.setMinimum(10)
        self.stimDelay.setMaximum(100000)
        self.stimDelay.setSingleStep(1)
        self.stimDelay.setProperty("value", 1000)
        self.stimDelay.setObjectName(_fromUtf8("stimDelay"))
        self.gridLayout.addWidget(self.stimDelay, 4, 3, 1, 1)

        # Row 5
        
        self.interpolateBtn = QtGui.QCheckBox(self.dockWidgetContents)
        self.interpolateBtn.setCheckable(True)
        self.interpolateBtn.setObjectName(_fromUtf8("interpolateBtn"))
        self.gridLayout.addWidget(self.interpolateBtn, 5, 0, 1, 1)

        self.artDelayLabel = QtGui.QLabel(self.dockWidgetContents)
        self.artDelayLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.artDelayLabel.setObjectName(_fromUtf8("artDelayLabel"))
        self.gridLayout.addWidget(self.artDelayLabel, 5, 2, 1, 1)

        self.artDelay = QtGui.QSpinBox(self.dockWidgetContents)
        self.artDelay.setMinimum(10)
        self.artDelay.setMaximum(100000)
        self.artDelay.setSingleStep(1)
        self.artDelay.setProperty("value", 1000)
        self.artDelay.setObjectName(_fromUtf8("artDelay"))
        self.gridLayout.addWidget(self.artDelay, 5, 3, 1, 1)

        # Row 6

        self.impStart = QtGui.QCheckBox(self.dockWidgetContents)
        self.impStart.setObjectName(_fromUtf8("impStart"))
        self.gridLayout.addWidget(self.impStart, 6, 0, 1, 1)

        self.impDelayLabel = QtGui.QLabel(self.dockWidgetContents)
        self.impDelayLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.impDelayLabel.setObjectName(_fromUtf8("impDelayLabel"))
        self.gridLayout.addWidget(self.impDelayLabel, 6, 2, 1, 1)

        self.impDelay = QtGui.QSpinBox(self.dockWidgetContents)
        self.impDelay.setMinimum(10)
        self.impDelay.setMaximum(100000)
        self.impDelay.setSingleStep(1)
        self.impDelay.setProperty("value", 1000)
        self.impDelay.setObjectName(_fromUtf8("impDelay"))
        self.gridLayout.addWidget(self.impDelay, 6, 3, 1, 1)

        DataVisualizer.setWidget(self.dockWidgetContents)

        self.retranslateUi(DataVisualizer)
        QtCore.QMetaObject.connectSlotsByName(DataVisualizer)

    def retranslateUi(self, DataVisualizer):
        DataVisualizer.setWindowTitle(_translate("DataVisualizer", "WAND_Control", None))

        self.streamBtn.setText(_translate("DataVisualizer", "Stream Data", None))
        self.clearBtn.setText(_translate("DataVisualizer", "Clear plots", None))
        self.autorange.setText(_translate("DataVisualizer", "Autorange Y", None))
        self.xRangeLabel.setText(_translate("DataVisualizer", "X-axis range (ms):", None))

        self.dispStream.setText(_translate("DataVisualizer", "Display stream data from Ch:", None))

        self.stim.setText(_translate("DataVisualizer", "Stimulate in Stream, Repeat:", None))

        self.delayLabel.setText(_translate("DataVisualizer", "Stim Delay:", None))
        self.interpolateBtn.setText(_translate("DataVisualizer", "Interpolate Artifacts", None))
        self.artDelayLabel.setText(_translate("DataVisualizer", "Artifact Delay:", None))
        self.impDelayLabel.setText(_translate("DataVisualizer", "Impedance Delay:", None))

        self.impStart.setText(_translate("DataVisualizer", "Measure Impedance w/ Delay:", None))

from pyqtgraph import GraphicsLayoutWidget
