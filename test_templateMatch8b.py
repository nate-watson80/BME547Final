import final_server as fs
import pytest
import base64


def test_templateMatch8b():
    spot_info = [[138, 86, 29],
                 [136, 174, 29],
                 [136, 262, 29],
                 [134, 434, 29],
                 [134, 348, 28]]
    shape = [522, 244]
    encoded_image = get_encoded_image_for_testing()
    rawImg16b = fs.decodeImage(encoded_image)
    pattern, spotsMask, bgMask = fs.generatePatternMasks(spot_info, shape)
    max_loc, verImg = fs.templateMatch8b(rawImg16b, pattern)

    # Remaining work: need to find Expected values for max_loc and verImg
    # which can be tested against.

def get_encoded_image_for_testing():
    filePath = "example imgs/slide1_0.tiff"
    with open(filePath, "rb") as image_file:
        b64_imageBytes = base64.b64encode(image_file.read())
    b64_imgString = str(b64_imageBytes, encoding='utf-8')
    return b64_imgString
