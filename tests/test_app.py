from springapi.app import create_app
import unittest


class TestSpringapiAppCreation(unittest.TestCase):

    def test_springapi_defaults_to_testing(self):
        app = create_app({})
        app_env = app.config
        self.assertEqual(app_env['ENV'], 'testing')

    def test_springapi_dev_env_enables_debug(self):
        app = create_app({"FLASK_ENV": "development"})
        app_env = app.config
        self.assertEqual(app_env['ENV'], 'development')
        self.assertEqual(app_env['DEBUG'], True)
