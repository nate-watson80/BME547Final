import final_server as fs
from datetime import datetime

fs.init_mongoDB()

def test_log_to_DB():
    timestamp = datetime.utcnow()
    in_data = {
               "user": "testUser",
               "timestamp": timestamp,
               "filename": "testFilename"
              }
    client_name = "GUI-test"
    action = "Image Uploaded"
    fs.log_to_DB(in_data, client_name, action)
