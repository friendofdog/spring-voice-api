from models.firebase.app import authenticate
import os
import unittest
from unittest import mock


class MockGoogleAuthCredentials:

    def __init__(self):
        self.project_id = 'some-project-id'
        self.service_account_email = 'notvalid@iam.gserviceaccount.com'
        self.signer = 'not-a-valid-signer'


class TestFirebaseAppCreation(unittest.TestCase):

    @mock.patch.dict(os.environ, {
        'PROJECT_ID': 'some-project-id',
        'CREDENTIALS_FILE': 'missing'
    })
    def test_firebase_raises_error_when_missing_credentials_file(self):
        try:
            authenticate()
        except FileNotFoundError:
            self.assertRaises(FileNotFoundError)

    @mock.patch('models.firebase.app.auth.credentials.Certificate')
    def test_firebase_raises_error_when_bad_credentials(self, mocked):
        mocked.return_value = MockGoogleAuthCredentials
        try:
            authenticate()
        except ValueError:
            self.assertRaises(ValueError)
