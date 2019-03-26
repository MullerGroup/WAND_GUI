# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'commanddockwidget.ui'
#
# Created: Thu Jul 30 18:44:20 2015
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

class Ui_nmicConfig(object):
    def setupUi(self, nmicConfig):
        nmicConfig.setObjectName(_fromUtf8("nmicConfig"))
        nmicConfig.resize(400, 300)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        self.wideIn = QtGui.QCheckBox(self.dockWidgetContents)
        self.wideIn.setObjectName(_fromUtf8("wideIn"))
        self.gridLayout.addWidget(self.wideIn, 0, 1, 1, 4)

        self.hvEn = QtGui.QPushButton(self.dockWidgetContents)
        self.hvEn.setObjectName(_fromUtf8("hvEn"))
        self.gridLayout.addWidget(self.hvEn, 1, 1, 1, 4)

        spacer = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacer, 2, 0, 1, 1)

        self.zMagLabel = QtGui.QLabel(self.dockWidgetContents)
        self.zMagLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.zMagLabel.setObjectName(_fromUtf8("zMagLabel"))
        self.gridLayout.addWidget(self.zMagLabel, 2, 1, 1, 1)

        self.zMag = QtGui.QComboBox(self.dockWidgetContents)
        self.zMag.setObjectName(_fromUtf8("zMag"))
        self.gridLayout.addWidget(self.zMag, 2, 2, 1, 1)
        self.zMag.addItem("0.0 uA")
        self.zMag.addItem("0.5 uA")
        self.zMag.addItem("1.0 uA")
        self.zMag.addItem("1.5 uA")

        self.zCycleLabel = QtGui.QLabel(self.dockWidgetContents)
        self.zCycleLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.zCycleLabel.setObjectName(_fromUtf8("zCycleLabel"))
        self.gridLayout.addWidget(self.zCycleLabel, 2, 3, 1, 1)

        self.zCycle = QtGui.QSpinBox(self.dockWidgetContents)
        self.zCycle.setMinimum(1)
        self.zCycle.setMaximum(16)
        self.zCycle.setSingleStep(1)
        self.zCycle.setProperty("value", 1)
        self.zCycle.setObjectName(_fromUtf8("zCycle"))
        self.gridLayout.addWidget(self.zCycle, 2, 4, 1, 1)

        self.gridLayout.addItem(spacer, 2, 5, 1, 1)

        self.zSet = QtGui.QPushButton(self.dockWidgetContents)
        self.zSet.setObjectName(_fromUtf8("zSet"))
        self.gridLayout.addWidget(self.zSet, 3, 1, 1, 4)


        nmicConfig.setWidget(self.dockWidgetContents)

        self.retranslateUi(nmicConfig)
        QtCore.QMetaObject.connectSlotsByName(nmicConfig)

    def retranslateUi(self, nmicConfig):
        nmicConfig.setWindowTitle(_translate("nmicConfig", "Configuration", None))
        self.wideIn.setText(_translate("nmicConfig", "Wide-input mode", None))
        self.hvEn.setText(_translate("nmicConfig", "Enable 12V stim compliance", None))
        self.zMagLabel.setText(_translate("nmicConfig", "Z-measure current", None))
        self.zCycleLabel.setText(_translate("nmicConfig", "Z-measure # cycles", None))
        self.zSet.setText(_translate("nmicConfig", "Set Z-measure", None))
        