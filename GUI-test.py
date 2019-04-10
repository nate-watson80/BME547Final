# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 17:46:15 2019

@author: Mars
"""
import os, sys
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
from encodedUi import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.openImage)
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
        filePath = QFileDialog.getOpenFileName(self)[0]
        print("file path: " + str(filePath))
        self.image = cv2.imread(filePath)
        self.plot_ax.imshow(self.image)
        self.plot_ax.axis('off')
        self.plot_ax.figure.canvas.draw()


def main():
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    frame = MainWindow()
    frame.setWindowTitle('D4 Analysis Client')
    
    frame.show()
    app.exec_()


if __name__ == '__main__':
    main()
