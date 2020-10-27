import json
import unittest
from unittest import mock

from springapi.config_helpers import encode_json_uri, InvalidJSONURI
from springapi.models.firebase.authenticate import (
    authenticate_firebase, MissingProjectId)


class MockGoogleAuthCredentials:

    @classmethod
    def from_path(cls, path):
        """
        The default Firebase Certificate constructor expects a path, so we're
        creating a method here that can be used in mocks to intercept the
        provided path and make assertions about what's being passed in

        :param path:
        :return:
        """
        with open(path, "rb") as fp:
            config = json.loads(fp.read())
        assert isinstance(config, dict)
        return cls()

    def __init__(self):
        self.project_id = 'some-project-id'
        self.service_account_email = 'notvalid@iam.gserviceaccount.com'
        self.signer = 'not-a-valid-signer'


class TestFirebaseAppCreation(unittest.TestCase):

    def test_authenticate_firebase_rejects_invalid_json_uri(self):
        self.assertRaises(
            InvalidJSONURI, lambda: authenticate_firebase("scheme://"))

    def test_firebase_ValueError_when_bad_credentials(self):
        config = {
            "type": "service_account",
            "project_id": "some-project-id",
            "token_uri": "foobar.com",
            "client_email": "admin@foobar.com",
            "private_key": "INVALID_KEY"
        }
        uri = encode_json_uri("firestore", config)

        with self.assertRaises(ValueError) as context:
            authenticate_firebase(uri)

        self.assertEqual(
            'Failed to initialize a certificate credential. Caused '
            'by: "No key could be detected."',
            str(context.exception))

    def test_firebase_ValueError_when_first_missing_field_is_type(self):
        config = {"project_id": "some-project-id"}
        uri = encode_json_uri("firestore", config)

        with self.assertRaises(ValueError) as context:
            authenticate_firebase(uri)

        self.assertEqual(
            'Invalid service account certificate. Certificate must contain a '
            '"type" field set to "service_account".',
            str(context.exception))

    def test_authenticate_firebase_raises_MissingProjectId_field_missing(self):
        config = {}
        uri = encode_json_uri("firestore", config)

        with self.assertRaises(MissingProjectId) as context:
            authenticate_firebase(uri)

        self.assertEqual('project_id missing', str(context.exception))

    @mock.patch(
        'springapi.models.firebase.authenticate.auth.credentials.Certificate')
    @mock.patch('springapi.models.firebase.authenticate.auth.initialize_app')
    def test_authenticate_firebase_returns_configured_firebase_instance(
            self, mocked_app, mocked_cert):
        mocked_cert.side_effect = MockGoogleAuthCredentials.from_path
        uri = encode_json_uri("firestore", {"project_id": "some-project-id"})
        authenticate_firebase(uri)

        mocked_app.assert_called_with(
            mock.ANY,
            {
                "projectId": "some-project-id",
                "storageBucket": "some-project-id.appspot.com"
            })
