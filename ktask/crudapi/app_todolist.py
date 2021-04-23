import mongoengine
from decouple import config

import json

from models import ToDoList


def lambda_handler(event, context):

    mongoengine.connect(config("MONGO_URL"))
    method = event["httpMethod"]

    if method == "GET":
        queryset = [todolist.serialize() for todolist in ToDoList.objects.all()]
        return {
            "status": 200,
            "body": json.dumps(queryset),
        }

    return {
        "status": 404
    }