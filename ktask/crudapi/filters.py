import json

from models import ToDo, ToDoList


def lambda_handler(event, context):
    """
    crud lambda application...
    """
    headers = {
        "Content-Type": "application/json",
        "Access-Allow-Credentials": "false",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST,GET,PUT,DELETE,OPTIONS",
        "Access-Control-Max-Age": "86400",
    }

    filters = {
        "/get_by_list": "todolist",
        "/get_by_owner": "owner",
        "/get_by_status": "status",
        "/get_by_user": "user",
    }

    path = event["path"]
    querystring_parameters = event["queryStringParameters"]
    query_filter = querystring_parameters[filters[path]]

    if filters[path] == "todolist":
        queryset = ToDo.objects(todolist=query_filter).all()
    elif filters[path] == "owner":
        owner = query_filter.lower()
        if "list" in querystring_parameters.keys():
            list_mode = querystring_parameters["list"].lower() == "true"
            queryset = (
                ToDoList.objects(owner=owner).all()
                if list_mode
                else ToDo.objects(owner=owner).all()
            )
        else:
            queryset = list(ToDoList.objects(owner=owner).all()) + list(
                ToDo.objects(owner=owner).all()
            )

    elif filters[path] == "user":
        queryset = ToDoList.objects(owner=query_filter).all()
        tmp = ToDoList.objects.all()

        contrib = list(
            filter(
                lambda x: query_filter in x.access["contributors"]
                or query_filter in x.access["readers"],
                tmp,
            )
        )
        queryset = list(queryset) + contrib
    else:
        status = query_filter.lower()
        if "list" in querystring_parameters.keys():
            list_mode = querystring_parameters["list"].lower() == "true"
            queryset = (
                ToDoList.objects(status=status).all()
                if list_mode
                else ToDo.objects(status=status).all()
            )
        else:
            queryset = list(ToDoList.objects(status=status).all()) + list(
                ToDo.objects(status=status).all()
            )

    queryset = [x.serialize() for x in queryset]

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(
            queryset,
        ),
    }
