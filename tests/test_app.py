import unittest

from flask import Flask
from springapi.app import (
    create_submission_database_instance, create_user_database_instance,
    create_token_database_instance)
from springapi.config_helpers import AUTH, TOKEN
from tests.helpers import make_test_springapi_app
from unittest import mock


class TestSpringapiAppCreation(unittest.TestCase):

    def test_springapi_debug_true_in_development(self):
        env_vars = {"FLASK_ENV": "development"}
        app = make_test_springapi_app("google", env_vars)
        app_env = app.config

        self.assertEqual(app_env['ENV'], 'development')
        self.assertEqual(app_env['DEBUG'], True)

    def test_springapi_defaults_to_env_testing_debug_false(self):
        app = make_test_springapi_app("google")
        app_env = app.config

        self.assertEqual(app_env['ENV'], 'testing')
        self.assertEqual(app_env['DEBUG'], False)

    def test_springapi_raises_AssertionError_if_required_env_var_missing(
            self):
        with self.assertRaises(AssertionError) as context:
            make_test_springapi_app("google", remove=[AUTH])

        self.assertIsInstance(context.exception, AssertionError)

    def test_springapi_raises_ValueError_scheme_not_found(self):
        scheme = "badscheme"
        with self.assertRaises(ValueError) as context:
            make_test_springapi_app(scheme)

        self.assertEqual(str(context.exception),
                         f"Unknown authorization protocol: {scheme}")


class TestSubmissionDatabaseCreation(unittest.TestCase):

    def test_create_submission_database_instance_raises_ValueError(self):
        scheme = 'badscheme'
        config = {'DATABASE_URI': f'{scheme}://ImFiY2RlIg=='}

        with self.assertRaises(ValueError) as context:
            create_submission_database_instance(config)

        self.assertEqual(str(context.exception),
                         f'Unknown database protocol: {scheme}')

    @mock.patch('springapi.app.authenticate_firebase')
    def test_create_submission_database_instance_auth_if_scheme_found(
            self, mocked):
        auth = mocked.return_value = 'abc'

        scheme = 'firestore'
        config = {'DATABASE_URI': f'{scheme}://ImFiY2RlIg=='}

        response = create_submission_database_instance(config)
        self.assertEqual(response, auth)
        mocked.assert_called_with(f'{scheme}://ImFiY2RlIg==')


@mock.patch('springapi.app.authenticate_firebase')
@mock.patch('springapi.app.admin.get_app')
class TestUserDatabaseCreation(unittest.TestCase):

    def test_create_user_database_instance_auth_if_scheme_found(
            self, mock_app, mock_auth):
        mock_app.return_value = False
        expected = mock_auth.return_value = 'abc'

        scheme = 'firebase'
        config = {'USERS': f'{scheme}://ImFiY2RlIg=='}

        response = create_user_database_instance(config)
        self.assertEqual(response, expected)
        mock_auth.assert_called_with(f'{scheme}://ImFiY2RlIg==')

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
            self, mock_app, mock_auth):
        scheme = 'badscheme'
        config = {'USERS': f'{scheme}://ImFiY2RlIg=='}

        with self.assertRaises(ValueError) as context:
            create_user_database_instance(config)

        self.assertEqual(str(context.exception),
                         f'Unknown user database protocol: {scheme}')


class TestTokenDatabaseCreation(unittest.TestCase):

    @mock.patch('springapi.app.db.init_app')
    def test_create_token_database_instance_calls_init_app(self, mock_db):
        app = Flask(__name__)
        config = {TOKEN: "sqlite"}
        create_token_database_instance(config, app)
        mock_db.assert_called_with(app)

    def test_create_token_database_instance_ValueError_on_bad_scheme(self):
        scheme = "bad_scheme"
        config = {TOKEN: scheme}
        with self.assertRaises(ValueError) as context:
            create_token_database_instance(config, "app")
        self.assertEqual(
            str(context.exception),
            f"Unknown token database protocol: {scheme}")
