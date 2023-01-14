import os
import time
import json
import requests
import webbrowser
import getpass
from dotenv import load_dotenv
from base64 import b64encode

load_dotenv()

def get_token():
    client_id = os.environ.get('ONSHAPE_CLIENT_ID')
    client_secret = os.environ.get('ONSHAPE_CLIENT_SECRET')
    redirect_uri = os.environ.get('ONSHAPE_REDIRECT_URI')

    auth_url = f'https://cad.onshape.com/oauth/authorize?client_id={client_id}&response_type=code'
    print(f'Please go to the following URL to authorize the application: {auth_url}')
    webbrowser.open(auth_url)
    code = getpass.getpass('Enter the authorization code: ')

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    response = requests.post('https://cad.onshape.com/oauth/token', data=data, headers=headers)
    token_data = json.loads(response.text)
    token_data['expires_at'] = int(time.time()) + token_data['expires_in']
    with open('token.json', 'w') as f:
        json.dump(token_data, f)
    return token_data['access_token']

def check_token():
    if os.path.isfile('token.json'):
        with open('token.json') as f:
            token_data = json.load(f)
            if int(time.time()) < token_data['expires_at']:
                return token_data['access_token']
    return get_token()
