from springapi.app import create_app
import unittest


class TestAppCration(unittest.TestCase):

    def test_create_springapi_app_in_testing(self):
        app = create_app('TestingConfig')
        app_env = app.config
        self.assertEqual(app_env['TESTING'], True)
