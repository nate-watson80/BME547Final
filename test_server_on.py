import final_server as fs
import pytest


def test_server_on():
    statusStr, statusCode = fs.server_on()
    exp_statusStr = "The server is up! Should be ready to rock and roll."
    exp_statusCode = 200
    assert statusStr == exp_statusStr
    assert statusCode == exp_statusCode
