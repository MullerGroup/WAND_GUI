# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'boardcontrol.ui'
#
# Created: Mon Oct 12 11:44:06 2015
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

class Ui_BoardControl(object):
    def setupUi(self, BoardControl):
        BoardControl.setObjectName(_fromUtf8("BoardControl"))
        BoardControl.resize(278, 284)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.disconnBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.disconnBtn.setEnabled(False)
        self.disconnBtn.setObjectName(_fromUtf8("disconnBtn"))
        self.gridLayout.addWidget(self.disconnBtn, 5, 3, 1, 1)
        self.selectBox = QtGui.QComboBox(self.dockWidgetContents)
        self.selectBox.setObjectName(_fromUtf8("selectBox"))
        self.gridLayout.addWidget(self.selectBox, 4, 1, 1, 2)
        self.connectBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.connectBtn.setObjectName(_fromUtf8("connectBtn"))
        self.gridLayout.addWidget(self.connectBtn, 4, 3, 1, 1)
        self.refreshBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.refreshBtn.setObjectName(_fromUtf8("refreshBtn"))
        self.gridLayout.addWidget(self.refreshBtn, 5, 1, 1, 1)
        self.resetBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.resetBtn.setObjectName(_fromUtf8("resetBtn"))
        self.gridLayout.addWidget(self.resetBtn, 6, 3, 1, 1)
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 1, 1, 2)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8("cortera-logo.png")))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        BoardControl.setWidget(self.dockWidgetContents)

        self.retranslateUi(BoardControl)
        QtCore.QMetaObject.connectSlotsByName(BoardControl)

    def retranslateUi(self, BoardControl):
        BoardControl.setWindowTitle(_translate("BoardControl", "Connection", None))
        self.disconnBtn.setText(_translate("BoardControl", "Disconnect", None))
        self.connectBtn.setText(_translate("BoardControl", "Connect", None))
        self.refreshBtn.setText(_translate("BoardControl", "Refresh", None))
        self.resetBtn.setText(_translate("BoardControl", "Reset interface", None))
        self.label.setText(_translate("BoardControl", "Connected control modules:", None))

