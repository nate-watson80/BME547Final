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


app = Flask(__name__)


@app.route("/", methods=['GET'])
def server_on():
    """Basic Check to see that the server is up!

    """
    return "The server is up! Should be ready to rock and roll"

@app.route("/imageUpload", methods=['POST'])
def imageUpload():
    in_data = request.get_json()
    output, servCode = patternMatching(in_data)    
    return output, servCode

def patternMatching(in_data):
    valid, servCode, errMsg = validate_patternMatching(in_data)
    if valid:
        str_img_encoded = in_data["image"]
        imgDecoded = base64.b64decode(str_img_encoded)
        image_buf = io.BytesIO(imgDecoded)
        rawImg16b = cv2.imdecode(np.frombuffer(image_buf.read(),
                                               np.uint16),
                                 0)
        rows = 2064
        cols = 3088
        img8b = cv2.normalize(rawImg16b.copy(),
                              np.zeros(shape=(rows,cols)),
                              0,255,
                              norm_type = cv2.NORM_MINMAX,
                              dtype = cv2.CV_8U)
        verImg = cv2.cvtColor(img8b.copy(),
                              cv2.COLOR_GRAY2RGB)
        standard_pattern = cv2.imread('standard_leptin_1-lowc.tiff', -1)
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

        for eachCircle in circleLocs:
            cv2.circle(verImg,
                       (max_loc[0] + eachCircle[0],
                        max_loc[1] + eachCircle[1]),
                       eachCircle[2]+4,
                       (30,30,255),
                       3)
            cv2.circle(verImg,
                       (max_loc[0] + eachCircle[0],
                        max_loc[1] + eachCircle[1]),
                       2,
                       (30,30,255),
                       2)
        cv2.imwrite("verification-img.tiff", verImg)
        _, verImg_buf = cv2.imencode(".tiff", verImg)
        verImg_buf_64 = base64.b64encode(verImg_buf)
        b64_imgString = str(verImg_buf_64, encoding='utf-8')
        payload = {"ver_Img" : b64_imgString}
        return jsonify(payload), 200
    else:
        return errMsg, servCode

def validate_patternMatching(in_data):
    return True, 200, "no errors"


if __name__ == '__main__':
    app.run()
