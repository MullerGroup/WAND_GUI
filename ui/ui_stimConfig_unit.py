# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stimConfig_unit.ui'
#
# Created: Mon Jul 27 15:56:55 2015
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

class Ui_StimConfigUnit(object):
    def setupUi(self, StimConfigUnit):
        StimConfigUnit.setObjectName(_fromUtf8("StimConfigUnit"))
        StimConfigUnit.resize(583, 28)
        self.gridLayout = QtGui.QGridLayout(StimConfigUnit)
        self.gridLayout.setContentsMargins(-1, 4, -1, 4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.wvfmBox = QtGui.QComboBox(StimConfigUnit)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wvfmBox.sizePolicy().hasHeightForWidth())
        self.wvfmBox.setSizePolicy(sizePolicy)
        self.wvfmBox.setMinimumSize(QtCore.QSize(120, 0))
        self.wvfmBox.setObjectName(_fromUtf8("wvfmBox"))
        self.gridLayout.addWidget(self.wvfmBox, 0, 1, 1, 1)
        self.Loc1Box = QtGui.QComboBox(StimConfigUnit)
        self.Loc1Box.setObjectName(_fromUtf8("Loc1Box"))
        self.gridLayout.addWidget(self.Loc1Box, 0, 2, 1, 1)
        self.Loc2Box = QtGui.QComboBox(StimConfigUnit)
        self.Loc2Box.setObjectName(_fromUtf8("Loc2Box"))
        self.gridLayout.addWidget(self.Loc2Box, 0, 3, 1, 1)
        self.enStim = QtGui.QCheckBox(StimConfigUnit)
        self.enStim.setObjectName(_fromUtf8("enStim"))
        self.gridLayout.addWidget(self.enStim, 0, 4, 1, 1)
        self.stimLabel = QtGui.QLabel(StimConfigUnit)
        self.stimLabel.setObjectName(_fromUtf8("stimLabel"))
        self.gridLayout.addWidget(self.stimLabel, 0, 0, 1, 1)

        self.retranslateUi(StimConfigUnit)
        QtCore.QMetaObject.connectSlotsByName(StimConfigUnit)

    def retranslateUi(self, StimConfigUnit):
        StimConfigUnit.setWindowTitle(_translate("StimConfigUnit", "Form", None))
        self.enStim.setText(_translate("StimConfigUnit", "Enable", None))
        self.stimLabel.setText(_translate("StimConfigUnit", "TextLabel", None))

