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
        self.gridLayout.addWidget(self.wideIn, 0, 0, 1, 1)

        nmicConfig.setWidget(self.dockWidgetContents)

        self.retranslateUi(nmicConfig)
        QtCore.QMetaObject.connectSlotsByName(nmicConfig)

    def retranslateUi(self, nmicConfig):
        nmicConfig.setWindowTitle(_translate("nmicConfig", "Configuration", None))
        self.wideIn.setText(_translate("nmicConfig", "Wide input mode", None))
        