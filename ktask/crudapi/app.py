import json
from datetime import date, datetime, timedelta

import app_todolist
import filters
import mongoengine
from bson import ObjectId
from decouple import config
from models import ToDo, ToDoList
from mongoengine.errors import ValidationError


def lambda_handler(event, context):
    """
    crud lambda application...
    """

    db = config("MONGO_DB")
    host = config("MONGO_HOST")
    conn = mongoengine.connect(host=host, db=db)

    headers = {
        "Content-Type": "application/json",
        "Access-Allow-Credentials": "false",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST,GET,PUT,DELETE,OPTIONS",
        "Access-Control-Max-Age": "86400",
    }

    method = event["httpMethod"]
    path = event["path"]
    filter_paths = ["/get_by_status", "/get_by_owner", "/get_by_list"]
    status = {"get": 200, "post": 200, "put": 200, "delete": 200}
    body = event["body"]
    f = json.loads(body) if body else {}
    querystring_parameters = event["queryStringParameters"]

    if method == "OPTIONS":
        return {"statusCode": 204, "headers": headers}

    if path in filter_paths:
        return filters.lambda_handler(event, context)

    if path == "/todolist":
        return app_todolist.lambda_handler(event, context)

    if method == "POST":
        try:
            deadline = [int(i) for i in f["deadline"].split("-")]
            deadline = date(year=deadline[0], month=deadline[1], day=deadline[2])

            ToDo.objects.create(
                name=f["name"],
                body=f["body"],
                owner=f["owner"],
                todolist=f["todolist"],
                assigment=f["assigment"],
                created_at=datetime.now(),
                last_update={"user": f["owner"], "date": datetime.now()},
                deadline=deadline,
                notification=deadline - timedelta(days=3),
                attachments=f["attachments"],
                status=None,
            ).save()
            message = [ToDo.objects(name=f["name"]).first().serialize()]
        except (ValidationError, KeyError):
            return {
                "statusCode": 500,
                "headers": headers,
                "body": json.dumps("Invalid request body"),
            }

    elif method == "PUT":
        try:
            _id = ObjectId(querystring_parameters["id"])
            obj = ToDo.objects(id=_id).first()
            d = obj.last_update
            # d["user"] = f["user"]
            d["date"] = datetime.now()
            # f.pop("user")
            f["last_update"] = d
            obj.update(**f)
            d["todo"] = str(obj.pk)
            ToDoList.objects(id=ObjectId(obj.todolist)).update(last_update=d)
            obj = ToDo.objects(id=_id).first()
            message = obj.serialize()
        except (ValidationError, KeyError) as e:
            return {"statusCode": 500, "headers": headers, "body": json.dumps(e)}

    elif method == "DELETE":
        _id = ObjectId(querystring_parameters["id"])
        ToDo.objects(id=_id).first().delete()
        message = "Object deleted successfully"

    else:
        message = [i.serialize() for i in ToDo.objects.all()]

    return {
        "headers": headers,
        "statusCode": status[method.lower()],
        "body": json.dumps(message),
    }
