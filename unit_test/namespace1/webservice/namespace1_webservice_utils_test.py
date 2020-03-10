import unittest

from namespace1.webservice.utils import MyJob


class TestMyHandler(unittest.TestCase):
    def test_init(self):
        my_handler = MyJob("uuid_str", {"data": "text"})
        self.assertEqual(my_handler.data, "text")
