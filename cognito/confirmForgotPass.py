import boto3

#username = 'Alexandre'
#new_password = '#Jej1234'
#confirm_code = '455900'
#cliId = 'vjmavfrop927pfnk9jn15h2ft'
def ConfirmForgottenPassword(username,new_password,confirm_code, cliId):
    client = boto3.client('cognito-idp', region_name='sa-east-1')

    response = client.confirm_forgot_password(ClientId=cliId, Username=username, ConfirmationCode=confirm_code, Password=new_password)

    return response