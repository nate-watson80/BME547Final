import final_server as fs
import pytest
import base64
import cv2


def test_encodeImage():
    np_img_array = cv2.imread("verification-img.tiff")
    str_img_buffer_enc64 = fs.encodeImage(np_img_array)
    exp_str_img_buffer_enc64 = get_encoded_image_for_testing()
    assert str_img_buffer_enc64 == exp_str_img_buffer_enc64


def get_encoded_image_for_testing():
    filePath = "verification-img.tiff"
    with open(filePath, "rb") as image_file:
        b64_imageBytes = base64.b64encode(image_file.read())
    b64_imgString = str(b64_imageBytes, encoding='utf-8')
    return b64_imgString
