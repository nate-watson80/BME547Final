# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 18:06:02 2019

@author: Mars
"""

from flask import Flask, jsonify, request
import numpy as np
import os, io
import base64
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from pymongo import MongoClient
from datetime import datetime
from scipy import ndimage



app = Flask(__name__)
client = MongoClient()
db = client.test_database

@app.route("/", methods=['GET'])
def server_on():
    """Basic Check to see that the server is up

    Gives status message that server is running

    Args:
        None

    Returns:
        None
    """
    return "The server is up! Should be ready to rock and roll"

@app.route("/pullAllData", methods=['GET'])
def pullAllData():
    """sends all analyzed data back in a json with fileNames and list of list of all "spots" intensities
    """
    storeFileNames = []
    storeSpotData = []
    for eachEntry in db.d4Images.find():
        storeFileNames.append(eachEntry["filename"])
        storeSpotData.append(eachEntry["spots"])
    payload = {"filename": storeFileNames,
               "spots": storeSpotData}
    return jsonify(payload), 200


@app.route("/imageUpload", methods=['POST'])
def imageUpload():
    in_data = request.get_json()
    patternDict = get_patternDict(in_data)
    if not patternDict:
        return jsonify({"error": "Batch not recognized contact distributor."}), 400
    servCode, errMsg = validate_image(in_data)
    if errMsg:
        return jsonify({"error": errMsg}), servCode
    matched_data = patternMatching(in_data['image'], patternDict)
    binary_d4OrigImage = base64.b64decode(in_data['image'])
    orig_img_id = db.d4OrigImg.insert_one({"image": binary_d4OrigImage}).inserted_id
    matched_img_id = db.d4MatchedImg.insert_one({"image": matched_data['ver_Img']}).inserted_id
    data = {
        "user": in_data["user"],
        "timestamp": datetime.utcnow(),
        "spots": matched_data["intensities"],
        "background": matched_data["background"],
        "batch": in_data["batch"],
        "img_grp": in_data["img_grp"],
        "orig_image": orig_img_id,
        "matched_image": matched_img_id,
        "filename": in_data['filename']
    }
    img_id = db.d4Images.insert_one(data)
    return jsonify(matched_data), 200


def get_patternDict(data):
    batch = data['batch']
    return db.patterns.find_one({"batch": batch})


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


def decodeImage(str_encoded_img, color = False):
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
                                -1)
    return orig_img


def encodeImage(np_img_array):
    _, img_buffer = cv2.imencode(".tiff", np_img_array)
    img_buffer_enc64 = base64.b64encode(img_buffer)
    str_img_buffer_enc64 = str(img_buffer_enc64, encoding='utf-8')
    return str_img_buffer_enc64


def generatePatternMasks(spot_info, shape):
    """generate pattern from json encoded circle locations
    and generate masks for spots and bgMask
    """
    pattern = np.zeros(shape, dtype = np.uint8)
    spotsMask = pattern.copy()
    bgMask = 255 * np.ones(shape, dtype = np.uint8)
    for eachCircle in spot_info:
        circlePixels = circlePixelID(eachCircle)
        for eachPixel in circlePixels:
            pattern[eachPixel[1], eachPixel[0]] = 50
            spotsMask[eachPixel[1], eachPixel[0]] = 255
            bgMask[eachPixel[1], eachPixel[0]] = 0
        cv2.circle(pattern,
                   (eachCircle[0], eachCircle[1]),
                   eachCircle[2],
                   100,
                   3)
    return pattern, spotsMask, bgMask


def templateMatch8b(image, pattern):

    imageCols, imageRows = image.shape[::-1]
    stdCols, stdRows = pattern.shape[::-1]
    print("pattern std shape: " + str(pattern.shape[::-1]))
    # grab dimensions of input image and convert to 8bit for manipulation
    image8b = cv2.normalize(image.copy(),
                            np.zeros(shape=(imageRows, imageCols)),
                            0,255,
                            norm_type = cv2.NORM_MINMAX,
                            dtype = cv2.CV_8U)
    verImg = cv2.cvtColor(image8b.copy(), cv2.COLOR_GRAY2RGB)

    res = cv2.matchTemplate(image8b, pattern, cv2.TM_CCORR_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(res)
    gausCols, gausRows = res.shape[::-1]
    print("max location REAL: " + str(max_loc))
    print("gaus img shape: " + str(res.shape[::-1]))

    x, y = np.meshgrid(range(gausCols), range(gausRows))
    centerRow = int((imageRows - stdRows)/2) - 200
    centerCol = int((imageCols - stdCols)/2)
    print("center row and col" + " " + str(centerRow) + " " + str(centerCol))
    #draws circle where the gaussian is centered.
    cv2.circle(verImg, (centerCol, centerRow), 3, (0, 0, 255), 3)
    sigma = 400 # inverse slope-- smaller = sharper peak, larger = dull peak
    gausCenterWeight = np.exp(-( (x-centerCol)**2 + (y-centerRow)**2)/ (2.0 * sigma**2))
    _, _, _, testCenter = cv2.minMaxLoc(gausCenterWeight)
    print("gaussian center: " + str(testCenter))
    weightedRes = res * gausCenterWeight
    _, _ , _, max_loc = cv2.minMaxLoc(weightedRes)
    print(max_loc) # max loc is reported as written as column,row...
    bottomRightPt = (max_loc[0] + stdCols,
                     max_loc[1] + stdRows)
    # cv2.rectangle takes in positions as (column, row)....
    cv2.rectangle(verImg,
                  max_loc,
                  bottomRightPt,
                  (0, 105, 255),
                  15)
    #cvWindow("rectangle drawn", verImg, False)
    topLeftMatch = max_loc # col, row
    return topLeftMatch, verImg


def patternMatching(encoded_image, patternDict):
    rawImg16b = decodeImage(encoded_image)
    pattern, spotMask, bgMask = generatePatternMasks(patternDict['spot_info'],
                                                     patternDict['shape'])

    max_loc, verImg = templateMatch8b(rawImg16b, pattern)
    stdCols, stdRows = pattern.shape[::-1]

    circleLocs = patternDict['spot_info']

    subImage = rawImg16b [max_loc[1]:max_loc[1] + stdRows,
                          max_loc[0]:max_loc[0] + stdCols].copy()

    for eachCircle in circleLocs:
        eachCircle[0] = eachCircle[0] + max_loc[0]
        eachCircle[1] = eachCircle[1] + max_loc[1]
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
    label_im, nb_labels = ndimage.label(spotMask)
    spot_vals = ndimage.measurements.mean(subImage, label_im, range(1, nb_labels+1))
    mean_vals = ndimage.measurements.mean(subImage, label_im)
    print(spot_vals)
    print(mean_vals)
    label_bg, bg_labels = ndimage.label(bgMask)
    mean_bg = ndimage.measurements.mean(subImage, label_bg)
    print(mean_bg)

    verImg = cv2.pyrDown(verImg) # downsizes
    cv2.imwrite("verification-img.tiff", verImg)
    verImgStr = encodeImage(verImg)
    payload = {"ver_Img" : verImgStr,
               "intensities" : spot_vals.tolist(),
               "background" : mean_bg}
    return payload


def validate_image(in_data):
    return 200, None

if __name__ == '__main__':
    app.run()
