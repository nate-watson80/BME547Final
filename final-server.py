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
    str_img_encoded = in_data["image"]
    str_img = base64.b64decode(str_img_encoded)
    spot_data, processed_img = dummy_process_image(str_img)
    data = {
        "user": in_data["user"],
        "timestamp": datetime.utcnow(),
        "spots": spot_data,
        "batch": in_data["batch"],
        "img_grp": in_data["img_grp"],
        "image": processed_img
    }
    img_id = db.d4Images.insert_one(data).inserted_id
    out_data = ("Server has received payload from " + in_data["client"] +
        " inserted into db with id " + str(img_id))
    
    return out_data

def dummy_process_image(str_img):
    return [], str_img
    
if __name__ == '__main__':
    app.run()
