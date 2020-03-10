import unittest

from namespace1.webservice.utils import MyHandler


class TestMyHandler(unittest.TestCase):
    def test_init(self):
        my_handler = MyHandler("text", "uuid_str")
        self.assertEqual(my_handler.text, "text")
