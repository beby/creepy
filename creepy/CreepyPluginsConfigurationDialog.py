# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pluginsConfig.ui'
#
# Created: Mon Jan 21 21:18:21 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PluginsConfigurationDialog(object):
    def setupUi(self, PluginsConfigurationDialog):
        PluginsConfigurationDialog.setObjectName(_fromUtf8("PluginsConfigurationDialog"))
        PluginsConfigurationDialog.resize(810, 640)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PluginsConfigurationDialog.sizePolicy().hasHeightForWidth())
        PluginsConfigurationDialog.setSizePolicy(sizePolicy)
        PluginsConfigurationDialog.setMinimumSize(QtCore.QSize(810, 640))
        PluginsConfigurationDialog.setMaximumSize(QtCore.QSize(810, 640))
        self.BtnBox = QtGui.QDialogButtonBox(PluginsConfigurationDialog)
        self.BtnBox.setGeometry(QtCore.QRect(430, 600, 341, 32))
        self.BtnBox.setOrientation(QtCore.Qt.Horizontal)
        self.BtnBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.BtnBox.setObjectName(_fromUtf8("BtnBox"))
        self.PluginsList = QtGui.QListView(PluginsConfigurationDialog)
        self.PluginsList.setGeometry(QtCore.QRect(10, 10, 211, 581))
        self.PluginsList.setEditTriggers(QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.PluginsList.setObjectName(_fromUtf8("PluginsList"))

        self.retranslateUi(PluginsConfigurationDialog)
        QtCore.QObject.connect(self.BtnBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PluginsConfigurationDialog.accept)
        QtCore.QObject.connect(self.BtnBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PluginsConfigurationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PluginsConfigurationDialog)

    def retranslateUi(self, PluginsConfigurationDialog):
        PluginsConfigurationDialog.setWindowTitle(QtGui.QApplication.translate("PluginsConfigurationDialog", "Plugins Configuration", None, QtGui.QApplication.UnicodeUTF8))

