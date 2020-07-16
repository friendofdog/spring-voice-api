from springapi.app import get_env_name
from tests.helpers import test_app_dev
import unittest


class TestAppConfig(unittest.TestCase):

    def test_config_attr_testing_true(self):
        app = test_app_dev()
        app_env = app.config
        self.assertEqual(app_env['TESTING'], True)

    def test_development_environment(self):
        env_name = get_env_name()
        self.assertEqual(env_name, 'TestingConfig')
