# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'powercontrol.ui'
#
# Created: Fri Jul 31 14:53:25 2015
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

class Ui_PowerControl(object):
    def setupUi(self, PowerControl):
        PowerControl.setObjectName(_fromUtf8("PowerControl"))
        PowerControl.resize(242, 181)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_5 = QtGui.QLabel(self.dockWidgetContents)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.dockWidgetContents)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.vdd3doubleSpinBox = QtGui.QDoubleSpinBox(self.dockWidgetContents)
        self.vdd3doubleSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.vdd3doubleSpinBox.setMinimum(3.0)
        self.vdd3doubleSpinBox.setMaximum(3.6)
        self.vdd3doubleSpinBox.setSingleStep(0.05)
        self.vdd3doubleSpinBox.setProperty("value", 3.3)
        self.vdd3doubleSpinBox.setObjectName(_fromUtf8("vdd3doubleSpinBox"))
        self.gridLayout.addWidget(self.vdd3doubleSpinBox, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 1)
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.i1doubleSpinBox = QtGui.QDoubleSpinBox(self.dockWidgetContents)
        self.i1doubleSpinBox.setReadOnly(True)
        self.i1doubleSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.i1doubleSpinBox.setDecimals(0)
        self.i1doubleSpinBox.setObjectName(_fromUtf8("i1doubleSpinBox"))
        self.gridLayout.addWidget(self.i1doubleSpinBox, 3, 0, 1, 1)
        self.i0doubleSpinBox = QtGui.QDoubleSpinBox(self.dockWidgetContents)
        self.i0doubleSpinBox.setReadOnly(True)
        self.i0doubleSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.i0doubleSpinBox.setDecimals(0)
        self.i0doubleSpinBox.setObjectName(_fromUtf8("i0doubleSpinBox"))
        self.gridLayout.addWidget(self.i0doubleSpinBox, 1, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.dockWidgetContents)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.vddhdoubleSpinBox = QtGui.QDoubleSpinBox(self.dockWidgetContents)
        self.vddhdoubleSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.vddhdoubleSpinBox.setMinimum(6.7)
        self.vddhdoubleSpinBox.setMaximum(11.9)
        self.vddhdoubleSpinBox.setSingleStep(0.1)
        self.vddhdoubleSpinBox.setProperty("value", 9.0)
        self.vddhdoubleSpinBox.setObjectName(_fromUtf8("vddhdoubleSpinBox"))
        self.gridLayout.addWidget(self.vddhdoubleSpinBox, 5, 1, 1, 1)
        self.i2doubleSpinBox = QtGui.QDoubleSpinBox(self.dockWidgetContents)
        self.i2doubleSpinBox.setReadOnly(True)
        self.i2doubleSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.i2doubleSpinBox.setDecimals(0)
        self.i2doubleSpinBox.setObjectName(_fromUtf8("i2doubleSpinBox"))
        self.gridLayout.addWidget(self.i2doubleSpinBox, 5, 0, 1, 1)
        self.vdd1enButton = QtGui.QPushButton(self.dockWidgetContents)
        self.vdd1enButton.setCheckable(True)
        self.vdd1enButton.setObjectName(_fromUtf8("vdd1enButton"))
        self.gridLayout.addWidget(self.vdd1enButton, 1, 2, 1, 1)
        self.vdd3enButton = QtGui.QPushButton(self.dockWidgetContents)
        self.vdd3enButton.setCheckable(True)
        self.vdd3enButton.setObjectName(_fromUtf8("vdd3enButton"))
        self.gridLayout.addWidget(self.vdd3enButton, 3, 2, 1, 1)
        self.vdd1doubleSpinBox = QtGui.QDoubleSpinBox(self.dockWidgetContents)
        self.vdd1doubleSpinBox.setMinimum(0.95)
        self.vdd1doubleSpinBox.setMaximum(1.6)
        self.vdd1doubleSpinBox.setSingleStep(0.05)
        self.vdd1doubleSpinBox.setProperty("value", 1.2)
        self.vdd1doubleSpinBox.setObjectName(_fromUtf8("vdd1doubleSpinBox"))
        self.gridLayout.addWidget(self.vdd1doubleSpinBox, 1, 1, 1, 1)
        PowerControl.setWidget(self.dockWidgetContents)

        self.retranslateUi(PowerControl)
        QtCore.QMetaObject.connectSlotsByName(PowerControl)

    def retranslateUi(self, PowerControl):
        PowerControl.setWindowTitle(_translate("PowerControl", "Power Control", None))
        self.label_5.setText(_translate("PowerControl", "VDDH", None))
        self.label_6.setText(_translate("PowerControl", "I2", None))
        self.vdd3doubleSpinBox.setSuffix(_translate("PowerControl", " V", None))
        self.label.setText(_translate("PowerControl", "VDD1", None))
        self.label_2.setText(_translate("PowerControl", "VDD3", None))
        self.label_3.setText(_translate("PowerControl", "I1", None))
        self.i1doubleSpinBox.setSuffix(_translate("PowerControl", " uA", None))
        self.i0doubleSpinBox.setSuffix(_translate("PowerControl", " uA", None))
        self.label_4.setText(_translate("PowerControl", "I0", None))
        self.vddhdoubleSpinBox.setSuffix(_translate("PowerControl", " V", None))
        self.i2doubleSpinBox.setSuffix(_translate("PowerControl", " uA", None))
        self.vdd1enButton.setText(_translate("PowerControl", "Enable", None))
        self.vdd3enButton.setText(_translate("PowerControl", "Enable", None))
        self.vdd1doubleSpinBox.setSuffix(_translate("PowerControl", " V", None))

