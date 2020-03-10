import logging
import os
import traceback

from flask import Flask, request, jsonify
from fluent import sender

from definitions import FLUENT_ADDRESS
from lib_logs.logger_fluent_flask import log
from namespace1.webservice.utils import MyHandler

app = Flask(__name__)
sender.setup(__name__, host=FLUENT_ADDRESS)
app.logger.setLevel(logging.INFO)


@app.route("/", methods=['POST'])
def webservice():
    method_name = 'webservice'
    req_json = request.json
    try:
        my_handler = MyHandler(req_json['data'], req_json['uuid_str'])
        res = my_handler.handle()
        return jsonify(res)
    except:
        log(method_name, {'traceback': traceback.format_exc(), 'uuid_str': req_json['uuid_str']})
        return jsonify({'message': 'Error', 'uuid_str': req_json['uuid_str']}), 500


@app.route("/ping", methods=['GET'])
def ping():
    return jsonify({'status': 'ok'})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8086)))
