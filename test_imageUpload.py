import final_server as fs
import pytest
import base64


def test_imageUpload():
    # Actual
    encoded_image = get_encoded_image_for_testing()
    in_data = {
               "client": "GUI-test",
               "image": encoded_image,
               "user": "testUser",
               "img_grp": "testGroup",
               "batch": "leptin-1",
               "location": "testlocation",
               "filename": "slide1_0.tiff"
              }
    matched_data, statusCode = fs.imageUpload(in_data)

    # Expected
    exp_encoded_image = get_encoded_image_for_testing()
    exp_in_data = {
                   "client": "GUI-test",
                   "image": exp_encoded_image,
                   "user": "testUser",
                   "img_grp": "testGroup",
                   "batch": "leptin-1",
                   "location": "testlocation",
                   "filename": "slide1_0.tiff"
                  }
    exp_patternDict = fs.get_patternDict(exp_in_data)
    exp_matched_data = fs.patternMatching(exp_in_data['image'],
                                          exp_patternDict)
    exp_statusCode = 200

    # Actual vs Expected
    assert matched_data == exp_matched_data
    assert statusCode == exp_statusCode


def get_encoded_image_for_testing():
    filePath = "example imgs/slide1_0.tiff"
    with open(filePath, "rb") as image_file:
        b64_imageBytes = base64.b64encode(image_file.read())
    b64_imgString = str(b64_imageBytes, encoding='utf-8')
    return b64_imgString
