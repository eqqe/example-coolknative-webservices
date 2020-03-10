import requests
from utils_webservices.flask_utils import BaseJob


class MyJob(BaseJob):

    def __init__(self, uuid_str, req_json):
        super().__init__(uuid_str)
        self.data = req_json['data']

    def run(self):
        notify_broker(self.data, self.uuid_str)
        return {'handled': 'true'}


def notify_broker(data, uuid_str):
    data = {'data': data, 'uuid_str': uuid_str}
    headers = {
        'Content-type': 'application/json',
        'Ce-Id': 'say-hello',
        'Ce-Specversion': '0.3',
        'Ce-Type': 'async',
        'Ce-Source': 'not-sendoff'
    }
    resp = requests.post("http://default-broker.namespace1", json=data, headers=headers)
    if not resp.ok:
        raise Exception()
