# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'registereditor_fileIO.ui'
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

class Ui_RegisterEditor(object):
    def setupUi(self, RegisterEditor):
        RegisterEditor.setObjectName(_fromUtf8("RegisterEditor"))
        RegisterEditor.resize(530, 329)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.dockWidgetContents.setStyleSheet('font-size: 12pt;')
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea = QtGui.QScrollArea(self.dockWidgetContents)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 510, 227))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout.setHorizontalSpacing(0)
        self.label_4 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.label = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.line = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 0, 1, 4)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.txtWriteButton = QtGui.QPushButton(self.dockWidgetContents)
        self.txtWriteButton.setObjectName(_fromUtf8("txtWriteButton"))
        self.gridLayout_2.addWidget(self.txtWriteButton, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.writeButton = QtGui.QPushButton(self.dockWidgetContents)
        self.writeButton.setObjectName(_fromUtf8("writeButton"))
        self.gridLayout_2.addWidget(self.writeButton, 2, 3, 1, 1)
        self.readButton = QtGui.QPushButton(self.dockWidgetContents)
        self.readButton.setObjectName(_fromUtf8("readButton"))
        self.gridLayout_2.addWidget(self.readButton, 0, 3, 1, 1)
        self.txtReadButton = QtGui.QPushButton(self.dockWidgetContents)
        self.txtReadButton.setFlat(False)
        self.txtReadButton.setObjectName(_fromUtf8("txtReadButton"))
        self.gridLayout_2.addWidget(self.txtReadButton, 0, 0, 1, 1)
        self.writeAllBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.writeAllBtn.setObjectName(_fromUtf8("writeAllBtn"))
        self.gridLayout_2.addWidget(self.writeAllBtn, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        RegisterEditor.setWidget(self.dockWidgetContents)

        self.retranslateUi(RegisterEditor)
        QtCore.QMetaObject.connectSlotsByName(RegisterEditor)

    def retranslateUi(self, RegisterEditor):
        RegisterEditor.setWindowTitle(_translate("RegisterEditor", "Registers", None))
        self.label_4.setText(_translate("RegisterEditor", "Write", None))
        self.label.setText(_translate("RegisterEditor", "Addr", None))
        self.label_2.setText(_translate("RegisterEditor", "Name", None))
        self.label_3.setText(_translate("RegisterEditor", "Value", None))
        self.txtWriteButton.setText(_translate("RegisterEditor", "Write to File", None))
        self.writeButton.setText(_translate("RegisterEditor", "Write", None))
        self.readButton.setText(_translate("RegisterEditor", "Read", None))
        self.txtReadButton.setText(_translate("RegisterEditor", "Read from File", None))
        self.writeAllBtn.setText(_translate("RegisterEditor", "Write All", None))

