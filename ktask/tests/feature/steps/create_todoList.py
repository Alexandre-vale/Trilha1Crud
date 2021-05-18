from behave import given, when, then, step
import requests
import json 

@given('A user whit valid acess tokens')
def set_access_token_in_header(context):
    context.headers = {"Authorization": "Bearer" + "<YOUR_ACCESS_TOKEN>"}

@step('the user wants create a todolist with name as "Object Oriented work"')
def set_name(context):
    context.request_body = {"name": "Object Oriented work"}

@step('the description of the todolist is "Intenface studies"')
def set_description(context):
    context.request_body['description'] = "Intenface studies"

@step('owner of the todolist is "fulano@gmail.com"')
def set_owner(context):
    context.request_body['owner'] = "fulano@gmail.com"

@step('access as a todolist contribution is "fuba2@gmail.com"')
def set_access_contributor(context):
    context.request_body['access'] = {"contributors": ["fuba2@gmail.com"]}

@step('reader access as a todolist  is "bolinho@gmail.com"')
def set_access_reader(context):
    context.request_body['access']['readers'] = ["bolinho@gmail.com"]

@step('the todolist deadline date is "2021-05-02"')
def set_creation_date(context):
    context.request_body['deadline'] = "2021-05-02"

@when('user submits the todolist data in "{url}"')
def execute_post_request_for_todolist_creation(context, url):
    body = context.request_body
    response = requests.post(url, headers = context.headers, json = body)
    context.status_code = response.status_code
    context.response_body = response.json()

@then('you should receive a "{status}" status code')
def check_status_code(context, status):
    statu = context.status_code
    assert int(status) == statu
    

@step('name "{name}" should be in response body')
def check_name(context, name):
    body = context.response_body
    assert body['name'] == name

@step('description "{description}" should be in response body')
def check_description(context, description):
    assert context.response_body['description'] == description

@step('owner "{owner}" should be in response body')
def check_owner(context, owner):
    assert context.response_body['owner'] == owner

@step('acess contributor "{contributors}" should be in response body')
def set_access_contributor(context, contributors): 
    assert context.response_body['access']['contributors'] == [contributors]

@step('access reader "{readers}" should be in response body')
def set_access_reader(context, readers):
    assert  context.response_body['access']['readers'] == [readers]

@step('deadline date "{deadline}" should be in response body')
def check_creation_date(context, deadline):
    assert context.response_body['deadline'] == deadline