# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pluginConfigCheckDialog.ui'
#
# Created: Wed Jan 23 21:08:13 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_checkPluginConfigurationDialog(object):
    def setupUi(self, checkPluginConfigurationDialog):
        checkPluginConfigurationDialog.setObjectName(_fromUtf8("checkPluginConfigurationDialog"))
        checkPluginConfigurationDialog.resize(378, 222)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(checkPluginConfigurationDialog.sizePolicy().hasHeightForWidth())
        checkPluginConfigurationDialog.setSizePolicy(sizePolicy)
        checkPluginConfigurationDialog.setMinimumSize(QtCore.QSize(378, 222))
        checkPluginConfigurationDialog.setMaximumSize(QtCore.QSize(378, 222))
        checkPluginConfigurationDialog.setModal(True)
        self.checkPluginConfigurationButtonBox = QtGui.QDialogButtonBox(checkPluginConfigurationDialog)
        self.checkPluginConfigurationButtonBox.setGeometry(QtCore.QRect(30, 176, 341, 32))
        self.checkPluginConfigurationButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.checkPluginConfigurationButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.checkPluginConfigurationButtonBox.setObjectName(_fromUtf8("checkPluginConfigurationButtonBox"))
        self.horizontalLayoutWidget = QtGui.QWidget(checkPluginConfigurationDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 40, 271, 121))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.checkPluginConfigurationHorizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.checkPluginConfigurationHorizontalLayout.setMargin(0)
        self.checkPluginConfigurationHorizontalLayout.setObjectName(_fromUtf8("checkPluginConfigurationHorizontalLayout"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.checkPluginConfigurationHorizontalLayout.addWidget(self.label)

        self.retranslateUi(checkPluginConfigurationDialog)
        QtCore.QObject.connect(self.checkPluginConfigurationButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), checkPluginConfigurationDialog.accept)
        QtCore.QObject.connect(self.checkPluginConfigurationButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), checkPluginConfigurationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(checkPluginConfigurationDialog)

    def retranslateUi(self, checkPluginConfigurationDialog):
        checkPluginConfigurationDialog.setWindowTitle(QtGui.QApplication.translate("checkPluginConfigurationDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("checkPluginConfigurationDialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

