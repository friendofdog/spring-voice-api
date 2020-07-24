import os
from springapi.app import create_app
import unittest
from unittest import mock


class TestAppCration(unittest.TestCase):

    def test_springapi_starts_in_testing(self):
        app = create_app()
        app_env = app.config
        self.assertEqual(app_env['ENV'], 'testing')

    @mock.patch.dict(os.environ, {'FLASK_ENV': 'development'})
    def test_springapi_dev_env_enables_debug(self):
        app = create_app()
        app_env = app.config
        self.assertEqual(app_env['ENV'], 'development')
        self.assertEqual(app_env['DEBUG'], True)
