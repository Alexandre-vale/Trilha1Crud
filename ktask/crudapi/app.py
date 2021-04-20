from decouple import config
import json
import mongoengine

from bson import ObjectId
from datetime import datetime, date

from models import ToDo
import filters



def lambda_handler(event, context):
    """
    crud lambda application...
    """
    path = event["path"]

    if path == "/get_by_status" or path == "/get_by_owner":
        return filters.lambda_handler(event, context)


    mongoengine.connect(
        host=config("MONGO_URL"),
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
            contribuitors=f["contribuitors"],
            created_at=datetime.now(),
            last_update=datetime.now(),
            deadline=date(year=deadline[0], month=deadline[1], day=deadline[2]),
            notification=date(
                year=notification[0], month=notification[1], day=notification[2]
            ),
            status=False,
        ).save()
        message = [ToDo.objects(name=f["name"]).first().serialize()]

    elif method == "PUT":
        _id = ObjectId(querystring_parameters["id"][0])
        ToDo.objects(id=_id).update(**f)
        message = [ToDo.objects(id=_id).first().serialize()]

    elif method == "DELETE":
        _id = ObjectId(querystring_parameters["id"][0])
        ToDo.objects(id=_id).first().delete()
        message = "Object deleted sucessfully"

    else:
        message = ([i.serialize() for i in ToDo.objects.all()],)

    return {
        "statusCode": status[method.lower()],
        "body": json.dumps(
            {"Todo": message},
        ),
    }
