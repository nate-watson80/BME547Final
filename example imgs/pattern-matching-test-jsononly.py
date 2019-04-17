# pattern matching simple

# import libraries 
import numpy as np 
import cv2
import sys
import csv
from operator import itemgetter

# for plotting, import these things
import numpy as np
import matplotlib.pyplot as plt
import json


arrayCoords = []
def mouseLocationClick(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("click identified at: " +str([x,y]))
        arrayCoords.append([x,y])
        
def pullElementsFromList(datList,argument): # use this when you have a 2d list and want a specific element from each entry
    return [thatSpecificArgument[argument] for thatSpecificArgument in datList]
  
def circleDistanceSorter(circleArray,position,numberofCaptSpots):
    dist = []
    for i in circleArray[0,:]: # calculates the distance from each circle to the center of the array
        distanceFromCenter = np.sqrt( pow((i[0] - position[0]),2) + pow((i[1] - position[1]),2) )
        dist.append(distanceFromCenter) # stores those values into an array
    pointers = range(len(circleArray[0,:])) # makes a pointer array that matches the pointers in the "circle" list
    closestCirclesPointers = sorted(zip(dist,pointers),reverse=False) # sorts and returns the sorted list [distance,pointers]
    sortedCirclesFromCenter = circleArray[0,pullElementsFromList(closestCirclesPointers,1)] # returns the circle List entries sorted by distance using the pointers to the circle List
    captureSpots = sortedCirclesFromCenter[:numberofCaptSpots]
    sortedCaptureSpotsByWhy = sorted(captureSpots, key = itemgetter(1))
    maxCircleRadius = max(pullElementsFromList(sortedCaptureSpotsByWhy,2))
    yCoordinateRowOfCircles= sortedCaptureSpotsByWhy[0][1]
    fullySortedList = []
    rowCircleList = []
    for eachCircle in sortedCaptureSpotsByWhy:
        #print(eachCircle)
        if (abs(eachCircle[1]-yCoordinateRowOfCircles) < maxCircleRadius):
            rowCircleList.append(eachCircle)
            #print(str(eachCircle) + " added")
        else:
            rowCirclesSortedByX = sorted(rowCircleList, key = itemgetter(0))
            fullySortedList = fullySortedList + rowCirclesSortedByX
            #print(str(rowCircleList) + " flushed")
            rowCircleList = []
            yCoordinateRowOfCircles = eachCircle[1]
            rowCircleList.append(eachCircle)
    rowCirclesSortedByX = sorted(rowCircleList, key = itemgetter(0))
    fullySortedList = fullySortedList + rowCirclesSortedByX
    #print(str(rowCircleList) + " flushed")
#    print(fullySortedList)        
    return fullySortedList

def circlePixelID(circleData): # output pixel locations of all circles within the list,    pixelLocations = []
    xCoordCirc = circleData[0] # separates the x and y coordinates of the center of the circles and the circle radius 
    yCoordCirc = circleData[1]
    radiusCirc = circleData[2]
    pixelLocations = []
    for exesInCircle in range(( xCoordCirc - radiusCirc ),( xCoordCirc + radiusCirc )):
        whyRange = np.sqrt(pow(radiusCirc,2) - pow((exesInCircle - xCoordCirc),2)) #calculates the y-coordinates that define the top and bottom bounds of a slice (at x position) of the circle 
        discreteWhyRange = int(whyRange) 
        for whysInCircle in range(( yCoordCirc - discreteWhyRange),( yCoordCirc + discreteWhyRange)):
            pixelLocations.append([exesInCircle,whysInCircle])
    return pixelLocations

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


def patternMatching(image, standardJsonData):
    
    pattern = np.zeros(standardJsonData['shape'], dtype=np.uint8)
    stdCircles = standardJsonData['spot_info']
    for eachCircle in stdCircles:
        circlePixels = circlePixelID(eachCircle)
        for eachPixel in circlePixels:
            pattern[eachPixel[1], eachPixel[0]] = 50
        cv2.circle(pattern ,
                   (eachCircle[0], eachCircle[1]),
                   eachCircle[2],
                   100,
                   3)

    # cvWindow("pattern maker test", pattern, False)
    
    # pattern is usually a dict with the pattern and the spot info in it too
    # image is encoded in the actual server code,
    
    imageCols, imageRows = image.shape[::-1]
    image8b = cv2.normalize(image.copy(),
                            np.zeros(shape=(imageRows, imageCols)),
                            0,255,
                            norm_type = cv2.NORM_MINMAX,
                            dtype = cv2.CV_8U)
    verImg = cv2.cvtColor(image8b.copy(), cv2.COLOR_GRAY2RGB)

    stdCols, stdRows = pattern.shape[::-1]
    print("pattern std shape: " + str(pattern.shape[::-1]))
    # pattern match
    res = cv2.matchTemplate(image8b,
                            pattern,
                            cv2.TM_CCORR_NORMED)
    gausCols, gausRows = res.shape[::-1]
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    print("max location REAL: " + str(max_loc))
    print("gaus img shape: " + str(res.shape[::-1]))
    x, y = np.meshgrid(range(gausCols), range(gausRows))

    # offset center of gaussian to where the top left of the array should be
    centerRow = int((imageRows - stdRows)/2) - 200
    centerCol = int((imageCols - stdCols)/2)
    print("center row and col" + " " + str(centerRow) + " " + str(centerCol))
    cv2.circle(verImg, (centerCol, centerRow), 3, (0, 0, 255), 3)
    sigma = 400 # inverse slope-- smaller = sharper peak, larger = dull peak
    gausCenterWeight = np.exp(-( (x-centerCol)**2 + (y-centerRow)**2)/ (2.0 * sigma**2))
    _, _, _, testCenter = cv2.minMaxLoc(gausCenterWeight)
    print("gaussian center: " + str(testCenter))
    weightedRes = res * gausCenterWeight
    _, _ , _, max_loc = cv2.minMaxLoc(weightedRes)
    print(max_loc) # max loc is reported as written as row, column... 
    bottomRightPt = (max_loc[0] + stdCols,
                     max_loc[1] + stdRows)
    # cv2.rectangle takes in positions as (column, row)....
    cv2.rectangle(verImg,
                  max_loc,
                  bottomRightPt,
                  (0, 105, 255),
                  15)
    cvWindow("rectangle drawn", verImg, False)
    #put this back in with the finalserver code
    # circleLocs = pattern["spot_info"]

    #delete this when in final server
    circleLocs = standardJsonData["spot_info"]

    
    # just find all pixels within the circles and save brightnesses
    circleBrightnesses = []
    circlePixels = []
    for eachCircle in circleLocs:
        print(eachCircle)
        eachCircle[0] = eachCircle[0] + max_loc[0]
        eachCircle[1] = eachCircle[1] + max_loc[1]
        print(eachCircle)
        # cv2.circle takes (column, row) in just like rect
        # note that everything is reported the other way around...
        cv2.circle(verImg,
                   (eachCircle[0], eachCircle[1]),
                   eachCircle[2]+4,
                   (30,30,255),
                   3)
        cv2.circle(verImg,
                   (eachCircle[0], eachCircle[1]),
                   2,
                   (30,30,255),
                   2)
        pixelBrightnesses = []
        circlePixelLocs = circlePixelID(eachCircle)
        for eachPixel in circlePixelLocs:
            pixelBrightnesses.append(image[eachPixel[1], eachPixel[0]])
            circlePixels.append([eachPixel[1], eachPixel[0]])
        avgIntensity = round(np.array(pixelBrightnesses).mean(),4)
        circleBrightnesses.append(avgIntensity)
        
##    backgroundBrightness = []
##    for eachRow in range(max_loc[1], max_loc[1] + stdRows):
##        for eachCol in range(max_loc[0], max_loc[0] + stdCols):
##            if [eachRow, eachCol] not in circlePixels:
##                backgroundBrightness.append([eachRow, eachCol])
    print(str(circleBrightnesses))
##    avgBackground = round(np.array(backgroundBrightness).mean(),4)
##    print(avgBackground)
    cvWindow("outputcirclesdrawn", verImg, False)

# read image to be analyzed
# -1 is as is, 0 is grayscale 8b, 1 is color
# reported with 2064 rows and 3088 cols
# rawImg.shape = (2064, 3088)
rawImg = cv2.imread('slide1_13.tiff', -1) 

# read json
inFile = open('standard_leptin_1-coffee-ring.json', "r")
standardJsonData = json.load(inFile)
inFile.close()

patternMatching(rawImg, standardJsonData)

###pattern match
##res = cv2.matchTemplate(rawImg,
##                        standard_pattern,
##                        cv2.TM_CCORR_NORMED)
##_, max_val, _, max_loc = cv2.minMaxLoc(res)
##
###verify that the pattern was found
##
##bottomRightPt = (max_loc[0] + stdWidth,
##                 max_loc[1] + stdHeight)
##verImg = cv2.cvtColor(rawImg.copy(), cv2.COLOR_GRAY2RGB)
##cv2.rectangle(verImg, max_loc, bottomRightPt, (0, 105, 255), 2)
### cvWindow("verification", verImg, False)
##
### draw in the circles defined by the dict of the circle locs
##filename = "standard_leptin_1-lowc.json"
##in_file = open(filename, "r")
##circleLocs_dict = json.load(in_file)
##in_file.close()
##
##circleLocs = circleLocs_dict["spot info"]
##
##for eachCircle in circleLocs:
##    cv2.circle(verImg,
##               (max_loc[0] + eachCircle[0],
##                max_loc[1] + eachCircle[1]),
##               eachCircle[2]+4,
##               (30,30,255),
##               3)
##    cv2.circle(verImg,
##               (max_loc[0] + eachCircle[0],
##                max_loc[1] + eachCircle[1]),
##               2,
##               (30,30,255),
##               2)
##cvWindow("verification", verImg, False)




















