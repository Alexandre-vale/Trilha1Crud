import boto3

#username = 'Alexandre'
#cliId = 'vjmavfrop927pfnk9jn15h2ft'
def ForgotPassword(username, cliId):
    client = boto3.client('cognito-idp', region_name='sa-east-1')

    response = client.forgot_password(ClientId=cliId, Username=username)

    return response