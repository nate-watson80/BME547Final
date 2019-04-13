# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 17:46:15 2019

@author: Mars
"""
import os, sys, base64, io
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

from encodedUi import Ui_MainWindow
from launch_dialog import LaunchDialog

USER = None
BATCH = None
IMG_GROUP = None

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.readImgButton.clicked.connect(self.openImage)
        self.testServerButton.clicked.connect(self.testServer)
        self.uploadImgButton.clicked.connect(self.uploadImage)
        #self.lineEdit.editingFinished.connect(self.goodbyeWorld)
        self.plotting_widget.setLayout(QVBoxLayout())
            
        self.plotting_matplotlib_canvas = FigureCanvas(figure=Figure())
        self.plotting_widget.layout().addWidget(
                NavigationToolbar(self.plotting_matplotlib_canvas, self))
            
        self.plotting_widget.layout().addWidget(
                self.plotting_matplotlib_canvas)
        self.plot_ax = self.plotting_matplotlib_canvas.figure.subplots()
        self.plot_ax.axis('off')

    def openImage(self):
        self.filePath = QFileDialog.getOpenFileName(self)[0]
        print("file path: " + str(self.filePath))
        self.image = cv2.imread(self.filePath)
        self.plot_ax.imshow(self.image, cmap='gray')
        self.plot_ax.axis('off')
        self.plot_ax.figure.canvas.draw()
        self.fileName.setText(QtWidgets.QApplication.translate("", self.filePath, None, -1))
    
    def uploadImage(self):
        with open(self.filePath, "rb") as image_file:
            b64_imageBytes = base64.b64encode(image_file.read())
        b64_imgString = str(b64_imageBytes, encoding='utf-8')
        URL = "http://127.0.0.1:5000/imageUpload"
        payload = {"client" : "GUI-test",
                   "image" : b64_imgString,
                   "user": USER,
                   "img_grp": IMG_GROUP,
                   "batch": BATCH}
        response = requests.post(URL, json=payload).text
        self.serverResponse.setText(QtWidgets.QApplication.translate("", response, None, -1))
        
    def testServer(self):
        URL = "http://127.0.0.1:5000/"
        response = requests.get(URL).text
        self.serverResponse.setText(QtWidgets.QApplication.translate("", response, None, -1))
        pass
        
    ## process the image and then send it back

def main():
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    app.setWindowIcon(QtGui.QIcon(config.ICON))
    window = LaunchDialog()
    data = window.get_data()
    USER, BATCH, IMG_GROUP = data['user'], data['batch'], data['img_grp']
    if USER and BATCH and IMG_GROUP: 
        frame = MainWindow()
        frame.setWindowTitle(config.TITLE)
        frame.show()
        app.exec_()
    app.quit()

if __name__ == '__main__':
    main()
