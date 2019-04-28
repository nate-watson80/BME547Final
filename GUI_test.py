# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 17:46:15 2019

@author: Mars
"""
import os
import sys
import base64
import io
from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtWidgets import (QApplication,
                            QMainWindow,
                            QVBoxLayout,
                            QFileDialog)
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import cv2
import numpy as np
import requests
import json
import config
import csv

from encodedUi import Ui_MainWindow
from launch_dialog import LaunchDialog

# Change based on where server is deployed - Nate
baseURL = "http://127.0.0.1:5000/"
# baseURL = "http://vcm-9091.vm.duke.edu:5000/"


def decodeImage(str_encoded_img, color=False):
    """Function to decode input images.

    This function inputs an encoded image string that was
    uploaded by the user. This function accepts both color images
    as well as 16 bit images. Encoded images are decoded and returned
    back to the user.

    Args:
        str_encoded_img (str) = Encoded image string.

        color (bool) = Bool number to determine if file is
            a color file. Most images will be grayscale.

    Returns:
        orig_img () = Original image after it has been decoded

    """

    decoded_img = base64.b64decode(str_encoded_img)
    buf_img = io.BytesIO(decoded_img)
    if color:
        colr_img = cv2.imdecode(np.frombuffer(buf_img.read(),
                                              np.uint16),
                                cv2.IMREAD_COLOR)
        orig_img = cv2.cvtColor(colr_img, cv2.COLOR_BGR2RGB)
    else:
        orig_img = cv2.imdecode(np.frombuffer(buf_img.read(),
                                              np.uint16),
                                0)
    return orig_img


class MainWindow(QMainWindow, Ui_MainWindow):
    """ This is the UI class for the main GUI window.

    This class is to control the visual layouts of the main UI display.
    There are several buttons cooresponding to communicating with the server
    including selecting an image, uploading an image, and exporting data.
    Additionally, once images are uploaded they are displayed utilizing
    matplotlib imread() command.

    Args:
        QMainWindow (class) = PyQt main class inheritance

        Ui_MainWindow (class) = Class from the encodedUi.py file cooresponding
            to the functionality of all the widgets in window.

    Attributes:
        readImgButton (class 'PyQt5.QtWidgets.QPushButton') = button

        testServerButton (class 'PyQt5.QtWidgets.QPushButton') = button

        uploadImgButton (class 'PyQt5.QtWidgets.QPushButton') = button

        pullAllData (class 'PyQt5.QtWidgets.QPushButton') = button

        submitQuery (class 'PyQt5.QtWidgets.QPushButton') = button

        plotting_widget (class 'PyQt5.QtWidgets.QWidget') = button

        user (str) = String for the username

        batch (str) = String for the batch number

        img_grp (str) = Image group number

        location (str) = Manual entry of location taken.

    """
    def __init__(self, user, batch, img_grp, location, parent=None):
        """ Init function for the MainWindow class.

        Set up the atrributes on the UI and connect their functionalities.
        Note: A lot of their functionalities are already set in the
        encodedUi.py file.

        Args:
            user (str) = String for the username

            batch (str) = String for the batch number

            img_grp (str) = Image group number

            location (str) = Manual entry of location taken.

        Returns:
            None

        """
        # Inheritance of the MainWindow
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # Connect all of the button from Ui_MainWindow
        self.readImgButton.clicked.connect(self.openImage)
        self.testServerButton.clicked.connect(self.testServer)
        self.uploadImgButton.clicked.connect(self.uploadImage)
        self.pullAllData.clicked.connect(self.writeCSVData)
        self.submitQuery.clicked.connect(self.queryImage)
        self.plotting_widget.setLayout(QVBoxLayout())

        # Display the image that has been selected
        self.plotting_matplotlib_canvas = FigureCanvas(figure=Figure())
        self.plotting_widget.layout().addWidget(
                NavigationToolbar(self.plotting_matplotlib_canvas, self))
        self.plotting_widget.layout().addWidget(
                self.plotting_matplotlib_canvas)
        self.plot_ax = self.plotting_matplotlib_canvas.figure.subplots()
        self.plot_ax.axis('off')

        # Store the data obtained from launch window as attributes
        self.user = user
        self.batch = batch
        self.img_grp = img_grp
        self.location = location

    def openImage(self):
        newFilePath = QFileDialog.getOpenFileName(self)[0]
        if newFilePath == "":
            return
        if newFilePath.split('.')[-1] != "tiff":
            QtWidgets.QMessageBox.warning(self, 'Message',
                                          "Only a tiff file generated by \
                                          this device can be opened.",
                                          QtWidgets.QMessageBox.Ok)
            return

        self.filePath = newFilePath
        self.image = cv2.imread(newFilePath)
        self.plot_ax.clear()
        self.plot_ax.imshow(self.image, cmap='gray')
        self.plot_ax.axis('off')
        self.plot_ax.figure.canvas.draw()
        self.fileName.setText(QtWidgets.QApplication.translate("",
                                                               newFilePath,
                                                               None,
                                                               -1))

    def queryImage(self):
        URL = baseURL+"pullImage"
        response = requests.get(URL+self.lineEdit.text())
        verImage = decodeImage(response.json()["image"], color=True)
        self.plot_ax.clear()
        self.plot_ax.imshow(verImage, interpolation='nearest')
        self.plot_ax.axis('off')
        self.plot_ax.figure.canvas.draw()
        string = "Showing queried file from server: " + self.lineEdit.text()
        self.serverResponse.setText(QtWidgets.QApplication.translate("",
                                                                     string,
                                                                     None,
                                                                     -1))

    def writeCSVData(self):
        URL = baseURL+"pullAllData"
        response = requests.get(URL)
        outLines = []
        for iterator, eachEntry in enumerate(response.json()['filename']):
            eachLine = [response.json()['filename'][iterator]]
            eachLine.append("spots: ")
            for eachSpot in response.json()['spots'][iterator]:
                eachLine.append(eachSpot)
            eachLine.append("background: ")
            eachLine.append(response.json()['background'][iterator])
            outLines.append(eachLine)
        with open('outputData.csv', 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(outLines)
        string = "all available image data written to outputData.csv"
        self.serverResponse.setText(QtWidgets.QApplication.translate("",
                                                                     string,
                                                                     None,
                                                                     -1))

    def uploadImage(self):
        with open(self.filePath, "rb") as image_file:
            b64_imageBytes = base64.b64encode(image_file.read())
        b64_imgString = str(b64_imageBytes, encoding='utf-8')
        URL = baseURL+"imageUpload"
        payload = {
                   "client": "GUI-test",
                   "image": b64_imgString,
                   "user": self.user,
                   "img_grp": self.img_grp,
                   "batch": self.batch,
                   "location": self.location,
                   "filename": self.filePath.split('/')[-1]
                  }
        response = requests.post(URL, json=payload)
        image_rgb = decodeImage(response.json()['ver_Img'], color=True)
        self.plot_ax.clear()
        self.plot_ax.imshow(image_rgb, interpolation='nearest')
        self.plot_ax.axis('off')
        self.plot_ax.figure.canvas.draw()

        string = "results: " + str(response.json()['intensities']) + "\n" \
            + "background: " + str(response.json()['background'])
        self.serverResponse.setText(QtWidgets.QApplication.translate("",
                                                                     string,
                                                                     None,
                                                                     -1))

    def testServer(self):
        URL = baseURL
        response = requests.get(URL).text
        self.serverResponse.setText(QtWidgets.QApplication.translate("",
                                                                     response,
                                                                     None,
                                                                     -1))
        pass

    # process the image and then send it back


def main():
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    app.setWindowIcon(QtGui.QIcon(config.ICON))
    app.setApplicationName(config.TITLE)
    window = LaunchDialog()
    data = window.get_data()
    USER = data['user']
    BATCH = data['batch']
    IMG_GROUP = data['img_grp']
    LOCATION = data['location']
    if USER and BATCH and IMG_GROUP and LOCATION:
        frame = MainWindow(USER, BATCH, IMG_GROUP, LOCATION)
        frame.setWindowTitle(config.TITLE)
        frame.show()
        app.exec_()
    app.quit()

if __name__ == '__main__':
    main()
