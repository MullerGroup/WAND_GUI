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
        DataVisualizer.resize(981, 827)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DataVisualizer.sizePolicy().hasHeightForWidth())
        DataVisualizer.setSizePolicy(sizePolicy)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.plot = GraphicsLayoutWidget(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.plot.setObjectName(_fromUtf8("plot"))
        self.gridLayout.addWidget(self.plot, 0, 0, 1, 3)
        self.autorange = QtGui.QCheckBox(self.dockWidgetContents)
        self.autorange.setObjectName(_fromUtf8("autorange"))
        self.gridLayout.addWidget(self.autorange, 1, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.dockWidgetContents)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 1, 1, 1)
        self.numPlotsDisplayed = QtGui.QComboBox(self.dockWidgetContents)
        self.numPlotsDisplayed.setEditable(False)
        self.numPlotsDisplayed.setMaxVisibleItems(5)
        self.numPlotsDisplayed.setObjectName(_fromUtf8("numPlotsDisplayed"))
        self.numPlotsDisplayed.addItem(_fromUtf8(""))
        self.numPlotsDisplayed.addItem(_fromUtf8(""))
        self.numPlotsDisplayed.addItem(_fromUtf8(""))
        self.numPlotsDisplayed.addItem(_fromUtf8(""))
        self.numPlotsDisplayed.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.numPlotsDisplayed, 1, 2, 1, 1)
        self.autoBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.autoBtn.setCheckable(True)
        self.autoBtn.setObjectName(_fromUtf8("autoBtn"))
        self.gridLayout.addWidget(self.autoBtn, 2, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.dockWidgetContents)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 1, 1, 1)
        self.xRange = QtGui.QSpinBox(self.dockWidgetContents)
        self.xRange.setMinimum(1)
        self.xRange.setMaximum(20000)
        self.xRange.setSingleStep(1000)
        self.xRange.setProperty("value", 1000)
        self.xRange.setObjectName(_fromUtf8("xRange"))
        self.gridLayout.addWidget(self.xRange, 2, 2, 1, 1)
        self.singleBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.singleBtn.setObjectName(_fromUtf8("singleBtn"))
        self.gridLayout.addWidget(self.singleBtn, 3, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 1, 1, 1)
        self.samples = QtGui.QSpinBox(self.dockWidgetContents)
        self.samples.setMinimum(1)
        self.samples.setMaximum(10000)
        self.samples.setSingleStep(100)
        self.samples.setProperty("value", 1000)
        self.samples.setObjectName(_fromUtf8("samples"))
        self.gridLayout.addWidget(self.samples, 3, 2, 1, 1)
        DataVisualizer.setWidget(self.dockWidgetContents)

        self.retranslateUi(DataVisualizer)
        self.numPlotsDisplayed.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DataVisualizer)

    def retranslateUi(self, DataVisualizer):
        DataVisualizer.setWindowTitle(_translate("DataVisualizer", "ADC Control", None))
        self.autorange.setText(_translate("DataVisualizer", "Autorange", None))
        self.label_4.setText(_translate("DataVisualizer", "Plots", None))
        self.numPlotsDisplayed.setItemText(0, _translate("DataVisualizer", "1", None))
        self.numPlotsDisplayed.setItemText(1, _translate("DataVisualizer", "2", None))
        self.numPlotsDisplayed.setItemText(2, _translate("DataVisualizer", "4", None))
        self.numPlotsDisplayed.setItemText(3, _translate("DataVisualizer", "8", None))
        self.numPlotsDisplayed.setItemText(4, _translate("DataVisualizer", "16", None))
        self.autoBtn.setText(_translate("DataVisualizer", "Auto", None))
        self.label_5.setText(_translate("DataVisualizer", "X-axis range (ms):", None))
        self.singleBtn.setText(_translate("DataVisualizer", "Update", None))
        self.label_3.setText(_translate("DataVisualizer", "Samples:", None))

from pyqtgraph import GraphicsLayoutWidget
