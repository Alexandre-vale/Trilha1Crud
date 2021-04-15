# Processos do cognito

IMPORTANTE! cliId é o client ID da user_pool do cognito, eu criei uma dummy usada para teste, porem pode ser usada no produto final tb, o codigo ja se encontra aqui

Nesta pasta temos as funções necessárias para todos os metodos de cognito, que são:  

Sign up: fornecendo email, username e senha podemos começar o processo de criação de uma conta, receberemos um codigo de confirmação no e-mail  
  
Resend E-mail Confirmation: Uma função simples que recebe o nome de usuario tentando abrir uma conta e manda outro e-mail de confirmação  
  
Confirm Sign Up: Usando o codigo de confirmação recebido no e-mail e as credenciais providenciadas, Confirmamos a conta com a verificação de e-mail.  

Initiate Authentication: Processo de Log in do usuario, usamos ele para receber um codigo de autenticação que sera usado em outras funções  

Get user: Utilizando o codigo de autenticação, podemos pegar as informações de usuario para leitura do aplicativo, bem importante

Forgot password: Usuario providencia seu username para requisitar uma nova senha, ele recebera um codigo de confirmação no e-mail  

Confirm forgotten password: Usando o codigo de email e colocando uma nova senha, confirmamos que o processo de troca de senha vai acontecer

Change password: Esta função faz a mudança de senha definitivamente no cognito  
