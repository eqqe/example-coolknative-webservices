import os
import traceback
import requests
import logging
from flask import Flask, jsonify, request
import redis
from api_utils.utils import secured_with_token, with_request_params
from definitions import FLUENT_ADDRESS, EVENT_LISTENER_TEKTON_ADDRESS, GET_LOGS_KNATIVE_MONITORING_ADDRESS, DEBUG, \
    REDIS_ADDRESS
from lib_logs.logger_fluent_flask import log
from fluent import sender

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
model_type = os.environ.get('MODEL_TYPE', 'document')
app_name = model_type + '-type-guessing'
sender.setup(app_name, host=FLUENT_ADDRESS)
pool = redis.ConnectionPool(host='localhost' if DEBUG else REDIS_ADDRESS, port=6379, db=0)
r = redis.Redis(connection_pool=pool)


@app.route("/ping", methods=['GET'])
@secured_with_token()
def ping():
    status = {"status": "ok"}
    log('ping', status)
    return jsonify(status)


@app.route("/health", methods=['GET'])
@secured_with_token()
def health():
    urls_to_ping = ['http://webservice.namespace1/ping', 'http://asyncwebservice.namespace1/ping',
                    'http://minio-hl-svc.minio:9000/minio/health/live',
                    GET_LOGS_KNATIVE_MONITORING_ADDRESS + 'ping']
    status = {}
    status_up_all = True
    for utp in urls_to_ping:
        status[utp], status_up = get_status(utp)
        status_up_all = status_up_all and status_up
    urls_to_ping_minio = []
    for utp in urls_to_ping_minio:
        status[utp], status_up = get_status(utp)
        status_up_all = status_up_all and status_up
    status_redis_up = r.ping()
    status_up_all = status_up_all and status_redis_up
    status['redis'] = {'status': 'ok'} if status_redis_up else {'status': 'down'}
    log('health', status)
    if status_up_all:
        return jsonify(status)
    else:
        return jsonify(status), 500


def get_status(utp):
    status_ok_constant = {'status': 'ok'}
    status_down_constant = {'status': 'down'}
    try:
        resp = requests.get(utp, timeout=2)
    except requests.exceptions.RequestException as e:
        return status_down_constant, False
    if resp.ok:
        return status_ok_constant, True
    else:
        return status_down_constant, False


@app.route("/webservice-1", methods=['POST'])
@secured_with_token()
@with_request_params(r, model_type, ["param1"])
def webservice1(param1, data, uuid_str, version):
    method_name = 'predict'
    error_message = {'message': 'Error while doing prediction', 'uuid_str': uuid_str}
    try:
        data_json = {'client_id': client_id, 'data': data, 'model_type': model_type, 'uuid_str': uuid_str}
        if version == 'legacy':
            predict_url_base = 'http://predict-' + model_type
        else:
            predict_url_base = 'http://predict'
        predict_address = 'http://localhost:8085' if app.debug else predict_url_base + '.' + version
        resp = requests.post(predict_address, json=data_json)
        if resp.status_code != 200:
            log(method_name, error_message)
            return jsonify(error_message), 500
        res = resp.json()
        res['uuid_str'] = uuid_str
        return jsonify(res)
    except requests.exceptions.ConnectionError as e:
        message = 'Error while doing prediction: ' + 'Cannot send POST request to webservice prediction. '
        message += str(e) + ' Is the webservice running?'
        log_error_message = {'message': message, 'uuid_str': uuid_str}
        log(method_name, log_error_message)
        return jsonify(error_message), 500
    except:
        log(method_name, {'traceback': traceback.format_exc()})
        return jsonify(error_message), 500


@app.route("/post_feedback", methods=['POST'])
@secured_with_token()
@with_request_params(r, model_type, ["client_id", "data", "label"])
def post_feedback(client_id, data, label, uuid_str, version):
    method_name = 'post_feedback'
    error_message = {'message': 'Error while sending feedback', 'uuid_str': uuid_str}
    try:
        if version == 'legacy':
            return jsonify({'result': 'acquired and feedback', 'uuid_str': uuid_str})
        data_json = {
            'client_id': client_id,
            'data': data,
            'label': label,
            'model_type': model_type,
            'uuid_str': uuid_str
        }
        feedback_address = 'http://localhost:8086' if app.debug else 'http://feedback.' + version
        resp = requests.post(feedback_address, json=data_json)
        if resp.status_code != 200:
            log(method_name, error_message)
            return jsonify(error_message), 500
        res = resp.json()
        res['uuid_str'] = uuid_str
        return jsonify(res)
    except requests.exceptions.ConnectionError as e:
        message = 'Error while doing prediction: ' + 'Cannot send POST request to webservice feedback. '
        message += str(e) + ' Is the webservice running?'
        log_error_message = {'message': message, 'uuid_str': uuid_str}
        log(method_name, log_error_message)
        return jsonify(error_message), 500
    except:
        log(method_name, {'traceback': traceback.format_exc()})
        return 'Error', 500


@app.route("/github_webhook", methods=['POST'])
def github_webhook():
    try:
        resp = requests.post(EVENT_LISTENER_TEKTON_ADDRESS, json=request.json)
        if resp.status_code != 200:
            raise Exception()
        return jsonify({'result': 'ok'})
    except:
        app.logger.error(traceback.format_exc())
        return 'Error', 500


@app.route("/get_logs", methods=['POST'])
@secured_with_token()
@with_request_params(r, model_type, ["uuid_requested"])
def get_logs(uuid_requested, uuid_str, version):
    method_name = 'get_logs'
    error_message = {'message': 'Error while getting logs', 'uuid_str': uuid_str}
    try:
        minute = r.get('request-timestamp-' + uuid_requested)
        if not minute:
            return jsonify({'error': 'log uuid cannot be found'}), 400
        minute = minute.decode()
        resp = requests.post(GET_LOGS_KNATIVE_MONITORING_ADDRESS, json={
            'uuid_requested': uuid_requested,
            'minute': minute,
            'uuid_str': uuid_str
        })
        if resp.status_code != 200:
            log(method_name, error_message)
            return jsonify(error_message), 500
        res = resp.json()
        res['uuid_str'] = uuid_str
        return jsonify(res)
    except requests.exceptions.ConnectionError as e:
        message = 'Error while getting logs: ' + 'Cannot send POST request to webservice feedback. '
        message += str(e) + ' Is the webservice running?'
        log_error_message = {'message': message, 'uuid_str': uuid_str}
        log(method_name, log_error_message)
        return jsonify(error_message), 500
    except:
        log(method_name, {'traceback': traceback.format_exc()})
        return 'Error', 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8081)))
