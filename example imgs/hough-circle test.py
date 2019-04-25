import os, sys, base64, io
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib import pyplot
import cv2
import numpy as np
import requests
import json

arrayCoords = []
def mouseLocationClick(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("           click identified at: " +str([x,y])+ " with " +str(len(arrayCoords)+1)+" coordinates saved")
        arrayCoords.append([x,y]) # horizontal position, then vertical position within an image


def cvWindow(nameOfWindow, imageToShow, keypressBool):
    print("----------Displaying: "
          + str(nameOfWindow)
          + "    ----------")
    cv2.namedWindow(nameOfWindow, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(nameOfWindow, mouseLocationClick)
    cv2.imshow(nameOfWindow, imageToShow)
    pressedKey = cv2.waitKey(0)
    cv2.destroyAllWindows()
    if keypressBool:
        return pressedKey


def circlePixelID(circleData): # output pixel locations of all circles within the list,
    pixelLocations = []
    xCoordCirc = circleData[0] # separates the x and y coordinates of the center of the circles and the circle radius 
    yCoordCirc = circleData[1]
    radiusCirc = circleData[2]
    for exesInCircle in range(( xCoordCirc - radiusCirc ),( xCoordCirc + radiusCirc )):
        whyRange = np.sqrt(pow(radiusCirc,2) - pow((exesInCircle - xCoordCirc),2)) #calculates the y-coordinates that define the top and bottom bounds of a slice (at x position) of the circle 
        discreteWhyRange = int(whyRange) 
        for whysInCircle in range(( yCoordCirc - discreteWhyRange),( yCoordCirc + discreteWhyRange)):
            pixelLocations.append([exesInCircle,whysInCircle])
    return pixelLocations


with open("slide1_8.tiff", "rb") as image_file:
    b64_imageEnc = base64.b64encode(image_file.read())
imgDec = base64.b64decode(b64_imageEnc)
image_buf = io.BytesIO(imgDec)

rawImg16b = cv2.imdecode(np.frombuffer(image_buf.read(),
                                       np.uint16),
                         0)
#cvWindow('test-rawimg',
#         rawImg16b,
#         False)
verImg = cv2.cvtColor(rawImg16b.copy(),
                      cv2.COLOR_GRAY2RGB)

# need to convert img to 8 bit for circle finding
rows = 2064
cols = 3088
img8b = cv2.normalize(rawImg16b.copy(),
                      np.zeros(shape=(rows,cols)),
                      0,255,
                      norm_type = cv2.NORM_MINMAX,
                      dtype = cv2.CV_8U)

smoothedIMG = cv2.medianBlur(img8b,3)
circlesD = cv2.HoughCircles(smoothedIMG,
                            cv2.HOUGH_GRADIENT,1,
                            minDist = 80,
                            param1=15,
                            param2=21,
                            minRadius=28,
                            maxRadius=32)
circlesX = np.uint16(np.around(circlesD))
circles = circlesX[0]

calibrationBrightness = []
for eachCircle in circles:
    #print(str(eachCircle))
    pixelLocsForCircle = circlePixelID([eachCircle[0],eachCircle[1],eachCircle[2]])
    pixelIntensities = []
    for eachPixel in pixelLocsForCircle:
        pixelIntensities.append(rawImg16b[eachCircle[1],eachCircle[0]])
    avgIntensity = round(np.array(pixelIntensities).mean(),4)
    calibrationBrightness.append([eachCircle[0],eachCircle[1],avgIntensity])
    #print(calibrationBrightness)
    
    cv2.circle(verImg,
               (eachCircle[0], eachCircle[1]),
                eachCircle[2],
                (0,0,255),
                2)

cvWindow("verification of circles found in calibration image",verImg,False)

