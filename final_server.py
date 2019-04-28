# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 18:06:02 2019

@author: Mars
"""

from flask import Flask, jsonify, request
import numpy as np
import os
import io
import base64
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from pymongo import MongoClient

from datetime import datetime
from scipy import ndimage
import logging


# Initialize the Flask and Mongo client-- this is set for a local Mongo DB
app = Flask(__name__)


def main():
    """Main code for module

    Creates a logging file and kicks off flask web server

    Args:
        None

    Return:
        None
    """
    logging.basicConfig(filename="logfile.log", level=logging.INFO)
    app.run(host="0.0.0.0")


def init_mongoDB():
    """Initializes the MongoDB

    Creates database object (which is stored to a global variable "db")
    which contains connection info to MongoDB database and MongoDB collection
    "Detector_Software"

    Args:
        None

    Returns:
        db (database object): MongoDB database
    """
    connString = "mongodb+srv://bme547:.9w-UVfWaMDCsuL"
    connString = connString + "@bme547-rrjis.mongodb.net/test?retryWrites=true"
    client = MongoClient(connString)
    db = client.Detector_Software
    return db


db = init_mongoDB()  # use a global variable for database object


@app.route("/", methods=['GET'])
def server_on():
    """Basic Check to see that the server is up

    Returns the server status.

    Args:
        None

    Returns:
        Server status
    """
    return "The server is up! Should be ready to rock and roll", 200


@app.route("/pullAllData", methods=['GET'])
def pullAllData():
    """sends all analyzed data back in a json with fileNames and list of list
    of all "spots" intensities and backgrounds.

    Args:
        db.d4Images (Mongo db collection): Mongo DB collection with processed
        data

    Returns:
        payload (jsonify(dict)): Processed data return
    """
    pullFileNames = []
    pullSpotData = []
    pullBgData = []
    for eachEntry in db.d4Images.find():
        pullFileNames.append(eachEntry["filename"])
        pullSpotData.append(eachEntry["spots"])
        pullBgData.append(eachEntry["background"])
    payload = {"filename": pullFileNames,
               "spots": pullSpotData,
               "background": pullBgData}
    return jsonify(payload), 200


@app.route("/imageUpload", methods=['POST'])
def imageUpload():
    """Uploads and processes an image

    The core function of the server, takes in a base64 encoded image
    and other associated data with it (which pattern to match to the image,
    the client where the call originates from). Then, it finds the pattern
    within the mongo db (it's generated from pattern-generator.py script first)
    Then, the patternMatching function is run, with the original image and the
    pattern. That function returns the processed data, which is shoved into
    the MongoDB and returned to the user.

    Args:
        in_data (json/dictionary): b64 encoded image, batch/pattern name, more

    Returns:
        matchedData (string): processed image, data, and more
        errorCode (int): HTTP status code
    """
    in_data = request.get_json()
    log_data = {
                "user": in_data["user"],
                "client": in_data["client"],
                "filename": in_data["filename"],
               }
    action = "Image Data Received from Client"
    timestamp_id = log_to_DB(log_data, action)
    patternDict = get_patternDict(in_data)
    if not patternDict:
        batch = in_data["batch"]
        errStr = "Batch " + batch + " not recognized contact distributor."
        logging.error(errStr)
        return jsonify({"error": errStr}), 400
    servCode, errMsg = validate_image(in_data)
    if errMsg:
        logging.error(errMsg)
        return jsonify({"error": errMsg}), servCode
    matched_data = patternMatching(in_data['image'], patternDict)
    action = "Image Data Matched"
    timestamp_id = log_to_DB(log_data, action)
    binary_d4OrigImage = base64.b64decode(in_data['image'])
    action = "Image Decoded"
    timestamp_id = log_to_DB(log_data, action)
    orig_img_id = db.d4OrigImg.insert_one(
        {"image": binary_d4OrigImage}).inserted_id
    matched_img_id = db.d4MatchedImg.insert_one(
        {"image": matched_data['ver_Img']}).inserted_id
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
    action = "Image Uploaded"
    timestamp_id = log_to_DB(log_data, action)
    return jsonify(matched_data), 200


@app.route("/pullImage/<qFileName>", methods=["GET"])
def pullImage(qFileName):
    if verifyFileName(qFileName):
        data = db.d4Images.find_one({"filename": qFileName})
        verImage = db.d4MatchedImg.find_one({"_id": data["matched_image"]})
        payload = {"status": "found image",
                   "image": str(verImage["image"])}
        return jsonify(payload), 200
    else:
        return "missing", 400


def verifyFileName(fileName):
    return True


def log_to_DB(log_data, action):
    """Creates log entries to MongoDB Cloud Database

    Adds to "Logging" collection on MongoDB for various actions performed
    by the client. Currently includes actions for:
    - Image Data Received from Client
    - Image Data Matched
    - Image Decoded
    - Image Uploaded
    Stores timestamp as primary key for "Logging" collection. Timestamp is
    rounded to the nearest 1000 microseconds (nearest 1 millisecond).

    Args:
        log_data (dictionary): contains user, client, and filename attributes
        action (string): the image action which is being logged

    Returns:
        timestamp_id (string): this log entry's primary key value
    """
    timestamp = datetime.utcnow()
    timestamp = timestamp.replace(microsecond=round(timestamp.microsecond, -3))
    log_data["_id"] = timestamp
    log_data["action"] = action
    timestamp_id = db.Logging.insert_one(log_data).inserted_id
    return timestamp_id


def get_patternDict(data):
    """ finds the pattern from the batch name input from the client from the
        MongoDB. Then returns the encoded pattern!

    Args:
        data (dictionary): the data dictionary that contains the 'batch' key

    Returns:
        patternDict (dictionary): dictionary of pattern data for this specific
                                  batch type
    """
    batch = data['batch']
    patternDict = db.patterns.find_one({"batch": batch})
    return patternDict


def circlePixelID(circleData):
    """Identifies all pixels within a circle

    Takes one circle centerpoint location and radius and calculates all pixel
    coords within the radius from that center location

    Args:
        circleData (list): centerpoint row, centerpoint col, and radius
                           for a circle in pattern
    Returns:
        pixelLocations (list): list of all pixel locations within a circle
    """
    pixelLocations = []
    # separates the x and y coordinates of the center of the circles and the
    # circle radius
    xCoordCirc = circleData[0]
    yCoordCirc = circleData[1]
    radiusCirc = circleData[2]
    for exesInCircle in range((xCoordCirc - radiusCirc),
                              (xCoordCirc + radiusCirc + 1)):
        # Calculates the y-coordinates that define the top and bottom bounds
        # of a slice (at x position) of the circle
        whyRange = np.sqrt(
            pow(radiusCirc, 2) - pow((exesInCircle - xCoordCirc), 2))
        discreteWhyRange = int(whyRange)
        for whysInCircle in range((yCoordCirc - discreteWhyRange),
                                  (yCoordCirc + discreteWhyRange + 1)):
            pixelLocations.append([exesInCircle, whysInCircle])
    return pixelLocations


def decodeImage(str_encoded_img, color=False):
    """ Takes an base 64 encoded image and converts it to a image array. Has
    the option to conserve the original color or just as a greyscale.

    Args:
        str_encoded_img (str): base 64 encoded image

    Returns:
        orig_img (np.array): numpy array image matrix
    """
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
    """ Encodes the np.array image matrix into a base 64 encoded string

    Args:
        np_img_array (np.array): just an image array
    Returns:
        str_img_buffer_enc64 (string): base 64 encoded image string
    """
    _, img_buffer = cv2.imencode(".tiff", np_img_array)
    img_buffer_enc64 = base64.b64encode(img_buffer)
    str_img_buffer_enc64 = str(img_buffer_enc64, encoding='utf-8')
    return str_img_buffer_enc64


def generatePatternMasks(spot_info, shape):
    """generate pattern from json encoded circle locations
    and generate masks for spots and bgMask. This is important for efficient
    quantification of brightness in the spots and background within the image

    Args:
        spot_info (list): encoded circle coordinates within the pattern
        shape (list): encoded shape of the pattern, circles are relative to
                    this
    Returns:
        pattern (np array): the pattern to be found within the image
        spotsMask (np array): the masks for the spots within the image
        bgMask (np array): the masks for the background wihin the image

    """
    pattern = np.zeros(shape, dtype=np.uint8)
    spotsMask = pattern.copy()
    bgMask = 255 * np.ones(shape, dtype=np.uint8)
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
    """Core template matching algorithm

    Calculates the correlation between the pattern and the image at all points
    in 2d sliding window format weighs the correlations higher in the center of
    the image where the spots should be.

    Args:
        image (np array): the image to be processed
        pattern (np array): the pattern to be found in the image (circles)
    Returns:
        topLeftMatch (list): location of the best fit defined as the top left
                             coordinate within the image
        verImg (np array): copy of the image in color with a rectangle drawn
                           where the pattern was best fit
    """
    imageCols, imageRows = image.shape[::-1]
    stdCols, stdRows = pattern.shape[::-1]
    print("pattern std shape: " + str(pattern.shape[::-1]))
    # grab dimensions of input image and convert to 8bit for manipulation
    image8b = cv2.normalize(image.copy(),
                            np.zeros(shape=(imageRows, imageCols)),
                            0, 255,
                            norm_type=cv2.NORM_MINMAX,
                            dtype=cv2.CV_8U)
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
    # draws circle where the gaussian is centered.
    cv2.circle(verImg, (centerCol, centerRow), 3, (0, 0, 255), 3)
    sigma = 400  # inverse slope-- smaller = sharper peak, larger = dull peak
    gausCenterWeight = np.exp(-((x-centerCol)**2 + (y-centerRow)**2) /
                              (2.0 * sigma**2))
    _, _, _, testCenter = cv2.minMaxLoc(gausCenterWeight)
    print("gaussian center: " + str(testCenter))
    weightedRes = res * gausCenterWeight
    _, _, _, max_loc = cv2.minMaxLoc(weightedRes)
    print(max_loc)  # max loc is reported as written as column,row...
    bottomRightPt = (max_loc[0] + stdCols,
                     max_loc[1] + stdRows)
    # cv2.rectangle takes in positions as (column, row)....
    cv2.rectangle(verImg,
                  max_loc,
                  bottomRightPt,
                  (0, 105, 255),
                  15)
    # cvWindow("rectangle drawn", verImg, False)
    topLeftMatch = max_loc  # col, row
    return topLeftMatch, verImg


def patternMatching(encoded_image, patternDict):
    """Performs pattern matching algorithm on uploaded image

    Takes the input image to be processed and the pattern, and finds the
    circles, draws circles on a copy of the original image- on a verification
    image. Then, this program quantifies the brightness of the spot features
    and the background intensity within the pattern (not-spot areas). Spits out
    a downsized verification image (because it doesn't need to be 16 bit or as
    large as the original image to show that circles were found).

    Args:
        encoded_image (str): base64 encoded image to be processed
        patternDict (dictionary): dictionary with encoded pattern
    Returns:
        payload (dictionary): contains verification image and the brightnesses
                              of the spots and of the background
    """
    rawImg16b = decodeImage(encoded_image)
    pattern, spotMask, bgMask = generatePatternMasks(patternDict['spot_info'],
                                                     patternDict['shape'])

    max_loc, verImg = templateMatch8b(rawImg16b, pattern)
    stdCols, stdRows = pattern.shape[::-1]

    circleLocs = patternDict['spot_info']

    subImage = rawImg16b[max_loc[1]:max_loc[1] + stdRows,
                         max_loc[0]:max_loc[0] + stdCols].copy()

    for eachCircle in circleLocs:
        eachCircle[0] = eachCircle[0] + max_loc[0]
        eachCircle[1] = eachCircle[1] + max_loc[1]
        cv2.circle(verImg,
                   (eachCircle[0], eachCircle[1]),
                   eachCircle[2]+4,
                   (30, 30, 255),
                   3)
        cv2.circle(verImg,
                   (eachCircle[0], eachCircle[1]),
                   2,
                   (30, 30, 255),
                   2)
    label_im, nb_labels = ndimage.label(spotMask)
    spot_vals = ndimage.measurements.mean(subImage, label_im,
                                          range(1, nb_labels+1))
    mean_vals = ndimage.measurements.mean(subImage, label_im)
    print(spot_vals)
    print(mean_vals)
    label_bg, bg_labels = ndimage.label(bgMask)
    mean_bg = ndimage.measurements.mean(subImage, label_bg)
    print(mean_bg)

    verImg = cv2.pyrDown(verImg)  # downsizes
    cv2.imwrite("verification-img.tiff", verImg)
    verImgStr = encodeImage(verImg)
    payload = {"ver_Img": verImgStr,
               "intensities": spot_vals.tolist(),
               "background": mean_bg}
    return payload


def validate_image(in_data):
    """ validates the input data to make sure it's formatted as expected

    Args:
        in_data (dictionary): the request.json in_Data from the client
    Returns:
        errorCode, errorStatement (int, Str): server error code and message
    """
    return 200, None

if __name__ == '__main__':
    main()
