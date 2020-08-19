import json
import unittest
from unittest import mock

from springapi.config_helpers import encode_json_uri, InvalidJSONURI
from springapi.models.firebase.app import authenticate


class MockGoogleAuthCredentials:

    @classmethod
    def from_path(cls, path):
        with open(path, "rb") as fp:
            config = json.loads(fp.read())
        assert isinstance(config, dict)
        return cls()

    def __init__(self):
        self.project_id = 'some-project-id'
        self.service_account_email = 'notvalid@iam.gserviceaccount.com'
        self.signer = 'not-a-valid-signer'


class TestFirebaseAppCreation(unittest.TestCase):

    def test_authenticate_rejects_invalid_json_uri(self):
        self.assertRaises(InvalidJSONURI, lambda: authenticate("scheme://"))

    def test_firebase_ValueError_when_bad_credentials(self):
        config = {
            "type": "service_account",
            "token_uri": "foobar.com",
            "client_email": "admin@foobar.com", "private_key": "INVALID KEY"
        }
        uri = encode_json_uri("firestore", config)

        with self.assertRaises(ValueError) as exc:
            authenticate(uri)

        self.assertEqual(
            'Failed to initialize a certificate credential. Caused '
            'by: "No key could be detected."',
            str(exc.exception))

    @mock.patch('springapi.models.firebase.app.auth.credentials.Certificate')
    @mock.patch('springapi.models.firebase.app.auth.initialize_app')
    def test_authenticate_returns_configured_firebase_instance(
            self, mocked_app, mocked_cert):
        mocked_cert.side_effect = MockGoogleAuthCredentials.from_path

        uri = encode_json_uri("firestore", {})

        authenticate(uri)

        mocked_app.assert_called_with(
            mock.ANY,
            {
                "projectId": "some-project-id",
                "storageBucket": "some-project-id.appspot.com"
            })
