# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/DataVisualizer.ui'
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
        DataVisualizer.resize(1105, 562)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DataVisualizer.sizePolicy().hasHeightForWidth())
        DataVisualizer.setSizePolicy(sizePolicy)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plot = GraphicsLayoutWidget(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.plot.setObjectName(_fromUtf8("plot"))
        self.verticalLayout.addWidget(self.plot)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.samples = QtGui.QSpinBox(self.dockWidgetContents)
        self.samples.setMinimum(1)
        self.samples.setMaximum(10000)
        self.samples.setSingleStep(100)
        self.samples.setProperty("value", 1000)
        self.samples.setObjectName(_fromUtf8("samples"))
        self.gridLayout.addWidget(self.samples, 1, 2, 1, 1)
        self.singleBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.singleBtn.setObjectName(_fromUtf8("singleBtn"))
        self.gridLayout.addWidget(self.singleBtn, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        self.autoBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.autoBtn.setCheckable(True)
        self.autoBtn.setObjectName(_fromUtf8("autoBtn"))
        self.gridLayout.addWidget(self.autoBtn, 0, 2, 1, 1)
        self.autorange = QtGui.QCheckBox(self.dockWidgetContents)
        self.autorange.setObjectName(_fromUtf8("autorange"))
        self.gridLayout.addWidget(self.autorange, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        DataVisualizer.setWidget(self.dockWidgetContents)

        self.retranslateUi(DataVisualizer)
        QtCore.QMetaObject.connectSlotsByName(DataVisualizer)

    def retranslateUi(self, DataVisualizer):
        DataVisualizer.setWindowTitle(_translate("DataVisualizer", "ADC Control", None))
        self.singleBtn.setText(_translate("DataVisualizer", "Update", None))
        self.label_3.setText(_translate("DataVisualizer", "Samples:", None))
        self.autoBtn.setText(_translate("DataVisualizer", "Auto", None))
        self.autorange.setText(_translate("DataVisualizer", "Autorange", None))

from pyqtgraph import GraphicsLayoutWidget
