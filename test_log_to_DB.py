import final_server as fs
from pymongo import MongoClient
from datetime import datetime

db = fs.init_mongoDB()


def test_log_to_DB():
    timestamp = datetime.utcnow()
    log_data = {
                "user": "testUser",
                "client": "GUI-test",
                "filename": "testFilename",
               }
    action = "Image Uploaded"
    log_result = fs.log_to_DB(log_data, action)
    exp_log_result = db.Logging.find_one({"timestamp": timestamp})["_id"]
    assert log_result == exp_log_result
