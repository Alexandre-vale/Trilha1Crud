import json

import pytest

from ktask.crudapi import app

SAMPLE_EVENT = {
    "body": '{ "test": "body"}',
    "resource": "/{proxy+}",
    "requestContext": {
        "resourceId": "123456",
        "apiId": "1234567890",
        "resourcePath": "/{proxy+}",
        "httpMethod": "GET",
        "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
        "accountId": "123456789012",
        "identity": {
            "apiKey": "",
            "userArn": "",
            "cognitoAuthenticationType": "",
            "caller": "",
            "userAgent": "Custom User Agent String",
            "user": "",
            "cognitoIdentityPoolId": "",
            "cognitoIdentityId": "",
            "cognitoAuthenticationProvider": "",
            "sourceIp": "127.0.0.1",
            "accountId": "",
        },
        "stage": "prod",
    },
    "multiValueQueryStringParameters": None,
    "headers": {
        "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
        "Accept-Language": "en-US,en;q=0.8",
        "CloudFront-Is-Desktop-Viewer": "true",
        "CloudFront-Is-SmartTV-Viewer": "false",
        "CloudFront-Is-Mobile-Viewer": "false",
        "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
        "CloudFront-Viewer-Country": "US",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "X-Forwarded-Port": "443",
        "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
        "X-Forwarded-Proto": "https",
        "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
        "CloudFront-Is-Tablet-Viewer": "false",
        "Cache-Control": "max-age=0",
        "User-Agent": "Custom User Agent String",
        "CloudFront-Forwarded-Proto": "https",
        "Accept-Encoding": "gzip, deflate, sdch",
    },
    "pathParameters": {"proxy": "/examplepath"},
    "httpMethod": "GET",
    "stageVariables": {"baz": "qux"},
    "path": "/todo",
}


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return SAMPLE_EVENT


@pytest.fixture()
def apigw_post_event():
    data = SAMPLE_EVENT
    data["httpMethod"] = "POST"
    data[
        "body"
    ] = """{
        "name": "teste todo",
        "body": "teste body",
        "owner": "teste@teste.com",
        "todolist": "6086c4662d7de51e39c60293",
        "assigment": "teste@teste.com",
        "deadline": "2021-06-15",
        "notification": "2021-05-26",
        "attachments": {"files": []},
        "status": "todo"
    }"""

    return data


@pytest.fixture()
def apigw_put_event(apigw_event):
    ret = app.lambda_handler(apigw_event, "")
    id = json.loads(ret["body"])[-1]["id"]
    data = SAMPLE_EVENT
    data["httpMethod"] = "PUT"
    data["multiValueQueryStringParameters"] = {
        "id": [
            id,
        ]
    }
    data[
        "body"
    ] = """
        {"name": "Testezin", "status": "done", "user": "boladefogo@teste.com"}
    """

    return data


@pytest.fixture()
def apigw_get_by_status_event(apigw_event):
    data = apigw_event
    data["path"] = "/get_by_status"
    data["multiValueQueryStringParameters"] = {
        "status": [
            "done",
        ]
    }

    return data


@pytest.fixture()
def apigw_get_by_owner_event(apigw_event):
    data = apigw_event
    data["path"] = "/get_by_owner"
    data["multiValueQueryStringParameters"] = {
        "owner": [
            "teste@teste.com",
        ]
    }

    return data


@pytest.fixture()
def apigw_delete_event(apigw_event):
    ret = app.lambda_handler(apigw_event, "")
    id = json.loads(ret["body"])[-1]["id"]
    data = SAMPLE_EVENT
    data["httpMethod"] = "DELETE"
    data["multiValueQueryStringParameters"] = {"id": [id]}
    data["path"] = "/todo"

    return data




def test_create_todo(apigw_post_event):
    ret = app.lambda_handler(apigw_post_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert data[0]["name"].strip() == "teste todo"


def test_get_all_todos(apigw_event):
    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert data[0]["name"].strip() == "teste todo"
    assert data[0]["body"].strip() == "teste body"


def test_update_todo(apigw_put_event):
    ret = app.lambda_handler(apigw_put_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert data["name"].strip() == "teste todo"


def test_filter_by_status(apigw_get_by_status_event):
    ret = app.lambda_handler(apigw_get_by_status_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert data[0]["status"] == "done"


def test_filter_by_owner(apigw_get_by_owner_event):
    ret = app.lambda_handler(apigw_get_by_owner_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert data[0]["owner"] == "teste@teste.com"


def test_delete_todo(apigw_delete_event):
    ret = app.lambda_handler(apigw_delete_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 404
    assert data == "Object deleted sucessfully"
