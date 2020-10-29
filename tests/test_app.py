import unittest
from springapi.app import (
    create_app, create_database_instance, create_user_database_instance)
from springapi.helpers import TOKENS, AUTH, USERS
from tests.helpers import MOCK_TOKENS
from unittest import mock


class TestSpringapiAppCreation(unittest.TestCase):

    def test_springapi_defaults_to_testing(self):
        app = create_app({TOKENS: "TOKEN", AUTH: "abc", USERS: ["a"]})
        app_env = app.config
        self.assertEqual(app_env['ENV'], 'testing')

    def test_springapi_raises_AssertionError_if_valid_users_missing(self):
        with self.assertRaises(AssertionError):
            create_app({AUTH: "abc"})

    def test_springapi_raises_AssertionError_if_auth_missing(self):
        with self.assertRaises(AssertionError):
            create_app({TOKENS: "abc"})

    def test_springapi_dev_env_enables_debug(self):
        app = create_app({
            "FLASK_ENV": "development",
            TOKENS: MOCK_TOKENS, AUTH: "abc", USERS: ["A"]})
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

    @mock.patch('springapi.app.authenticate_firebase')
    def test_create_database_instance_auth_if_scheme_found(self, mocked):
        auth = mocked.return_value = 'abc'

        scheme = 'firestore'
        config = {'DATABASE_URI': f'{scheme}://ImFiY2RlIg=='}

        response = create_database_instance(config)
        self.assertEqual(response, auth)
        mocked.assert_called_with(f'{scheme}://ImFiY2RlIg==')

    @mock.patch('springapi.app.authenticate_firebase')
    @mock.patch('springapi.app.admin.get_app')
    def test_create_user_database_instance_auth_if_scheme_found(
            self, mock_app, mock_auth):
        mock_app.return_value = False
        expected = mock_auth.return_value = 'abc'

        scheme = 'firebase'
        config = {'USERS': f'{scheme}://ImFiY2RlIg=='}

        response = create_user_database_instance(config)
        self.assertEqual(response, expected)
        mock_auth.assert_called_with(f'{scheme}://ImFiY2RlIg==')

    @mock.patch('springapi.app.authenticate_firebase')
    @mock.patch('springapi.app.admin.get_app')
    def test_create_user_database_instance_returns_str_if_instantiated(
            self, mock_app, mock_auth):
        scheme = 'firebase'
        mock_app.return_value = True
        expected = mock_auth.return_value = \
            "Skipping user database instantiation. "\
            f"{scheme} database instance already created"

        config = {'USERS': f'{scheme}://ImFiY2RlIg=='}

        response = create_user_database_instance(config)
        self.assertEqual(response, expected)

    def test_create_user_database_instance_returns_ValueError_on_bad_scheme(
            self):
        scheme = 'badscheme'
        config = {'USERS': f'{scheme}://ImFiY2RlIg=='}

        with self.assertRaises(ValueError) as context:
            create_user_database_instance(config)

        self.assertEqual(str(context.exception),
                         f'Unknown user database protocol: {scheme}')
