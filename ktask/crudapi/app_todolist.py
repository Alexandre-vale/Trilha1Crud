import json
from datetime import date, datetime, timedelta

from bson import ObjectId
from models import ToDoList


def lambda_handler(event, context):

    headers = {
        "Content-Type": "application/json",
        "Access-Allow-Credentials": "false",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST,GET,PUT,DELETE,OPTIONS",
        "Access-Control-Max-Age": "86400",
    }

    method = event["httpMethod"]
    params = {}

    try:
        body = json.loads(event["body"])
    except TypeError:
        body = {}

    if event["queryStringParameters"]:
        params = event["queryStringParameters"]

    if method == "GET":
        if "id" in params.keys():
            queryset = ToDoList.objects(id=ObjectId(params["id"])).first().serialize()
        else:
            queryset = [todolist.serialize() for todolist in ToDoList.objects.all()]

        return {"statusCode": 200, "body": json.dumps(queryset), "headers": headers}

    if method == "POST":
        deadline = [int(i) for i in body["deadline"].split("-")]
        deadline = date(year=deadline[0], month=deadline[1], day=deadline[2])

        todo = ToDoList.objects.create(
            name=body["name"],
            description=body["description"],
            owner=body["owner"],
            access=body["access"],
            todos={"todo": []},
            created_at=datetime.now(),
            last_update={"user": body["owner"], "date": datetime.now(), "todo": None},
            deadline=deadline,
            notification=deadline - timedelta(days=3),
            status=None,
        ).save()

        return {
            "statusCode": 200,
            "body": json.dumps(todo.serialize()),
            "headers": headers,
        }

    if method == "PUT":
        if "access" in body.keys():
            for reader in body["access"]["readers"]:
                if (
                    body["access"]["readers"].count(reader) > 1
                    or reader in body["access"]["contributors"]
                ):
                    return {
                        "statusCode": 400,
                        "headers": headers,
                        "body": json.dumps(
                            "Este usuário já está adicionado ao projeto"
                        ),
                    }

            for contributor in body["access"]["contributors"]:
                if (
                    body["access"]["contributors"].count(contributor) > 1
                    or contributor in body["access"]["readers"]
                ):
                    return {
                        "statusCode": 400,
                        "headers": headers,
                        "body": json.dumps(
                            "Este usuário já está adicionado ao projeto"
                        ),
                    }

        id = ObjectId(params["id"])
        obj = ToDoList.objects(id=id).first()
        obj.update(**body)
        obj = ToDoList.objects(id=id).first()

        return {
            "statusCode": 200,
            "body": json.dumps(obj.serialize()),
            "headers": headers,
        }

    if method == "DELETE":
        id = ObjectId(params["id"])
        obj = ToDoList.objects(id=id).first()
        obj.delete()

        return {"statusCode": 200, "headers": headers}
