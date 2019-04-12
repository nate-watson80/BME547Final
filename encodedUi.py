# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test-jason.ui'
#
# Created: Thu Feb 21 19:56:42 2019
#      by: qtpy-uic 2.0.4
#
# WARNING! All changes made in this file will be lost!

from qtpy import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plotting_widget = QtWidgets.QWidget(self.centralwidget)
        self.plotting_widget.setObjectName("plotting_widget")
        self.verticalLayout.addWidget(self.plotting_widget)
        
        self.fileName = QtWidgets.QLabel(self.centralwidget)
        self.fileName.setObjectName("fileName")
        self.fileName.setAlignment(QtCore.Qt.AlignCenter)
        self.fileName.setMaximumHeight(20)
        self.verticalLayout.addWidget(self.fileName)
        
        self.serverResponse = QtWidgets.QLabel(self.centralwidget)
        self.serverResponse.setObjectName("serverResponse")
        self.serverResponse.setAlignment(QtCore.Qt.AlignCenter)
        self.serverResponse.setMaximumHeight(20)
        self.verticalLayout.addWidget(self.serverResponse)
        
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)

        self.readImgButton = QtWidgets.QPushButton(self.centralwidget)
        self.readImgButton.setObjectName("readImgButton")
        self.verticalLayout.addWidget(self.readImgButton)
        
        self.uploadImgButton = QtWidgets.QPushButton(self.centralwidget)
        self.uploadImgButton.setObjectName("uploadImgButton")
        self.verticalLayout.addWidget(self.uploadImgButton )
        
        self.testServerButton = QtWidgets.QPushButton(self.centralwidget)
        self.testServerButton.setObjectName("testServerButton")
        self.verticalLayout.addWidget(self.testServerButton)
        
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 17))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("", "MainWindow", None, -1))
        self.readImgButton.setText(QtWidgets.QApplication.translate("", "Open Image", None, -1))
        self.uploadImgButton.setText(QtWidgets.QApplication.translate("", "Upload Image to Server", None, -1))
        self.fileName.setText(QtWidgets.QApplication.translate("", "Press 'Open Image' button'", None, -1))
        self.testServerButton.setText(QtWidgets.QApplication.translate("", "Test Server!", None, -1))
        