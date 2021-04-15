import boto3

# Email = 'v-alexan@hotmail.com'
# username = 'Alexandre'
# password = '#Abc1234'
#cliId = 'vjmavfrop927pfnk9jn15h2ft'

def SignUp(Email,username,password,cliId):

    client = boto3.client('cognito-idp', region_name='sa-east-1')
    response = client.sign_up(ClientId='vjmavfrop927pfnk9jn15h2ft', Username=username, Password=password,UserAttributes=[{'Name': 'email', 'Value': Email}])
    return response