import json
from datetime import date, datetime

import mongoengine
from bson import ObjectId
from decouple import config

from models import ToDoList


def lambda_handler(event, context):
    method = event["httpMethod"]
    params = {}

    try:
        body = json.loads(event["body"])
    except TypeError:
        body = {}

    if event["multiValueQueryStringParameters"]:
        params = event["multiValueQueryStringParameters"]

    if method == "GET":
        if "id" in params.keys():
            queryset = (
                ToDoList.objects(id=ObjectId(params["id"][0])).first().serialize()
            )
        else:
            queryset = [todolist.serialize() for todolist in ToDoList.objects.all()]

        return {
            "statusCode": 200,
            "body": json.dumps(queryset),
        }

    if method == "POST" or method == "OPTIONS":
        deadline = [int(i) for i in body["deadline"].split("-")]
        notification = [int(i) for i in body["notification"].split("-")]

        todo = ToDoList.objects.create(
            name=body["name"],
            description=body["description"],
            owner=body["owner"],
            access=body["access"],
            todos={"todo": []},
            created_at=datetime.now(),
            last_update={"user": body["owner"], "date": datetime.now(), "todo": None},
            deadline=date(year=deadline[0], month=deadline[1], day=deadline[2]),
            notification=date(
                year=notification[0], month=notification[1], day=notification[2]
            ),
            status=None,
        ).save()

        return {
            "statusCode": 200,
            "body": json.dumps(todo.serialize()),
        }

    if method == "PUT":
        id = ObjectId(params["id"][0])
        obj = ToDoList.objects(id=id).first()
        obj.update(**body)

        return {"statusCode": 200, "body": json.dumps(obj.serialize())}

    if method == "DELETE":
        id = ObjectId(params["id"][0])
        ToDoList.objects(id=id).delete()

        return {"statusCode": 404}
