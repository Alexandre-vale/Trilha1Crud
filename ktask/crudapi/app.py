import json
from datetime import date, datetime
from dbm.ndbm import _dbm

import mongoengine
from bson import ObjectId
from decouple import config

import app_todolist, filters
from models import ToDo, ToDoList


def lambda_handler(event, context):
    """
    crud lambda application...
    """
    path = event["path"]
    filter_paths = [
        "/get_by_status",
        "/get_by_owner",
        "/get_by_list"
    ]

    if path in filter_paths:
        return filters.lambda_handler(event, context)

    if path == "/todolist":
        return app_todolist.lambda_handler(event, context)
 
    mongoengine.connect(
        host=config("MONGO_URL"), _db=config("MONGO_DB")
    )

    status = {"get": 200, "post": 200, "put": 200, "delete": 404}
    method = event["httpMethod"]

    body = event["body"]
    f = json.loads(body) if body else {}
    querystring_parameters = event["multiValueQueryStringParameters"]

    if method == "POST":
        deadline = [int(i) for i in f["deadline"].split("-")]
        notification = [int(i) for i in f["notification"].split("-")]

        ToDo.objects.create(
            name=f["name"],
            body=f["body"],
            owner=f["owner"],
            todolist=f["todolist"],
            assigment=f["assigment"],
            created_at=datetime.now(),
            last_update={"user": f["owner"], "date": datetime.now()},
            deadline=date(year=deadline[0], month=deadline[1], day=deadline[2]),
            notification=date(
                year=notification[0], month=notification[1], day=notification[2]
            ),
            attachments=f["attachments"],
            status=f["status"],
        ).save()
        message = [ToDo.objects(name=f["name"]).first().serialize()]

    elif method == "PUT":
        _id = ObjectId(querystring_parameters["id"][0])
        obj = ToDo.objects(id=_id).first()
        d = obj.last_update
        d["user"] = f["user"]
        d["date"] = datetime.now()
        f.pop("user")
        f["last_update"] = d
        obj.update(**f)
        d["todo"] = str(obj.pk)
        ToDoList.objects(id=ObjectId(obj.todolist)).update(last_update=d)
        message = obj.serialize()

    elif method == "DELETE":
        _id = ObjectId(querystring_parameters["id"][0])
        ToDo.objects(id=_id).first().delete()
        message = "Object deleted sucessfully"

    else:
        message = [i.serialize() for i in ToDo.objects.all()]

    return {
        "statusCode": status[method.lower()],
        "body": json.dumps(
             message
        ),
    }
