import json

import mongoengine
from bson import ObjectId
from decouple import config

from models import ToDo, ToDoList


def lambda_handler(event, context):
    """
    crud lambda application...
    """
    filters = {
        "/get_by_list": "todolist",
        "/get_by_owner": "owner",
        "/get_by_status": "status",
        "/get_from_user": "contribuitor",
    }

    path = event["path"]
    querystring_parameters = event["multiValueQueryStringParameters"]
    query_filter = querystring_parameters[filters[path]][0]

    if filters[path] == "todolist":
        queryset = ToDo.objects(todolist=query_filter).all()
    elif filters[path] == "owner":
        queryset = ToDo.objects(owner=query_filter).all()
    elif filters[path] == "contribuitor":
        queryset = ToDoList.objects(owner=query_filter).all()
        tmp = ToDoList.objects.all()

        contrib = list(
            filter(
                lambda x: query_filter in x.acces["contributors"]
                or query_filter in x.acess["readers"],
                tmp,
            )
        )

        queryset = list(queryset) + contrib
    else:
        status = query_filter.lower()
        queryset = ToDo.objects(status=status).all()

    queryset = [todo.serialize() for todo in queryset]

    return {
        "statusCode": 200,
        "body": json.dumps(
            queryset,
        ),
    }
