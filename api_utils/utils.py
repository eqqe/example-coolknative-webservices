import copy
import datetime
import json
import os
import uuid
from flask import request, Response
import logging
import traceback
from definitions import MINIO_BUCKET_LOGS_EXPIRATION_DAYS
from lib_logs.logger_fluent_flask import log


def get_version():
    version = request.headers.get('version')
    return version if version else 'legacy'


def with_request_params(r, model_type, mandatory=[], optional=[]):
    def get_request_param(key):
        try:
            return request.json[key]
        except KeyError:
            return None

    def call_with_params(f):
        def wrapper():
            params = {}
            for key in mandatory:
                params[key] = get_request_param(key)
                if not params[key]:
                    return ErrorSecuredWithToken('Missing expected parameter {}'.format(key)).response()
            for key in optional:
                params[key] = get_request_param(key)
            if 'client_id' in params:
                client_id = params['client_id']
                if len(client_id) > 53:
                    message = 'Error: client_id parameter is too long: ' + str(len(client_id))
                    message += ' is more than 53 characters'
                    return ErrorSecuredWithToken(message).response()
                params['client_id'] = client_id + '-' + get_version()
            uuid_str = str(uuid.uuid4())
            params['uuid_str'] = uuid_str
            expiration_seconds = MINIO_BUCKET_LOGS_EXPIRATION_DAYS * 24 * 60
            r.set('request-timestamp-' + uuid_str, str(datetime.datetime.utcnow()), expiration_seconds)
            params['version'] = get_version()
            params_logged = copy.deepcopy(params)
            if 'data' in params_logged:
                params_logged['len_data'] = len(params_logged['data'])
                del params_logged['data']
            params_logged['model_type'] = model_type
            log(f.__name__, params_logged)
            return f(**params)

        wrapper.__name__ = f.__name__
        return wrapper

    return call_with_params


def secured_with_token():
    try:
        expected_api_key = os.environ['token']
    except KeyError:
        expected_api_key = None
    api_key_header = 'Token'

    def get_token_from_request():
        return request.headers.get(api_key_header)

    def secured_call(f):
        def wrapper(*args, **kwargs):
            if expected_api_key is None or (get_token_from_request() == expected_api_key):
                try:
                    return f(*args, **kwargs)
                except Exception as ex:
                    message = 'Unhandled exception occurred : {}'.format(traceback.format_exc())
                    logging.error(message)
                    return ErrorSecuredWithToken(message).response()
            else:
                return ErrorSecuredWithToken('Could not validate credentials', http_status=403).response()

        wrapper.__name__ = f.__name__
        return wrapper

    return secured_call


class ErrorSecuredWithToken:
    def __init__(self, details, http_status=400):
        self._status = http_status
        self._details = details
        self._http_status = http_status

    def response(self):
        response = {
            'status': self._status,
            'details': self._details if self._details is not None else ''
        }
        return Response(json.dumps(response), status=self._http_status, mimetype='application/json')
