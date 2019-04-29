import final_server as fs
import pytest

db = fs.db


def test_verifyFileName():
    # Positive testing
    qFileName_good = "slide1_0.tiff"
    file_exists, msg, data = fs.verifyFileName(qFileName_good)
    assert file_exists is True
    assert msg == "Filename "+qFileName_good+" is displayed above."

    # Negative testing
    qFileName_bad = "Zslide1_0.tiff"
    file_exists, msg, data = fs.verifyFileName(qFileName_bad)
    assert file_exists is False
    assert msg == "Filename "+qFileName_bad+" could not be found."
