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

        # Connect all of the button from Ui_MainWindow to functions
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
        """ Method for opening images that have been selected from OS

        This function is used for the UI to open up the image that has been
        selected from the computer. It functions primarily by using the
        getOpenFileName method that is from the QFileDialog class in PyQt.
        Next, logical operations are run to see if the file is a tiff file.
        For D4 images, tiff files are the only file format that is accepted
        as input. Image is then plotted using matplotlib.

        Args:
            None

        Returns:
            None

        """
        newFilePath = QFileDialog.getOpenFileName(self)[0]

        # Ensure a file has been selected
        if newFilePath == "":
            return

        # Check to see if file has the .tiff image extension
        if newFilePath.split('.')[-1] != "tiff":
            out_message = "Only a tiff files are able to be opened."
            QtWidgets.QMessageBox.warning(self,
                                          'Message',
                                          out_message,
                                          QtWidgets.QMessageBox.Ok)
            return

        # Use matplotlib to display the image that has been uploaded
        self.filePath = newFilePath
        self.image = cv2.imread(newFilePath)
        self.plot_ax.clear()
        self.plot_ax.imshow(self.image, cmap='gray')
        self.plot_ax.axis('off')
        self.plot_ax.figure.canvas.draw()

        # Return file name back to blank text string
        self.fileName.setText(QtWidgets.QApplication.translate("",
                                                               newFilePath,
                                                               None,
                                                               -1))

    def queryImage(self):
        """ Method for querying the database for stored images.

        This function is associated with the get image button. This image
        takes in a string from the text box and will send a request to the
        server in order to obtain the image. Next, it will display the image
        utilizing matplotlib once it has been fetched from the server.

        Args:
            None

        Returns:
            None

        """
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
        """ Function to write the pulled data into a CSV file format.

        This function will respond to the pull all data button in the main
        window UI. Effectively this function will return all of the data that
        has been previously stored on the server. The raw data that has been
        obtained will then be exported to a CSV file.

        Args:
            None

        Returns:
            None

        """
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
        """ Function attached to the upload image button.

        This function is tied to the upload image to server function. The
        way that this works is via a requests.post command of a payload
        containing the client, image file, username, group number, batch,
        location, and filename. The iamge is encoded to utf-8 format prior
        to sending out. The response that the post request will recieve will
        be the results of the image including the mean spot intensities as well
        as the background intensities.

        Args:
            None

        Returns:
            None

        """
        # Encode the image file in base 64:
        with open(self.filePath, "rb") as image_file:
            b64_imageBytes = base64.b64encode(image_file.read())
        b64_imgString = str(b64_imageBytes, encoding='utf-8')
        URL = baseURL+"imageUpload"

        # Create the payload dictionary
        payload = {
                   "client": "GUI-test",
                   "image": b64_imgString,
                   "user": self.user,
                   "img_grp": self.img_grp,
                   "batch": self.batch,
                   "location": self.location,
                   "filename": self.filePath.split('/')[-1]
                  }

        # Send the payload to the server
        response = requests.post(URL, json=payload)
        image_rgb = decodeImage(response.json()['ver_Img'], color=True)
        # Clear the image
        self.plot_ax.clear()
        self.plot_ax.imshow(image_rgb, interpolation='nearest')
        self.plot_ax.axis('off')
        self.plot_ax.figure.canvas.draw()

        # Display the responses of from the analyzed image files.
        string = "results: " + str(response.json()['intensities']) + "\n" \
            + "background: " + str(response.json()['background'])

        # Clear the textbox:
        self.serverResponse.setText(QtWidgets.QApplication.translate("",
                                                                     string,
                                                                     None,
                                                                     -1))

    def testServer(self):
        """ Function attached to the test the server button

        Simply this function will test to see if the server is up and running.
        Will display text to verify that the server is up and running.

        Args:
            None

        Returns:
            None

        """
        URL = baseURL
        response = requests.get(URL).text
        self.serverResponse.setText(QtWidgets.QApplication.translate("",
                                                                     response,
                                                                     None,
                                                                     -1))
        pass


def main():
    """ Main operating script

    main() is the main function that is calling the other procedures and
    functions. First, it will call the LaunchWindow() class and display and
    wait for the proper user inputs. Next, it will open the main UI window.
    In this window, all of the image processing tasks can be completed if
    necesssary.

    Args:
        None

    Returns:
        None

        """
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    # Display the config.py file
    app.setWindowIcon(QtGui.QIcon(config.ICON))
    app.setApplicationName(config.TITLE)

    # Call the launch windows
    window = LaunchDialog()

    # Obtain data from launch window
    user, batch, img_group, location = get_launch_data(window)

    if user and batch and img_group and location:
        frame = MainWindow(user, batch, img_group, location)
        frame.setWindowTitle(config.TITLE)
        frame.show()
        app.exec_()
    else:
        app.quit()


def get_launch_data(window):
    """ Function to obtain the data that was entered in launch window

    This function is utilized to obtain the data that was entered by the
    client in the launch window. This works by going into the window class
    and running the get_data() method. The data is then parsed from the dict
    and returned.

        Args:
            window (class) = LaunchDialog class that was begun in main()

        Returns:
            user (str) = String containing the username

            batch (str) = String containing the batch name

            img_grp (str) = String containing the image group

            location (str) = String containing location data

    """
    data = window.get_data()
    user = data['user']
    batch = data['batch']
    img_grp = data['img_grp']
    location = data['location']

    return user, batch, img_grp, location

if __name__ == '__main__':
    """ Main driver calling the other procedures

        Args:
            None

        Returns:
            None

    """
    main()
