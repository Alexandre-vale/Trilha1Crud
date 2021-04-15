import boto3

#Email = 'v-alexan@hotmail.com'
#username = 'Alexandre'
#password = '#Abc1234'
#confirmcode = '548422'
#cliId = 'vjmavfrop927pfnk9jn15h2ft'
def ConfirmSignUp(Email,username,password,confirmcode,cliId)
    client = boto3.client('cognito-idp', region_name='sa-east-1')
    response = client.confirm_sign_up(ClientId=cliId, Username=username, ConfirmationCode=confirmcode)

    return response