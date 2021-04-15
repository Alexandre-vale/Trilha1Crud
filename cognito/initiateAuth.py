import boto3

# username = 'Alexandre'
# password = '#Jej1234'
#cliId = 'vjmavfrop927pfnk9jn15h2ft'\

def InitiateAutentication(password, username, cliId):
    client = boto3.client('cognito-idp', region_name='sa-east-1')

    response = client.initiate_auth(ClientId=cliId, AuthFlow='USER_PASSWORD_AUTH', AuthParameters={'USERNAME': username,'PASSWORD': password})

    return response

# print('Access Token', response['AuthenticationResult']['AccessToken'])
# print('Refresh Token', response['AuthenticationResult']['RefreshToken'])