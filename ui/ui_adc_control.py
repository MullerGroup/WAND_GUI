# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adc_control.ui'
#
# Created: Sun Oct 11 16:09:49 2015
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_AdcControl(object):
    def setupUi(self, AdcControl):
        AdcControl.setObjectName(_fromUtf8("AdcControl"))
        AdcControl.resize(844, 377)
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
        self.plot.setObjectName(_fromUtf8("plot"))
        self.verticalLayout.addWidget(self.plot)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.saveMatBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.saveMatBtn.setObjectName(_fromUtf8("saveMatBtn"))
        self.gridLayout.addWidget(self.saveMatBtn, 0, 0, 1, 1)
        self.autoBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.autoBtn.setCheckable(True)
        self.autoBtn.setObjectName(_fromUtf8("autoBtn"))
        self.gridLayout.addWidget(self.autoBtn, 0, 12, 1, 1)
        self.plotA = QtGui.QCheckBox(self.dockWidgetContents)
        self.plotA.setChecked(True)
        self.plotA.setObjectName(_fromUtf8("plotA"))
        self.gridLayout.addWidget(self.plotA, 0, 6, 1, 1)
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 4, 1, 1)
        self.singleBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.singleBtn.setObjectName(_fromUtf8("singleBtn"))
        self.gridLayout.addWidget(self.singleBtn, 0, 11, 1, 1)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.plotmean = QtGui.QCheckBox(self.dockWidgetContents)
        self.plotmean.setObjectName(_fromUtf8("plotmean"))
        self.gridLayout.addWidget(self.plotmean, 0, 10, 1, 1)
        self.chanB = QtGui.QComboBox(self.dockWidgetContents)
        self.chanB.setObjectName(_fromUtf8("chanB"))
        self.gridLayout.addWidget(self.chanB, 1, 5, 1, 1)
        self.chanA = QtGui.QComboBox(self.dockWidgetContents)
        self.chanA.setObjectName(_fromUtf8("chanA"))
        self.gridLayout.addWidget(self.chanA, 0, 5, 1, 1)
        self.samples = QtGui.QSpinBox(self.dockWidgetContents)
        self.samples.setMinimum(1)
        self.samples.setMaximum(10000)
        self.samples.setSingleStep(100)
        self.samples.setProperty("value", 1000)
        self.samples.setObjectName(_fromUtf8("samples"))
        self.gridLayout.addWidget(self.samples, 1, 12, 1, 1)
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 11, 1, 1)
        self.plotTHD = QtGui.QCheckBox(self.dockWidgetContents)
        self.plotTHD.setObjectName(_fromUtf8("plotTHD"))
        self.gridLayout.addWidget(self.plotTHD, 1, 10, 1, 1)
        self.chA_thd = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chA_thd.sizePolicy().hasHeightForWidth())
        self.chA_thd.setSizePolicy(sizePolicy)
        self.chA_thd.setMinimumSize(QtCore.QSize(45, 0))
        self.chA_thd.setObjectName(_fromUtf8("chA_thd"))
        self.gridLayout.addWidget(self.chA_thd, 0, 3, 1, 1)
        self.chB_thd = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chB_thd.sizePolicy().hasHeightForWidth())
        self.chB_thd.setSizePolicy(sizePolicy)
        self.chB_thd.setMinimumSize(QtCore.QSize(45, 0))
        self.chB_thd.setObjectName(_fromUtf8("chB_thd"))
        self.gridLayout.addWidget(self.chB_thd, 1, 3, 1, 1)
        self.chA_rms = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chA_rms.sizePolicy().hasHeightForWidth())
        self.chA_rms.setSizePolicy(sizePolicy)
        self.chA_rms.setMinimumSize(QtCore.QSize(45, 0))
        self.chA_rms.setObjectName(_fromUtf8("chA_rms"))
        self.gridLayout.addWidget(self.chA_rms, 0, 2, 1, 1)
        self.chB_rms = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chB_rms.sizePolicy().hasHeightForWidth())
        self.chB_rms.setSizePolicy(sizePolicy)
        self.chB_rms.setMinimumSize(QtCore.QSize(45, 0))
        self.chB_rms.setObjectName(_fromUtf8("chB_rms"))
        self.gridLayout.addWidget(self.chB_rms, 1, 2, 1, 1)
        self.chanC = QtGui.QComboBox(self.dockWidgetContents)
        self.chanC.setObjectName(_fromUtf8("chanC"))
        self.gridLayout.addWidget(self.chanC, 2, 5, 1, 1)
        self.chanD = QtGui.QComboBox(self.dockWidgetContents)
        self.chanD.setObjectName(_fromUtf8("chanD"))
        self.gridLayout.addWidget(self.chanD, 3, 5, 1, 1)
        self.label_4 = QtGui.QLabel(self.dockWidgetContents)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 4, 1, 1)
        self.label_5 = QtGui.QLabel(self.dockWidgetContents)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 3, 4, 1, 1)
        self.chC_thd = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chC_thd.sizePolicy().hasHeightForWidth())
        self.chC_thd.setSizePolicy(sizePolicy)
        self.chC_thd.setMinimumSize(QtCore.QSize(45, 0))
        self.chC_thd.setObjectName(_fromUtf8("chC_thd"))
        self.gridLayout.addWidget(self.chC_thd, 2, 3, 1, 1)
        self.chD_thd = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chD_thd.sizePolicy().hasHeightForWidth())
        self.chD_thd.setSizePolicy(sizePolicy)
        self.chD_thd.setMinimumSize(QtCore.QSize(45, 0))
        self.chD_thd.setObjectName(_fromUtf8("chD_thd"))
        self.gridLayout.addWidget(self.chD_thd, 3, 3, 1, 1)
        self.chC_rms = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chC_rms.sizePolicy().hasHeightForWidth())
        self.chC_rms.setSizePolicy(sizePolicy)
        self.chC_rms.setMinimumSize(QtCore.QSize(45, 0))
        self.chC_rms.setObjectName(_fromUtf8("chC_rms"))
        self.gridLayout.addWidget(self.chC_rms, 2, 2, 1, 1)
        self.chD_rms = QtGui.QLabel(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chD_rms.sizePolicy().hasHeightForWidth())
        self.chD_rms.setSizePolicy(sizePolicy)
        self.chD_rms.setMinimumSize(QtCore.QSize(45, 0))
        self.chD_rms.setObjectName(_fromUtf8("chD_rms"))
        self.gridLayout.addWidget(self.chD_rms, 3, 2, 1, 1)
        self.plotrms = QtGui.QCheckBox(self.dockWidgetContents)
        self.plotrms.setObjectName(_fromUtf8("plotrms"))
        self.gridLayout.addWidget(self.plotrms, 2, 10, 1, 1)
        self.plotB = QtGui.QCheckBox(self.dockWidgetContents)
        self.plotB.setChecked(True)
        self.plotB.setObjectName(_fromUtf8("plotB"))
        self.gridLayout.addWidget(self.plotB, 1, 6, 1, 1)
        self.plotC = QtGui.QCheckBox(self.dockWidgetContents)
        self.plotC.setChecked(True)
        self.plotC.setObjectName(_fromUtf8("plotC"))
        self.gridLayout.addWidget(self.plotC, 2, 6, 1, 1)
        self.plotD = QtGui.QCheckBox(self.dockWidgetContents)
        self.plotD.setChecked(True)
        self.plotD.setObjectName(_fromUtf8("plotD"))
        self.gridLayout.addWidget(self.plotD, 3, 6, 1, 1)
        self.autorange = QtGui.QCheckBox(self.dockWidgetContents)
        self.autorange.setObjectName(_fromUtf8("autorange"))
        self.gridLayout.addWidget(self.autorange, 3, 10, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        AdcControl.setWidget(self.dockWidgetContents)

        self.retranslateUi(AdcControl)
        QtCore.QMetaObject.connectSlotsByName(AdcControl)

    def retranslateUi(self, AdcControl):
        AdcControl.setWindowTitle(_translate("AdcControl", "ADC Control", None))
        self.saveMatBtn.setText(_translate("AdcControl", "Save .mat", None))
        self.autoBtn.setText(_translate("AdcControl", "Auto", None))
        self.plotA.setText(_translate("AdcControl", "Plot A", None))
        self.label.setText(_translate("AdcControl", "Channel A: ", None))
        self.singleBtn.setText(_translate("AdcControl", "Update", None))
        self.label_2.setText(_translate("AdcControl", "Channel B: ", None))
        self.plotmean.setText(_translate("AdcControl", "Plot mean", None))
        self.label_3.setText(_translate("AdcControl", "Samples:", None))
        self.plotTHD.setText(_translate("AdcControl", "Plot THD", None))
        self.chA_thd.setText(_translate("AdcControl", "-100 dB", None))
        self.chB_thd.setText(_translate("AdcControl", "-100 dB", None))
        self.chA_rms.setText(_translate("AdcControl", "500 LSB", None))
        self.chB_rms.setText(_translate("AdcControl", "500 LSB", None))
        self.label_4.setText(_translate("AdcControl", "Channel C: ", None))
        self.label_5.setText(_translate("AdcControl", "Channel D: ", None))
        self.chC_thd.setText(_translate("AdcControl", "-100 dB", None))
        self.chD_thd.setText(_translate("AdcControl", "-100 dB", None))
        self.chC_rms.setText(_translate("AdcControl", "500 LSB", None))
        self.chD_rms.setText(_translate("AdcControl", "500 LSB", None))
        self.plotrms.setText(_translate("AdcControl", "Plot rms", None))
        self.plotB.setText(_translate("AdcControl", "Plot B", None))
        self.plotC.setText(_translate("AdcControl", "Plot C", None))
        self.plotD.setText(_translate("AdcControl", "Plot D", None))
        self.autorange.setText(_translate("AdcControl", "Autorange", None))

from pyqtgraph import GraphicsLayoutWidget
