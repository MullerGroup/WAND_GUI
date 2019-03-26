# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'commanddockwidget.ui'
#
# Created: Thu Jul 30 18:44:20 2015
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

class Ui_nmicCommand(object):
    def setupUi(self, nmicCommand):
        nmicCommand.setObjectName(_fromUtf8("nmicCommand"))
        nmicCommand.resize(400, 300)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.stim_transfer = QtGui.QPushButton(self.dockWidgetContents)
        self.stim_transfer.setObjectName(_fromUtf8("stim_transfer"))
        self.gridLayout.addWidget(self.stim_transfer, 7, 0, 1, 1)
        self.stim_start = QtGui.QPushButton(self.dockWidgetContents)
        self.stim_start.setObjectName(_fromUtf8("stim_start"))
        self.gridLayout.addWidget(self.stim_start, 6, 0, 1, 1)
        self.reset = QtGui.QPushButton(self.dockWidgetContents)
        self.reset.setObjectName(_fromUtf8("reset"))
        self.gridLayout.addWidget(self.reset, 0, 0, 1, 1)
        self.hv_load = QtGui.QPushButton(self.dockWidgetContents)
        self.hv_load.setObjectName(_fromUtf8("hv_load"))
        self.gridLayout.addWidget(self.hv_load, 2, 0, 1, 1)
        self.imp_start = QtGui.QPushButton(self.dockWidgetContents)
        self.imp_start.setObjectName(_fromUtf8("imp_start"))
        self.gridLayout.addWidget(self.imp_start, 3, 0, 1, 1)
        self.clear_err = QtGui.QPushButton(self.dockWidgetContents)
        self.clear_err.setObjectName(_fromUtf8("clear_err"))
        self.gridLayout.addWidget(self.clear_err, 1, 0, 1, 1)
        self.stim_reset = QtGui.QPushButton(self.dockWidgetContents)
        self.stim_reset.setObjectName(_fromUtf8("stim_reset"))
        self.gridLayout.addWidget(self.stim_reset, 4, 0, 1, 1)
        nmicCommand.setWidget(self.dockWidgetContents)

        self.retranslateUi(nmicCommand)
        QtCore.QMetaObject.connectSlotsByName(nmicCommand)

    def retranslateUi(self, nmicCommand):
        nmicCommand.setWindowTitle(_translate("nmicCommand", "Commands", None))
        self.stim_transfer.setText(_translate("nmicCommand", "Transfer stimulation settings", None))
        self.stim_start.setText(_translate("nmicCommand", "Trigger stimulation", None))
        self.reset.setText(_translate("nmicCommand", "Reset NMIC", None))
        self.hv_load.setText(_translate("nmicCommand", "Load high voltage charge pump", None))
        self.imp_start.setText(_translate("nmicCommand", "Trigger impedance measurement", None))
        self.clear_err.setText(_translate("nmicCommand", "Clear errors", None))
        self.stim_reset.setText(_translate("nmicCommand", "Reset stimulation", None))

