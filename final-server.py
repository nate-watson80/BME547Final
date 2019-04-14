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
import json
from pymongo import MongoClient
from datetime import datetime



app = Flask(__name__)
client = MongoClient()
db = client.test_database

@app.route("/", methods=['GET'])
def server_on():
    """Basic Check to see that the server is up!

    """
    return "The server is up! Should be ready to rock and roll"

@app.route("/imageUpload", methods=['POST'])
def imageUpload():
    in_data = request.get_json()
    pattern = get_pattern(in_data)
    if not pattern:
        return jsonify({"error": "Batch not recognized contact distributor."}), 400
    servCode, errMsg = validate_image(in_data)
    if errMsg:
        return jsonify({"error": errMsg}), servCode
    matched_data = patternMatching(in_data['image'], pattern)
    binary_d4OrigImage = base64.b64decode(in_data['image'])
    orig_img_id = db.d4OrigImg.insert_one({"image": binary_d4OrigImage}).inserted_id
    matched_img_id = db.d4MatchedImg.insert_one({"image": matched_data['ver_Img']}).inserted_id
    data = {
        "user": in_data["user"],
        "timestamp": datetime.utcnow(),
        "spots": matched_data["intensities"],
        "batch": in_data["batch"],
        "img_grp": in_data["img_grp"],
        "orig_image": orig_img_id,
        "matched_image": matched_img_id
    }
    img_id = db.d4Images.insert_one(data)
    return jsonify(matched_data), 200

def get_pattern(data):
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
                                0)
    return orig_img

def encodeImage(np_img_array):
    _, img_buffer = cv2.imencode(".tiff", np_img_array)
    img_buffer_enc64 = base64.b64encode(img_buffer)
    str_img_buffer_enc64 = str(img_buffer_enc64, encoding='utf-8')
    return str_img_buffer_enc64

def patternMatching(encoded_image, pattern):
    rawImg16b = decodeImage(encoded_image)
    standard_pattern = decodeImage(pattern["image"])
    rows = 2064
    cols = 3088
    img8b = cv2.normalize(rawImg16b.copy(),
                          np.zeros(shape=(rows,cols)),
                          0,255,
                          norm_type = cv2.NORM_MINMAX,
                          dtype = cv2.CV_8U)
    verImg = cv2.cvtColor(img8b.copy(),
                          cv2.COLOR_GRAY2RGB)
    
    stdWidth, stdHeight = standard_pattern.shape[::-1]

    #pattern match
    res = cv2.matchTemplate(rawImg16b,
                    standard_pattern,
                    cv2.TM_CCORR_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    bottomRightPt = (max_loc[0] + stdWidth,
                     max_loc[1] + stdHeight)
    cv2.rectangle(verImg, max_loc, bottomRightPt, (0, 105, 255), 15)    
    circleLocs = pattern["spot_info"]

    circleBrightnesses = []
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
        pixelBrightnesses = []
        circlePixelLocs = circlePixelID(eachCircle)
        for eachPixel in circlePixelLocs:
            pixelBrightnesses.append(rawImg16b[eachPixel[1], eachPixel[0]])
        avgIntensity = round(np.array(pixelBrightnesses).mean(),4)
        circleBrightnesses.append(avgIntensity)

    verImg = cv2.pyrDown(verImg) # downsizes
    cv2.imwrite("verification-img.tiff", verImg)
    verImgStr = encodeImage(verImg)
    payload = {"ver_Img" : verImgStr,
               "intensities" : circleBrightnesses}
    return payload

def validate_image(in_data):
    return 200, None

if __name__ == '__main__':
    app.run()
