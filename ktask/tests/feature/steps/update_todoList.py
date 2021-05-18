from behave import given, when, then, step
import requests
import json 

@step('the todolist id to be changed is "60a2e24e433effaba1e58f27"')
def set_id(context):
    id = context.request_params_id
    id = "60a2e24e433effaba1e58f27"

@step('the description will be changed by "testando criação de todolista  sobre orinetação objeto"')
def set_update_description(context):
    context.request_body['description'] = "testando criação de todolista  sobre orinetação objeto"

@when('user submits the todolist data for update in "{url}"')
def execute_put_request_for_todolist_update(context, url, id):
    body = context.request_body
    response = requests.put(url + id, headers = context.headers, json = body)
    context.status_code = response.status_code
    context.response_body = response.json()

@step('id {id} should be in response parameter')
def check_id(context):
    assert context.response_params_id == id

@step('description for update is  "{description}" should be in response body')
def check_description_update(context, description):
    assert context.response_body['description'] == description