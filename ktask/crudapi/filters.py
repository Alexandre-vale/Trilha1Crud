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
        "/get_from_user": "contribuitor",
    }

    path = event["path"]
    querystring_parameters = event["queryStringParameters"]
    query_filter = querystring_parameters[filters[path]]

    if filters[path] == "todolist":
        queryset = ToDo.objects(todolist=query_filter).all()

    # elif filters[path] == "owner": Aqui esta o anterior, caso tentar fazer um novo por minha parte falhe
    #     queryset = ToDo.objects(owner=query_filter).all()

    elif filters[path] == "owner": #quase igual ao que fizemos juntos, mas adicionei uns passos a mais quando se trata de nome próprios
        status = query_filter #recebendo o param cru caso os nomes sejam case sensitive
        if "list" in querystring_parameters.keys():
            list_mode = querystring_parameters["list"] == "True"
            queryset = (
                ToDoList.objects(status=status).all()
                if list_mode
                else ToDo.objects(status=status).all()
            )
            if not queryset: #se a lista retornar vazia, tentar com o nome todo lowercase
                status = query_filter.lower()
                queryset = (
                ToDoList.objects(status=status).all()
                if list_mode
                else ToDo.objects(status=status).all()
            )
        else:
            queryset = (
                list(ToDoList.objects(status=status).all())
                + list(ToDo.objects(status=status).all())
            )
            if not queryset: #mesma coisa aqui
                status = query_filter.lower()
                queryset = (
                list(ToDoList.objects(status=status).all())
                + list(ToDo.objects(status=status).all())
                )

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
        if "list" in querystring_parameters.keys():
            list_mode = querystring_parameters["list"] == "True"
            queryset = (
                ToDoList.objects(status=status).all()
                if list_mode
                else ToDo.objects(status=status).all()
            )
        else:
            queryset = (
                list(ToDoList.objects(status=status).all())
                + list(ToDo.objects(status=status).all())
            )

    queryset = [todo.serialize() for todo in queryset]

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(
            queryset,
        ),
    }
