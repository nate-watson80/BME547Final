import final_server as fs
import pytest
from pymongo import MongoClient


def test_init_mongoDB():
    # Actual
    db = fs.init_mongoDB()

    # Expected
    connString = "mongodb+srv://bme547:.9w-UVfWaMDCsuL"
    connString = connString + "@bme547-rrjis.mongodb.net/test?retryWrites=true"
    client = MongoClient(connString)
    exp_db = client.Detector_Software

    # Actual vs Expected
    assert db == exp_db
