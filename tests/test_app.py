import unittest

from flask import Flask
from springapi.config_helpers import AUTH, TOKEN, create_database_instance
from springapi.helpers import encode_json_uri
from tests.helpers import make_test_client
from unittest import mock


class TestSpringapiAppCreation(unittest.TestCase):

    def test_springapi_debug_true_in_development(self):
        environ = {"FLASK_ENV": "development"}
        with make_test_client(environ=environ) as app:
            app_env = app.application.config

        self.assertEqual(app_env['ENV'], 'development')
        self.assertEqual(app_env['DEBUG'], True)

    def test_springapi_defaults_to_env_testing_debug_false(self):
        with make_test_client() as app:
            app_env = app.application.config

        self.assertEqual(app_env['ENV'], 'testing')
        self.assertEqual(app_env['DEBUG'], False)

    def test_springapi_raises_AssertionError_if_required_env_var_missing(self):
        with self.assertRaises(AssertionError) as context:
            with make_test_client(skip_defaults=True):
                self.assertIsInstance(context.exception, AssertionError)

    def test_springapi_raises_ValueError_scheme_not_found(self):
        scheme = "badscheme"
        environ = encode_json_uri(scheme, {})

        with self.assertRaises(ValueError) as context:
            with make_test_client({AUTH: environ}):
                self.assertIsInstance(context.exception, ValueError)
                self.assertEqual(str(context.exception),
                                 f"Unknown authorization protocol: {scheme}")


@mock.patch('springapi.config_helpers.authenticate_firebase')
@mock.patch('springapi.config_helpers.admin.get_app')
class TestDatabaseCreationFirebase(unittest.TestCase):

    def test_create_database_instance_with_firebase_authenticates(
            self, mock_app, mock_auth):
        mock_app.side_effect = ValueError
        scheme = 'firebase'
        config = {TOKEN: f'{scheme}://ImFiY2RlIg=='}

        create_database_instance(config, TOKEN)
        mock_auth.assert_called_with(f'{scheme}://ImFiY2RlIg==')

    def test_create_database_instance_with_firebase_returns_None(
            self, mock_app, mock_auth):
        mock_app.return_value = True
        scheme = 'firebase'
        config = {TOKEN: f'{scheme}://ImFiY2RlIg=='}

        response = create_database_instance(config, TOKEN)
        self.assertEqual(mock_auth.called, False)
        self.assertEqual(response, None)

    def test_create_database_instance_raises_ValueError_on_bad_scheme(
            self, mock_app, mock_auth):
        scheme = 'badscheme'
        config = {TOKEN: f'{scheme}://ImFiY2RlIg=='}

        with self.assertRaises(ValueError) as context:
            create_database_instance(config, TOKEN)

        self.assertEqual(
            str(context.exception), f'Unknown database protocol: {scheme}')


@mock.patch('springapi.config_helpers.db.init_app')
class TestDatabaseCreationSqlite(unittest.TestCase):

    def test_create_database_instance_with_sqlite_calls_init_app(
            self, mock_db):
        app = Flask(__name__)
        scheme = "sqlite"
        config = {TOKEN: f'{scheme}://ImFiY2RlIg=='}
        create_database_instance(config, TOKEN, app)
        mock_db.assert_called_with(app)
