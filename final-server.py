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
    if !pattern:
        return jsonify({"error": "Batch not recognized contact distributor."}), 400
    servCode, errMsg = validate_image(in_data)
    if errMsg:
        return jsonify({"error": errMsg}), servCode
    matched_data = patternMatching(in_data, pattern)
    orig_img_id = db.d4OrigImg.insert_one({"image": in_data['image']}).inserted_id
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
    return db.patterns.findOne({"batch": batch}) 

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


def decodeImage(str_encoded_img):
    decoded_img = base64.b64decode(str_encoded_img)
    buf_img = io.BytesIO(decoded_img)
    orig_img = cv2.imdecode(np.frombuffer(buf_img.read(),
                                          np.uint16),
                            0)
    return orig_img


def patternMatching(encoded_image, encoded_pattern):
    rawImg16b = decodeImage(encoded_image)
    standard_pattern = decodeImage(encoded_pattern)
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
    filename = "standard_leptin_1-lowc.json"
    in_file = open(filename, "r")
    circleLocs_dict = json.load(in_file)
    in_file.close()
    
    circleLocs = circleLocs_dict["spot info"]

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
        
    cv2.imwrite("verification-img.tiff", verImg)
    _, verImg_buf = cv2.imencode(".tiff", verImg)
    verImg_buf_64 = base64.b64encode(verImg_buf)
    b64_imgString = str(verImg_buf_64, encoding='utf-8')
    payload = {"ver_Img" : b64_imgString,
               "intensities" : circleBrightnesses}
    return payload

def validate_image(in_data):
    return 200, None

if __name__ == '__main__':
    app.run()
