import boto3

# Email = 'v-alexan@hotmail.com'
# username = 'Alexandre'
# password = '#Abc1234'
#cliId = 'vjmavfrop927pfnk9jn15h2ft'

def ResendEmailConfirmation(username, cliId)
    client = boto3.client('cognito-idp', region_name='sa-east-1')
    response = client.resend_confirmation_code(ClientId=cliId, Username=username)
    return response