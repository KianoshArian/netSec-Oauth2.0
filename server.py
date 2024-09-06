import uvicorn
from fastapi import FastAPI
import requests
import json

identityParams={
	'client_id': '4bfed6c21d4c0effd02b',
	'state': 'lothric987278999',
	'redirect_uri': 'http://localhost:8589/oauth/redirect',
	'scope': 'repo'
}
r = requests.get('https://github.com/login/oauth/authorize', params=identityParams)
print("please open the link below:")
print(r.url)

app = FastAPI()

@app.get("/oauth/redirect")
def oauth_redirect(code: str):
	print(f'Github code is: {code}')
	reqTokenParams={
		'client_id': '4bfed6c21d4c0effd02b',
		'client_secret': '***************',
		'code': code
	}
	r = requests.post('https://github.com/login/oauth/access_token', params=reqTokenParams)
	print('Access Token Is:')
	at=r.text[(r.text.index('=')+1):r.text.index('&')]
	print(at)
	authHeader={'Authorization': "Bearer " + at}
	r = requests.get('https://api.github.com/user', headers=authHeader)
	print('Profile Data:')
	print("UserName: " + json.loads(r.text)['login'])
	print("Id: " + str(json.loads(r.text)['id']))
	print("Avatar: " + json.loads(r.text)['avatar_url'])
	return f'Github code is: {code}'

if (__name__ == '__main__'):
	uvicorn.run(app, host= '0.0.0.0', port = 8589)
