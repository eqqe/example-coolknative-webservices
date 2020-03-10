import unittest
from namespace1.asyncwebservice.utils import MyJob


class TestMyJob(unittest.TestCase):
    def test_init(self):
        my_job = MyJob("uuid_str", {"data": "text"}, None)
        self.assertEqual(my_job.data, "text")
