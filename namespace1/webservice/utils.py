import requests


class MyHandler:

    def __init__(self, text, uuid_str):
        self.text = text
        self.uuid_str = uuid_str

    def handle(self):
        notify_broker(self.text, self.uuid_str)
        return {'handled': 'true'}


def notify_broker(text, uuid_str):
    data = {'text': text, 'uuid_str': uuid_str}
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
