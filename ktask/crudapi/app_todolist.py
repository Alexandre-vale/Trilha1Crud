import json
from datetime import date, datetime

import mongoengine
from bson import ObjectId
from decouple import config

from models import ToDoList


def lambda_handler(event, context):
    mongoengine.connect(
        host=config("MONGO_URL"),
    )
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
            queryset = ToDoList.objects(id=ObjectId(params["id"][0])).first().serialize()
        else:
            queryset = [todolist.serialize() for todolist in ToDoList.objects.all()]

        return {
            "statusCode": 200,
            "body": json.dumps(queryset),
        }

    if method == "POST":
        deadline = [int(i) for i in body["deadline"].split("-")]
        notification = [int(i) for i in body["notification"].split("-")]

        ToDoList.objects.create(
            name=body["name"],
            description=body["description"],
            owner=body["owner"],
            access=body["access"],
            todos=body["todos"],
            created_at=datetime.now(),
            last_update={"user": body["owner"], "date": datetime.now(), "todo": None},
            deadline=date(year=deadline[0], month=deadline[1], day=deadline[2]),
            notification=date(
                year=notification[0], month=notification[1], day=notification[2]
            ),
            status=body["status"],
        ).save()

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "created"
                }
            )
        }

    if method == "PUT":
        id = ObjectId(params["id"][0])
        ToDoList.objects(id=id).update(**body)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "updated"
                }
            )
        }

    if method == "DELETE":
        id = ObjectId(params["id"][0])
        ToDoList.objects(id=id).delete()

    return {"statusCode": 404}
