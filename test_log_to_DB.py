import final_server as fs
from pymongo import MongoClient
from datetime import datetime

db = fs.init_mongoDB()


def test_log_to_DB():
    timestamp = datetime.utcnow()
    in_data = {
               "user": "testUser",
               "timestamp": timestamp,
               "filename": "testFilename"
              }
    client_name = "GUI-test"
    action = "Image Uploaded"
    log_result = fs.log_to_DB(in_data, client_name, action)
    exp_log_result = db.Logging.find_one({"timestamp": timestamp})["_id"]
    assert result == exp_result
