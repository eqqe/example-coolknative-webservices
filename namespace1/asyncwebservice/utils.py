import uuid
from minio.error import BucketAlreadyOwnedByYou, BucketAlreadyExists, ResponseError


class MyJob:
    def __init__(self, mc, text):
        self.minio_utils = mc
        self.text = text
        self.bucket_name = "test"

    def run(self):
        try:
            self.mc.make_bucket(self.bucket_name)
        except BucketAlreadyOwnedByYou:
            pass
        except BucketAlreadyExists:
            pass
        except ResponseError:
            raise
        object_name = 'my_test_object' + str(uuid.uuid4()) + ".txt"
        self.mc.put_object(self.bucket_name, object_name, self.text, len(self.text), content_type="text/plain")
