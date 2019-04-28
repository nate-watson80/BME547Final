import final_server as fs
import pytest
import base64
import io
import cv2
import numpy as np


def test_decodeImage():
    # Actual
    encoded_image = get_encoded_image_for_testing()
    rawImg16b = fs.decodeImage(encoded_image)
    top_left_corner = rawImg16b[0, 0]
    top_right_corner = rawImg16b[0, -1]
    bot_left_corner = rawImg16b[-1, 0]
    bot_right_corner = rawImg16b[-1, -1]
    middle = rawImg16b[1032, 1544]

    # Expected
    exp_top_left_corner = 8960
    exp_top_right_corner = 20224
    exp_bot_left_corner = 7936
    exp_bot_right_corner = 12288
    exp_middle = 5376

    # Actual vs Expected
    assert top_left_corner == exp_top_left_corner
    assert top_right_corner == exp_top_right_corner
    assert bot_left_corner == exp_bot_left_corner
    assert bot_right_corner == exp_bot_right_corner
    assert middle == exp_middle


def get_encoded_image_for_testing():
    filePath = "example imgs/slide1_0.tiff"
    with open(filePath, "rb") as image_file:
        b64_imageBytes = base64.b64encode(image_file.read())
    b64_imgString = str(b64_imageBytes, encoding='utf-8')
    return b64_imgString
