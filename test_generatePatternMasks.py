import final_server as fs
import pytest
import base64
import cv2

def test_generatePatternMasks():
    spot_info = [[138, 86, 29],
                 [136, 174, 29],
                 [136, 262, 29],
                 [134, 434, 29],
                 [134, 348, 28]]
    shape = [522, 244]
    pattern, spotsMask, bgMask = fs.generatePatternMasks
