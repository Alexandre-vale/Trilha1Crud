import json

import pytest

from ...crudapi.app_todolist import lambda_handler
from .test_todo import SAMPLE_EVENT


@pytest.fixture()
def apigw_event():
    data = SAMPLE_EVENT
    data["queryStringParameters"] = {}
    data["httpMethod"] = "GET"
    data["path"] = "/todolist"
    return data


@pytest.fixture()
def apigw_post_event(apigw_event):
    data = SAMPLE_EVENT
    data["httpMethod"] = "POST"
    data[
        "body"
    ] = """{
          "name": "Teste 1 ",
          "description": "Teste 1 unit",
          "owner": "teste@teste.com",
          "todos": {"todos": []},
          "access": {  
            "readers": [],
            "contributors": []
          },
          "deadline": "2021-06-15",
          "notification": "2021-05-26",
          "status": "todo"
    }"""

    return data


@pytest.fixture()
def apigw_put_event(apigw_event):
    ret = lambda_handler(apigw_event, "")
    id = json.loads(ret["body"])[-1]["id"]
    data = SAMPLE_EVENT
    data["httpMethod"] = "PUT"
    data["body"] = """{"description": "Teste 1 unit updated"}"""
    data["queryStringParameters"] = {
        "id": id,
    }

    return data


@pytest.fixture()
def apigw_delete_event(apigw_event):
    data = SAMPLE_EVENT
    ret = lambda_handler(apigw_event, "")
    id = json.loads(ret["body"])[-1]["id"]

    data["httpMethod"] = "DELETE"
    data["queryStringParameters"] = {
        "id": id,
    }

    return data


def test_create_todo_list(apigw_post_event):
    ret = lambda_handler(apigw_post_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert data["name"].strip() == "Teste 1"


def test_get_all_todo_lists(apigw_event):

    res = lambda_handler(apigw_event, "")
    data = json.loads(res["body"])
    first = data[0]
    name = first["name"].strip()
    owner = first["owner"]

    assert res["statusCode"] == 200
    assert name == "Teste 1"
    assert owner == "teste@teste.com"


def test_get_one_todo_list(apigw_put_event):
    apigw_put_event["httpMethod"] = "GET"
    res = lambda_handler(apigw_put_event, "")
    first = json.loads(res["body"])

    assert res["statusCode"] == 200
    assert first["name"].strip() == "Teste 1"


def test_update_todo_list(apigw_put_event):
    res = lambda_handler(apigw_put_event, "")
    data = json.loads(res["body"])

    assert res["statusCode"] == 200
    # assert data["description"].strip() == "Teste 1 unit updated"


def test_delete_todo_list(apigw_delete_event):
    res = lambda_handler(apigw_delete_event, "")

    assert res["statusCode"] == 200
