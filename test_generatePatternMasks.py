import final_server as fs
import pytest


def test_generatePatternMasks():
    # Actual
    spot_info = [[138, 86, 29],
                 [136, 174, 29],
                 [136, 262, 29],
                 [134, 434, 29],
                 [134, 348, 28]]
    shape = [522, 244]
    pattern, spotsMask, bgMask = fs.generatePatternMasks(spot_info, shape)
    pattern_test_array = [pattern[0, 0],
                          pattern[100, 110],
                          pattern[100, 125]]
    spotsMask_test_array = [spotsMask[0, 0],
                            spotsMask[100, 110],
                            spotsMask[100, 125]]
    bgMask_test_array = [bgMask[0, 0],
                         bgMask[100, 110],
                         bgMask[100, 125]]

    # Expected
    exp_pattern_test_array = [0, 100, 50]
    exp_spotsMask_test_array = [0, 0, 255]
    exp_bgMask_test_array = [255, 255, 0]

    # Actual vs Expected
    assert pattern_test_array == exp_pattern_test_array
    assert spotsMask_test_array == exp_spotsMask_test_array
    assert bgMask_test_array == exp_bgMask_test_array
