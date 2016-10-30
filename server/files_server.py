from flask import Flask, request, jsonify
from flask import send_from_directory
from server.config import config
import os

from werkzeug.utils import secure_filename
from flask_hmacauth import hmac_auth, DictAccountBroker, HmacManager

app = Flask(__name__)


accountmgr = DictAccountBroker(
    accounts={
        "admin": {"secret": ";hi^897t7utf", "rights": ["connect", "list", "get", "put"]},
        "editor": {"secret": "afstr5afewr", "rights": ["connect", "list", "get"]},
        "guest": {"secret": "ASDFjoiu%i", "rights": ["connect", "list"]}
    })

hmacmgr = HmacManager(accountmgr, app)


@app.route('/connect')
@hmac_auth('connect')
def connect():
    return jsonify({'success': True})


@app.route('/list')
@hmac_auth('list')
def files_list():
    files = os.listdir("files")
    return jsonify({'files': files})


@app.route('/get')
@hmac_auth('get')
def get_file():
    file_name = request.args.get('file_name')
    return send_from_directory('files', file_name)


@app.route('/put', methods=['POST'])
@hmac_auth('put')
def put_file():
    files = request.files
    saved_files = 0
    for file_name, file_content in files.iteritems():
        file_content.save(os.path.join('files', secure_filename(file_name)))
        saved_files += 1
    return jsonify({'upladed files': saved_files})


if __name__ == '__main__':
    # for deploying without uwsgi
    app.run(host=config.get('ip'), port=config.get('port'))
