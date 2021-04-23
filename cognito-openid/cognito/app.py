import json
import jwt
import requests


def lambda_handler(event, context):

    code = event["queryStringParameters"]["code"]
    
    secret = "aaa"
    response = requests.post(
        "https://todoapi.auth.sa-east-1.amazoncognito.com/oauth2/token",
        {
            "Content-Type": "application/x-www-form-urlencoded",
            "grant_type": "authorization_code",
            "client_id": "vjmavfrop927pfnk9jn15h2ft",
            "code": code,
            "redirect_uri": "http://localhost:3000/cognito",
        },
    )

    response = response.json()
    idtoken = response["id_token"]
    user = jwt.decode(
        idtoken, secret, algorithms=["RS256"], options={"verify_signature": False}
    )

    return {"statusCode": 200, "body": json.dumps(user)}
