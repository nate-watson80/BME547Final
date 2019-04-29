import final_server as fs
import pytest
from flask import Flask, jsonify, request

app = Flask(__name__)


def test_pullAllData():
    with app.app_context():
        json_payload, http_status = fs.pullAllData()
        payload = json_payload.json
        exp_payload = {
                        "background": 3860.4447940978507,
                        "filename": "slide1_0.tiff",
                        "spots": 47907.341194370485
                      }
        exp_http_status = 200
        assert payload["background"][0] == exp_payload["background"]
        assert payload["filename"][0] == exp_payload["filename"]
        assert payload["spots"][0][0] == exp_payload["spots"]
        assert http_status == exp_http_status
