import final_server as fs
import pytest


def test_circlePixelID():
    circleData = [5, 5, 1]
    pixelLocations = fs.circlePixelID(circleData)
    exp_pixelLocations = [[4, 5],
                          [5, 4], [5, 5], [5, 6],
                          [6, 5]]
    assert pixelLocations == exp_pixelLocations

    circleData = [5, 5, 2]
    pixelLocations = fs.circlePixelID(circleData)
    exp_pixelLocations = [[3, 5],
                          [4, 4], [4, 5], [4, 6],
                          [5, 3], [5, 4], [5, 5], [5, 6], [5, 7],
                          [6, 4], [6, 5], [6, 6],
                          [7, 5]]
    assert pixelLocations == exp_pixelLocations
