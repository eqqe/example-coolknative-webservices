import os
import logging
import traceback
from flask import Flask, jsonify, request
from fluent import sender
from minio import Minio

from definitions import FLUENT_ADDRESS, DEBUG, MINIO_ADDRESS
from lib_logs.logger_fluent_flask import log
from namespace1.asyncwebservice.utils import MyJob

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
sender.setup(__name__, host=FLUENT_ADDRESS)

pool = get_redis_connection_pool()
mc = Minio(('localhost' if DEBUG else MINIO_ADDRESS) + ':9000',
           access_key=os.environ.get('MINIO_ACCESS_KEY', 'minio'),
           secret_key=os.environ.get('MINIO_SECRET_KEY', 'minio123'),
           secure=False)


@app.route("/", methods=['POST'])
def app():
    method_name = 'app'
    req_json = request.json
    uuid_str = req_json['uuid_str']
    try:
        log(method_name, {'text': req_json['text'], 'uuid_str': uuid_str})
        my_job = MyJob(mc, req_json['text'])
        res = my_job.run()
        return jsonify(res)
    except Exception:
        log(method_name, {'traceback': traceback.format_exc(), 'uuid_str': uuid_str})
        return jsonify({'message': 'Error while training model', 'uuid_str': uuid_str}), 500


@app.route("/ping", methods=['GET'])
def ping():
    return jsonify({'status': 'ok'})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
