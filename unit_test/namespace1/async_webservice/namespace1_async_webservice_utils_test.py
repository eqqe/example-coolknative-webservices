import unittest
from namespace1.asyncwebservice.utils import MyJob


class TestMyJob(unittest.TestCase):
    def test_init(self):
        my_job = MyJob(None, "text")
        self.assertEqual(my_job.text, "text")
