import json
import logging
import os
import dateutil
from flask import jsonify, request, Flask
from fluent import sender
from minio import Minio

from definitions import FLUENT_ADDRESS, DEBUG, MINIO_ADDRESS
from lib_logs.logger_fluent_flask import log

app = Flask(__name__)
sender.setup(__name__, host=FLUENT_ADDRESS)
app.logger.setLevel(logging.INFO)
mc = Minio(('localhost' if DEBUG else MINIO_ADDRESS) + ':9000',
           access_key=os.environ.get('MINIO_ACCESS_KEY', 'minio'),
           secret_key=os.environ.get('MINIO_SECRET_KEY', 'minio123'),
           secure=False)


@app.route("/", methods=['POST'])
def get_logs():
    method_name = 'get_logs'
    req_json = request.json
    log(method_name, req_json)
    uuid_str_requested = req_json['uuid_requested']
    mn = dateutil.parser.parse(req_json['minute'])
    bucket_name = 'logs'
    list_log_file = list(mc.list_objects(bucket_name, mn.strftime('%Y-%m-%d-%H:%M')))
    res = []
    for log_file in list_log_file:
        log_file_content = mc.get_object(log_file.bucket_name, log_file.object_name).read().decode()
        log_file_content = log_file_content.split('\n')
        for log_file_content_line in log_file_content:
            if log_file_content_line == '':
                continue
            log_file_content_line = log_file_content_line.split('\t')
            timestamp = log_file_content_line[0]
            tag = log_file_content_line[1]
            json_log = json.loads(log_file_content_line[2])
            if 'uuid_str' not in json_log:
                continue
            uuid_str = json_log['uuid_str']
            if uuid_str == uuid_str_requested:
                res.append({
                    'timestamp': timestamp,
                    'tag': tag,
                    'json_log': json_log
                })
    res = sorted(res, key=lambda k: k['timestamp'])
    return jsonify({'res': res})


@app.route("/ping", methods=['GET'])
def ping():
    return jsonify({'status': 'ok'})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8088)))
