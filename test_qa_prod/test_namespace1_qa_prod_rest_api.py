import os
import unittest

from test_dev.helper_test_dev_rest_api import HelperTestDevRestApi


class TestQaProdRestApi(unittest.TestCase):
    helper_test_dev_rest_api = HelperTestDevRestApi({
        'token': os.environ.get('TOKEN_WEBSERVICE_1'),
        'version': 'namespace1'},
        'here we go')

    def test_webservice(self):
        self.helper_test_dev_rest_api.test_webservice()

    def test_webservice_then_read(self):
        self.helper_test_dev_rest_api.test_webservice_then_read()