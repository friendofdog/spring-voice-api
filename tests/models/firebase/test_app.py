import os
import unittest
from springapi.models.firebase.app import authenticate
from unittest import mock


class MockGoogleAuthCredentials:

    def __init__(self):
        self.project_id = 'some-project-id'
        self.service_account_email = 'notvalid@iam.gserviceaccount.com'
        self.signer = 'not-a-valid-signer'


class TestFirebaseAppCreation(unittest.TestCase):

    @mock.patch.dict(os.environ, {
        'CREDENTIALS_FILE': 'missing.json'
    })
    def test_firebase_FileNoteFoundError_when_missing_credentials_file(self):
        self.assertRaises(FileNotFoundError, authenticate)

    @mock.patch('springapi.models.firebase.app.auth.credentials.Certificate')
    def test_firebase_ValueError_when_bad_credentials(self, mocked):
        mocked.return_value = MockGoogleAuthCredentials
        self.assertRaises(ValueError, authenticate)
