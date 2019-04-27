import final_server as fs
import pytest
from pymongo import MongoClient
import bson

db = fs.db


def test_get_patternDict():
    data = {
            "client": "GUI-test",
            "image": "imageString",
            "user": "testUser",
            "img_grp": "testGroup",
            "batch": "leptin-1",
            "filename": "testFilename"
           }
    patternDict = fs.get_patternDict(data)
    # ObjectId taken from MongoDB database
    exp_ObjectID = bson.objectid.ObjectId('5cba0e4c12ab312088990a74')
    exp_patternDict = {
                       "_id": exp_ObjectID,
                       "batch": "leptin-1",
                       "spot_info": [[138, 86, 29],
                                     [136, 174, 29],
                                     [136, 262, 29],
                                     [134, 434, 29],
                                     [134, 348, 28]],
                       "shape": [522, 244]
                      }
    assert patternDict == exp_patternDict
