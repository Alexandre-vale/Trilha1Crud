from decouple import config
import json
import mongoengine


from .models import ToDo


def lambda_handler(event, context):
    """
    crud lambda application...
    """
    mongoengine.connect(
        host=config("MONGO_URL"),
    )

    filters = {
        "/get_by_owner": "owner",
        "/get_by_status": "status",
    }

    path = event["path"]
    querystring_parameters = event["multiValueQueryStringParameters"]
    query_filter = querystring_parameters[filters[path]][0]

    if filters[path] == "owner":
        queryset = ToDo.objects(owner=query_filter).all()
    else:
        status = query_filter.lower() == "true"
        queryset = ToDo.objects(status=status).all()
    queryset = [todo.serialize() for todo in queryset]

    return {
        "statusCode": 200,
        "body": json.dumps(
            {"Todo": queryset},
        ),
    }
