import requests as rq

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def print_url_from_get():
    print(f'receiving get request')
    code = request.args.get('code')
    response = rq.post('https://todoapi.auth.sa-east-1.amazoncognito.com/oauth2/token',{'Content-Type':'application/x-www-form-urlencoded', 'grant_type': 'authorization_code', 'client_id': 'vjmavfrop927pfnk9jn15h2ft',  'code': code, 'redirect_uri': 'http://localhost:8000/'})
    response = response.json()
    print(response)
    print(code)
    return code

@app.route("/redirect", methods=["GET"])
def print_url_from_get_redirect():
    print(f'receiving get request')
    url = request.url
    print(url)
    return url



if __name__ == "__main__":
    app.run(port=8000)

#ssl_context='adhoc',
# url = 'https://todoapi.auth.sa-east-1.amazoncognito.com/login?response_type=code&client_id=vjmavfrop927pfnk9jn15h2ft&redirect_uri=http://localhost:8000/'
# authurl = 'https://todoapi.auth.sa-east-1.amazoncognito.com/oauth2/token'


# response = rq.get(url)

# print(response)

