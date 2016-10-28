import requests
from requests import ConnectionError


def _list(base_url, args):
    response = requests.get(base_url + '/list', auth=('user', 'pass'))
    print response.json()


def _get(base_url, args):
    for file_name in args:
        route = '/get?file_name={file_name}'.format(file_name=file_name)
        response = requests.get(base_url + route, auth=('user', 'pass'))

        if response.status_code == 404:
            print 'no such file!'

        with open('files/' + file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print 'received file {file_name}'.format(file_name=file_name)


def _put(base_url, args):
    files = {}
    for file_name in args:
        files.update({file_name: open('files/' + file_name, 'rb')})
    response = requests.post(base_url + '/put', files=files)
    print response.json


def _connect(ip, port):
    print 'trying to issue connection'
    base_url = 'http://{ip}:{port}'.format(ip=ip, port=port)
    try:
        r = requests.get(base_url + '/connect', auth=('user', 'pass'))
    except ConnectionError:
        print 'Error connecting to server'
        return None
    if r.status_code == 200:
        print 'connected'
    return base_url


mapping = {'list': _list, 'get': _get, 'put': _put}


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