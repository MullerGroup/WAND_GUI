# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/boardcontrol.ui'
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

class Ui_BoardControl(object):
    def setupUi(self, BoardControl):
        BoardControl.setObjectName(_fromUtf8("BoardControl"))
        BoardControl.resize(455, 300)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8("cortera-logo.png")))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)
        self.selectBox = QtGui.QComboBox(self.dockWidgetContents)
        self.selectBox.setObjectName(_fromUtf8("selectBox"))
        self.gridLayout.addWidget(self.selectBox, 3, 0, 1, 2)
        self.connectBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.connectBtn.setObjectName(_fromUtf8("connectBtn"))
        self.gridLayout.addWidget(self.connectBtn, 3, 2, 1, 1)
        self.refreshBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.refreshBtn.setObjectName(_fromUtf8("refreshBtn"))
        self.gridLayout.addWidget(self.refreshBtn, 4, 0, 1, 1)
        self.flushCommandBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.flushCommandBtn.setObjectName(_fromUtf8("flushCommandBtn"))
        self.gridLayout.addWidget(self.flushCommandBtn, 4, 1, 1, 1)
        self.disconnBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.disconnBtn.setEnabled(False)
        self.disconnBtn.setObjectName(_fromUtf8("disconnBtn"))
        self.gridLayout.addWidget(self.disconnBtn, 4, 2, 1, 1)
        self.flushDataBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.flushDataBtn.setObjectName(_fromUtf8("flushDataBtn"))
        self.gridLayout.addWidget(self.flushDataBtn, 5, 1, 1, 1)
        self.resetBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.resetBtn.setObjectName(_fromUtf8("resetBtn"))
        self.gridLayout.addWidget(self.resetBtn, 5, 2, 1, 1)
        BoardControl.setWidget(self.dockWidgetContents)

        self.retranslateUi(BoardControl)
        QtCore.QMetaObject.connectSlotsByName(BoardControl)

    def retranslateUi(self, BoardControl):
        BoardControl.setWindowTitle(_translate("BoardControl", "Connection", None))
        self.label.setText(_translate("BoardControl", "Connected control modules:", None))
        self.connectBtn.setText(_translate("BoardControl", "Connect", None))
        self.refreshBtn.setText(_translate("BoardControl", "Refresh", None))
        self.flushCommandBtn.setText(_translate("BoardControl", "Flush command FIFO", None))
        self.disconnBtn.setText(_translate("BoardControl", "Disconnect", None))
        self.flushDataBtn.setText(_translate("BoardControl", "Flush data FIFO", None))
        self.resetBtn.setText(_translate("BoardControl", "Reset interface", None))

