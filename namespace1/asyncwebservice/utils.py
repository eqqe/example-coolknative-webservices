from pathlib import Path
from minio.error import BucketAlreadyOwnedByYou, BucketAlreadyExists, ResponseError

from utils_webservices.definitions import BUCKET_NAME
from utils_webservices.flask_utils import BaseJob


class MyJob(BaseJob):
    def __init__(self, uuid_str, req_json, mc):
        super().__init__(uuid_str)
        self.data = req_json['data']
        self.mc = mc

    def run(self):
        try:
            self.mc.make_bucket(BUCKET_NAME)
        except BucketAlreadyOwnedByYou:
            pass
        except BucketAlreadyExists:
            pass
        except ResponseError:
            raise
        object_name = 'my_test_object_' + self.uuid_str + ".txt"
        my_file = Path(object_name)
        my_file.open(mode='w').write(self.data)
        self.mc.fput_object(BUCKET_NAME, object_name, my_file, content_type="text/plain")
        my_file.unlink()
