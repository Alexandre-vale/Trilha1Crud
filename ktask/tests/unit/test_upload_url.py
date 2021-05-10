import json

import pytest

from ktask.upload import app


@pytest.fixture()
def api_event():
    return {
        "path": "/get_upload_url",
        "queryStringParameters": {"key": "abobora"},
        "httpMethod": "GET"
    }


def test_url(api_event):
    res = app.lambda_handler(api_event, "")
    body = json.loads(res["body"])

    assert res["statusCode"] == 200
    assert body[-1]["url"]
