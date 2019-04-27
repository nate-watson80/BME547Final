# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test-jason.ui'
#
# Created: Thu Feb 21 19:56:42 2019
#      by: qtpy-uic 2.0.4
#
# WARNING! All changes made in this file will be lost!

from qtpy import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    """ Class for the UI of the main window.

    This class is designed to provide the layout of the main user
    interface window. This window was written following the QtPy
    UI framework. The basic layout of this window contains several
    buttons in order to upload files to the server, open images that
    have been previously been uploaded as well as process the spots to
    understand the test results.

    """
    def setupUi(self, MainWindow):
        """ Method setting up the locations and layout of UI

        This method is utilized to set up the location and visualization
        of the main user interface. All buttons, labels, and functionalities
        are set here. This method can be called to set up the GUI upon calling
        the class. 

        Args:
            MainWindow (class) = Class cooresponding to the main UI
                window.

        Returns:
            None

        """

        # Main window init/size
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        # Various button and plotting widgets
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
        self.serverResponse.setMaximumHeight(45)
        self.verticalLayout.addWidget(self.serverResponse)

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)

        self.submitQuery = QtWidgets.QPushButton(self.centralwidget)
        self.submitQuery.setObjectName("submitQuery")
        self.verticalLayout.addWidget(self.submitQuery)

        self.readImgButton = QtWidgets.QPushButton(self.centralwidget)
        self.readImgButton.setObjectName("readImgButton")
        self.verticalLayout.addWidget(self.readImgButton)

        self.uploadImgButton = QtWidgets.QPushButton(self.centralwidget)
        self.uploadImgButton.setObjectName("uploadImgButton")
        self.verticalLayout.addWidget(self.uploadImgButton)

        self.testServerButton = QtWidgets.QPushButton(self.centralwidget)
        self.testServerButton.setObjectName("testServerButton")
        self.verticalLayout.addWidget(self.testServerButton)

        self.pullAllData = QtWidgets.QPushButton(self.centralwidget)
        self.pullAllData.setObjectName("pullAllData")
        self.verticalLayout.addWidget(self.pullAllData)

        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 17))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Call retranslate method to add text labels
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """ Method adding text onto the various widgets

        This method is designed to add text to the the various
        widgets that were defied in the Ui_MainWindow class. These
        buttons allow for user interactions with the server.

        Args:
            MainWindow (class) = Class cooresponding to the main UI
                window.

        Returns:
            None

        """
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate(
            "", "MainWindow", None, -1))
        self.readImgButton.setText(QtWidgets.QApplication.translate(
            "", "Open Image", None, -1))
        self.uploadImgButton.setText(QtWidgets.QApplication.translate(
            "", "Upload Image to Server", None, -1))
        self.fileName.setText(QtWidgets.QApplication.translate(
            "", "Press 'Open Image' button'", None, -1))
        self.pullAllData.setText(QtWidgets.QApplication.translate(
            "", "Pull Data to outputData.csv", None, -1))
        self.submitQuery.setText(QtWidgets.QApplication.translate(
            "", "View entered filename from server", None, -1))
        self.testServerButton.setText(
            QtWidgets.QApplication.translate("", "Test Server!", None, -1))
