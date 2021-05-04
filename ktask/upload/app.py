import boto3
from botocore.config import Config
from decouple import config

import json


def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, PUT, DELETE, OPTIONS",
        "Access-Control-Max-Age": 86400
    }

    key = event["queryStringParameters"]["key"]

    url = boto3.client(
        "s3",
        aws_access_key_id=config("KEY"),
        aws_secret_access_key=config("SECRET_KEY"),
        config=Config(signature_version='s3v4'),
        region_name='sa-east-1'
    ).generate_presigned_url(
        "put_object",
        Params={"Bucket": config("BUCKET_NAME"), "Key": key},
        ExpiresIn=3600,
        HttpMethod="PUT",
    )

    return {"headers": headers, "statusCode": 200, "body": json.dumps(url)}
