import hashlib

import hmac
import json

import requests
import time
from requests import ConnectionError

CLIENT_SECRET = ';hi^897t7utf'
ACCOUNT_ID = "ACCOUNT_ID=admin"


def _list(base_url, args):
    route = '/list'
    route, hmac_sig = _create_hmac_signature('GET', route)
    response = requests.get(base_url+route, headers={'X-Auth-Signature': hmac_sig})
    print response.json()


def _get(base_url, args):
    for file_name in args:
        route = '/get?file_name={file_name}'.format(file_name=file_name)
        route, hmac_sig = _create_hmac_signature('GET', route)
        response = requests.get(base_url+route, headers={'X-Auth-Signature': hmac_sig})

        if response.status_code == 404:
            print 'no such file!'

        with open('files/' + file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print 'received file {file_name}'.format(file_name=file_name)


def _put(base_url, args):
    route = '/put'
    files = {}
    for file_name in args:
        files.update({file_name: open('files/' + file_name, 'rb')})
    route, hmac_sig = _create_hmac_signature('PUT', route, data=files)
    response = requests.post(base_url + route, files=files,
                             headers={'X-Auth-Signature': hmac_sig})
    print response.json


def _connect(ip, port):
    print 'trying to issue connection'
    base_url = 'http://{ip}:{port}'.format(ip=ip, port=port)
    route = '/connect'
    route, hmac_sig = _create_hmac_signature('GET', route)
    try:
        r = requests.get(base_url + route, headers={'X-Auth-Signature': hmac_sig})
    except ConnectionError:
        print 'Error connecting to server'
        return None
    if r.status_code == 200:
        print 'connected'
    elif r.status_code == 403:
        print 'could not connect to server, please  check credentials'
        return None
    return base_url


mapping = {'list': _list, 'get': _get, 'put': _put}


def _create_hmac_signature(method, query_string, data=None):
    msg = query_string + "?TIMESTAMP={ts}&ACCOUNT_ID={aid}".format(ts=str(int(time.time())),
                                                                   aid=ACCOUNT_ID)

    route = str(msg)
    if data is not None and method == 'POST':
        msg += json.dumps(data)

    return route, hmac.new(CLIENT_SECRET, digestmod=hashlib.sha1, msg=msg).hexdigest()


def main():

    while True:
        ip = raw_input("Please type server ip: ")
        port = raw_input("Please type server port: ")
        base_url = _connect(ip, port)
        if base_url is not None:
            break

    while True:
        args = raw_input("Please type command and arguments: ").split(' ')
        command = args.pop(0)
        callback = mapping.get(command)

        if callback is None:
            print('invalid command')
            continue

        callback(base_url, args)


if __name__ == '__main__':
    main()