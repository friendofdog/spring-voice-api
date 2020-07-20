from run import get_env_name
import unittest
from unittest.mock import patch
import sys


class TestEnvironmentConfiguration(unittest.TestCase):

    @patch('sys.argv', [sys.argv[0], '--env=test'])
    def test_environment_is_testingconfig(self):
        env_name = get_env_name()
        self.assertEqual(env_name, 'TestingConfig')

    @patch('sys.argv', [sys.argv[0], '--abc=def'])
    def test_ignore_bad_arg_use_default(self):
        env_name = get_env_name()
        self.assertEqual(env_name, 'ProductionConfig')
