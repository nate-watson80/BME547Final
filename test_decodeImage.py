import final_server as fs
import pytest
import base64

def test_decodeImage():
    # Actual
    encoded_image = get_encoded_image_for_testing()
    rawImg16b = fs.decodeImage(encoded_image)

    # Expected


    # Actual vs Expected

def get_encoded_image_for_testing():
    filePath = "example imgs/slide1_0.tiff"
    with open(filePath, "rb") as image_file:
        b64_imageBytes = base64.b64encode(image_file.read())
    b64_imgString = str(b64_imageBytes, encoding='utf-8')
    return b64_imgString
