import final_server as fs
import pytest
from pymongo import MongoClient

db = fs.db


def test_log_to_DB():
    log_data = {
                "user": "testUser",
                "client": "GUI-test",
                "filename": "testFilename",
               }
    action = "Image Uploaded"
    timestamp_id = fs.log_to_DB(log_data, action)
    exp_timestamp_id = db.Logging.find_one({"_id": timestamp_id})["_id"]
    assert timestamp_id == exp_timestamp_id
