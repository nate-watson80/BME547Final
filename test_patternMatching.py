import final_server as fs
import pytest
import base64
import cv2


def test_patternMatching():
    # Actual data
    encoded_image = get_encoded_image_for_testing()
    data = {
            "client": "GUI-test",
            "image": "imageString",
            "user": "testUser",
            "img_grp": "testGroup",
            "batch": "leptin-1",
            "filename": "testFilename"
           }
    patternDict = fs.get_patternDict(data)
    matched_data = fs.patternMatching(encoded_image, patternDict)

    # Expected data
    exp_verImg = cv2.imread("verification-img.tiff")
    exp_verImgStr = fs.encodeImage(exp_verImg)
    exp_intensities = [48030.58677042802, 46267.2186770428, 42864.66614785992,
                       43446.404006677796, 44654.580544747085]
    exp_background = 3928.5359746102604
    exp_matched_data = {
                        "ver_Img": exp_verImgStr,
                        "intensities": exp_intensities,
                        "background": exp_background
                       }

    # Testing actual vs expected
    assert matched_data == exp_matched_data


def get_encoded_image_for_testing():
    filePath = "example imgs/slide1_0.tiff"
    with open(filePath, "rb") as image_file:
        b64_imageBytes = base64.b64encode(image_file.read())
    b64_imgString = str(b64_imageBytes, encoding='utf-8')
    return b64_imgString
