from flask import Flask, jsonify
from flask_cors import CORS
import webdisk


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/status', methods=['GET'])
def ping_pong():
    return jsonify('Ok')

@app.route('/host-info', methods=['GET'])
def all_storage():
    DEVICES = webdisk.get_disk_info()
    return jsonify({
        'status': 'success',
        'hosts': DEVICES
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0')