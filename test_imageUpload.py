import final_server as fs
import pytest


def test_imageUpload():
    encoded_image = get_encoded_image_for_testing()
    in_data = {
               "client": "GUI-test",
               "image": encoded_image,
               "user": "testUser",
               "img_grp": "testGroup",
               "batch": "leptin-1",
               "filename": "slide1_0.tiff"
              }
    matchedData, statusCode = fs.imageUpload()



def get_encoded_image_for_testing():
    filePath = "example imgs/slide1_0.tiff"
    with open(filePath, "rb") as image_file:
        b64_imageBytes = base64.b64encode(image_file.read())
    b64_imgString = str(b64_imageBytes, encoding='utf-8')
    return b64_imgString
