import requests
import json

def send_request(url, method, payload=None, headers=None):
    headers = {'User-Agent': 'Mozilla/5.0'}
    #headers = {'Content-Type':'application/', 'User-Agent': 'Mozilla/5.0'}
    print method + " " +url
    if method == "GET":
        r = requests.get(url, headers=headers)
    elif method == "POST":
        r = requests.post(url, data=json.dumps(payload), headers=headers)
    elif method == "PUT":
        r = requests.put(url, data=json.dumps(payload), headers=headers)
    elif method == "DELETE":
        r = requests.delete(url, data=json.dumps(payload), headers=headers)
    if r.status_code != requests.codes.ok or r.status_code != 210: 
        r.raise_for_status()
    return r

