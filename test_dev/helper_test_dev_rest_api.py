import os
from time import sleep

import requests


def get_resp_body(resp):
    assert resp.ok
    resp_body = resp.json()
    return resp_body


class HelperTestDevRestApi:
    timeout = 10

    def __init__(self, headers, data):
        domain_template = os.environ.get('KNATIVE_SERVING_DOMAIN_TEMPLATE')
        domain_template = domain_template.replace('{{.Domain}}', os.environ.get('DOMAIN'))
        domain_template = domain_template.replace('{{.Namespace}}', os.environ.get('NAMESPACE'))
        domain_template = domain_template.replace('{{.Name}}', 'api')
        if os.environ.get('PUBLIC_IP') == 'localhost':
            self.base_url = 'http://kourier.kourier-system/'
            headers['Host'] = domain_template
        else:
            self.base_url = 'https://' + domain_template + '/'
        self.headers = headers
        self.data = data

    def test_webservice(self):
        payload = {'data': self.data}
        resp_body = self.get_resp(payload, 'webservice')
        assert resp_body['handled'] == 'true'

    def test_webservice_then_read(self):
        payload = {'data': self.data}
        resp_body = self.get_resp(payload, 'webservice')
        assert resp_body['handled'] == 'true'
        sleep(10)
        payload = {'uuid_requested': resp_body['uuid_str']}
        resp_body = self.get_resp(payload, 'readwebservice')
        assert resp_body['data'] == self.data

    def get_resp(self, payload, method):
        resp = requests.post(self.base_url + method, json=payload, headers=self.headers, timeout=self.timeout)
        resp_body = get_resp_body(resp)
        return resp_body
