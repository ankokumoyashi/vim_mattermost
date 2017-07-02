import requests
import json
import pdb
url = 'http://localhost:8065/api/v3/users/login'
method = 'POST'
headers = {"Content-Type": "application/json"}
f = open('login.json')
data = json.load(f)
response = requests.post(url, data=json.dumps(data), headers=headers).json()
pdb.set_trace()

