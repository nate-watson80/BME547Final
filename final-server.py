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


app = Flask(__name__)


@app.route("/", methods=['GET'])
def server_on():
    """Basic Check to see that the server is up!

    """
    return "The server is up! Should be ready to rock and roll"

@app.route("/imageUpload", methods=['POST'])
def imageUpload():
    in_data = request.get_json()
    str_img_encoded = in_data["image"]
    str_img = base64.b64decode(str_img_encoded)
    with open("sent-imgX.tiff", "wb") as out_file:
        out_file.write(str_img)
    out_data = "Server has received payload from " + in_data["client"]
    
    return out_data
    
if __name__ == '__main__':
    app.run()
