from flask import Flask, request, jsonify
from flask import send_from_directory
from server.config import config
import os

from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/connect')
def connect():
    return jsonify({'success': True})


@app.route('/list')
def files_list():
    files = os.listdir("files")
    return jsonify({'files': files})


@app.route('/get')
def get_file():
    file_name = request.args.get('file_name')
    return send_from_directory('files', file_name)


@app.route('/put', methods=['POST'])
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
