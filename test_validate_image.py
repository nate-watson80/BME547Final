import final_server as fs
import pytest


def test_validate_image():
    # Positive testing
    in_data_good = {
                    "client": "GUI-test",
                    "image": "imageString",
                    "user": "testUser",
                    "img_grp": "testGroup",
                    "batch": "leptin-1",
                    "location": "testLocation",
                    "filename": "testFilename"
                   }
    errorCode, errorStatement = fs.validate_image(in_data_good)
    assert errorCode == 200
    assert errorStatement is None

    # Negative test case: missing data
    in_data_bad1 = {
                    "client": "GUI-test",
                    "image": "imageString",
                    "user": "testUser",
                    "img_grp": "testGroup",
                    "batch": "leptin-1",
                    "location": "testLocation",
                   }
    errorCode, errorStatement = fs.validate_image(in_data_bad1)
    assert errorCode == 400
    assert errorStatement == "Missing data from client."

    # Negative test case: bad data
    in_data_bad2 = {
                    "client": "GUI-test",
                    "image": "imageString",
                    "user": "testUser",
                    "img_grp": 1234,
                    "batch": "leptin-1",
                    "location": "testLocation",
                    "filename": "testFilename"
                   }
    errorCode, errorStatement = fs.validate_image(in_data_bad2)
    assert errorCode == 406
    assert errorStatement == "Bad (non-string) data from client."
