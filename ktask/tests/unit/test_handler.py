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
        "path": "/examplepath",
    }


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return SAMPLE_EVENT


@pytest.fixture()
def apigw_post_event():
    data = SAMPLE_EVENT
    data["httpMethod"] = "POST"
    data["body"] = '''{
        "name": "Example",
        "body": "testetetetetete",
        "owner": "teste@teste.com",
        "contribuitors": {
        },
        "deadline": "2021-06-15",
        "notification": "2021-05-26"
    }'''

    return data


@pytest.fixture()
def apigw_put_event(apigw_post_event):
    ret = app.lambda_handler(apigw_post_event, "")
    id = json.loads(ret["body"])["Todo"][0]["id"]
    data = SAMPLE_EVENT
    data["httpMethod"] = "PUT"
    data["multiValueQueryStringParameters"] = {"id": [id,]}
    data["body"] = '{"name": "Testezin"}'

    return data


@pytest.fixture()
def apigw_delete_event(apigw_post_event):
    ret = app.lambda_handler(apigw_post_event, "")
    id = json.loads(ret["body"])["Todo"][0]["id"]
    data = SAMPLE_EVENT
    data["httpMethod"] = "DELETE"
    data["multiValueQueryStringParameters"] = {"id": [id]}

    return data


def test_get_all_todos(apigw_event):

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "Todo" in ret["body"]
    assert type(data["Todo"]) == list


def test_create_todo(apigw_post_event):
    ret = app.lambda_handler(apigw_post_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "Todo" in ret["body"]
    assert len(list(data["Todo"])) > 0


def test_update_todo(apigw_put_event):
    ret = app.lambda_handler(apigw_put_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert data["Todo"][0]["name"] == "Testezin"


def test_delete_todo(apigw_delete_event):
    ret = app.lambda_handler(apigw_delete_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 404