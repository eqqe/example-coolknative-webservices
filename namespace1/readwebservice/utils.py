from utils_webservices.definitions import BUCKET_NAME
from utils_webservices.flask_utils import BaseJob


class MyJob(BaseJob):

    def __init__(self, uuid_str, req_json, mc):
        super().__init__(uuid_str)
        self.uuid_requested = req_json['uuid_requested']
        self.mc = mc

    def run(self):
        object_name = 'my_test_object_' + self.uuid_requested + ".txt"
        data = self.mc.get_object(BUCKET_NAME, object_name).read().decode()
        return {'data': data}
