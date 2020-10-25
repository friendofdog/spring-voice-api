import unittest
from springapi.app import create_app, create_database_instance
from springapi.helpers import VALID_USERS, AUTH
from tests.helpers import MOCK_TOKENS
from unittest import mock


class TestSpringapiAppCreation(unittest.TestCase):

    def test_springapi_defaults_to_testing(self):
        app = create_app({VALID_USERS: "TOKEN", AUTH: "abc"})
        app_env = app.config
        self.assertEqual(app_env['ENV'], 'testing')

    def test_springapi_raises_AssertionError_if_valid_users_missing(self):
        with self.assertRaises(AssertionError):
            create_app({AUTH: "abc"})

    def test_springapi_raises_AssertionError_if_auth_missing(self):
        with self.assertRaises(AssertionError):
            create_app({VALID_USERS: "abc"})

    def test_springapi_dev_env_enables_debug(self):
        app = create_app({
            "FLASK_ENV": "development", VALID_USERS: MOCK_TOKENS, AUTH: "abc"})
        app_env = app.config
        self.assertEqual(app_env['ENV'], 'development')
        self.assertEqual(app_env['DEBUG'], True)

    def test_create_database_instance_returns_ValueError_on_bad_scheme(self):
        scheme = 'badscheme'
        config = {'DATABASE_URI': f'{scheme}://ImFiY2RlIg=='}

        with self.assertRaises(ValueError) as context:
            create_database_instance(config)

        self.assertEqual(str(context.exception),
                         f'Unknown database protocol: {scheme}')

    @mock.patch('springapi.app.authenticate_db')
    def test_create_database_instance_auth_if_scheme_found(self, mocked):
        auth = mocked.return_value = 'abc'

        scheme = 'firestore'
        config = {'DATABASE_URI': f'{scheme}://ImFiY2RlIg=='}

        response = create_database_instance(config)
        self.assertEqual(response, auth)
        mocked.assert_called_with(f'{scheme}://ImFiY2RlIg==')
