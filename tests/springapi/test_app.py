from springapi.app import get_env_name, create_app
import unittest
from unittest.mock import patch
import sys


class TestAppConfig(unittest.TestCase):

    @patch('sys.argv', [sys.argv[0], '--env=test'])
    def test_config_attr_testing_true(self):
        app = create_app()
        app_env = app.config
        self.assertEqual(app_env['TESTING'], True)

    @patch('sys.argv', [sys.argv[0], '--env=test'])
    def test_development_environment(self):
        env_name = get_env_name()
        self.assertEqual(env_name, 'TestingConfig')
