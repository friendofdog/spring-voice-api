import json
import unittest

from mockfirestore import MockFirestore
from springapi.helpers import encode_json_uri
from springapi.exceptions import (
    CollectionNotFound, EntryAlreadyExists, EntryNotFound, InvalidJSONURI,
    ValidationError)
from springapi.models.firebase.client import (
    add_entry, authenticate_firebase, get_collection, get_entry,
    get_email_addresses, update_entry, MissingProjectId)
from tests.helpers import populate_mock_submissions
from unittest import mock


@mock.patch('firebase_admin.firestore.client')
class TestFirestoreCalls(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFirestoreCalls, self).__init__(*args, **kwargs)
        self.entries = {
            "1": {"name": "Some Guy", "message": "Hi there"},
            "2": {"name": "Another Fellow", "message": "Goodbye"}
        }

    def test_get_collection_raises_CollectionNotFound(self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)
        collection = 'nonexistent'

        with self.assertRaises(CollectionNotFound) as context:
            get_collection(collection)

        self.assertEqual(
            context.exception.error_response_body(),
            CollectionNotFound(collection).error_response_body()
        )

    def test_get_collection_returns_collection_if_found(self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)

        response = get_collection('submissions')
        self.assertTrue(response)
        self.assertDictEqual(response, self.entries)

    def test_get_collection_returns_filtered_collection_given_field_value(
            self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)

        response = get_collection('submissions', 'message', 'Goodbye')
        self.assertTrue(response)
        self.assertNotIn("1", response.keys())
        self.assertDictEqual(response["2"], self.entries["2"])

    def test_get_collection_returns_whole_collection_given_single_arg(
            self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)

        response = get_collection('submissions', 'message')
        self.assertTrue(response)
        self.assertDictEqual(response, self.entries)

    def test_get_entry_raises_EntryNotFound(self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)
        collection = 'submissions'
        entry_id = 'abc'

        with self.assertRaises(EntryNotFound) as context:
            get_entry(collection, entry_id)

        self.assertEqual(
            context.exception.error_response_body(),
            EntryNotFound(entry_id, collection).error_response_body()
        )

    def test_get_entry_returns_entry_data_if_found(self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)

        response = get_entry('submissions', '1')
        self.assertEqual(response, self.entries['1'])

    def test_add_entry_returns_entry_data_if_successful(self, mock_client):
        mock_client.return_value = MockFirestore()

        entry_id = "abc123"
        data = {"name": "This Person", "message": "Ohayo", "id": entry_id}
        response = add_entry("submissions", data.copy())

        self.assertEqual(
            response, {entry_id: data})

    def test_add_entry_raises_ValidationError_if_id_missing(self, mock_client):
        data = {"name": "This Person", "message": "Ohayo"}
        mock_client.return_value = MockFirestore()

        with self.assertRaises(ValidationError) as err:
            add_entry("submissions", data)

        self.assertEqual(str(err.exception), "Entry ID missing")

    def test_add_entry_raises_EntryAlreadyExists(self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)

        entry_id = "1"
        data = {"name": "This Person", "message": "Ohayo", "id": entry_id}
        collection = "submissions"

        with self.assertRaises(EntryAlreadyExists) as context:
            add_entry(collection, data)

        self.assertEqual(
            context.exception.error_response_body(),
            EntryAlreadyExists(entry_id, collection).error_response_body()
        )

    def test_update_entry_returns_entry_data_if_successful(self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)
        entry_id = "1"
        data = {"message": "Ohayo"}

        response = update_entry('submissions', data, entry_id)
        self.assertEqual(
            response, {"success": f"{entry_id} updated in submissions"})

    def test_update_entry_raises_EntryNotFound(self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)
        collection = "submissions"
        entry_id = "abc"
        data = {"message": "Ohayo"}

        with self.assertRaises(EntryNotFound) as context:
            update_entry(collection, data, entry_id)

        self.assertEqual(
            context.exception.error_response_body(),
            EntryNotFound(entry_id, collection).error_response_body()
        )


class MockFirebaseUser:

    def __init__(self, i):
        self.email = f"foo{i}@example.com"


class MockFirebaseUserList:

    def __init__(self, i):
        self.users = self.create_users(i)

    def create_users(self, count):
        return [MockFirebaseUser(i) for i in range(count)]


@mock.patch('firebase_admin.auth.list_users')
class TestFirebaseCalls(unittest.TestCase):

    def test_get_email_addresses_returns_list_of_users(self, mock_get):
        mock_get.return_value = MockFirebaseUserList(3)
        expected = ['foo0@example.com', 'foo1@example.com', 'foo2@example.com']
        user_list = get_email_addresses()
        self.assertEqual(user_list, expected)

    def test_get_email_addresses_returns_empty_list(self, mock_get):
        mock_get.return_value = MockFirebaseUserList(0)
        expected = []
        user_list = get_email_addresses()
        self.assertEqual(user_list, expected)


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

    @mock.patch('firebase_admin.credentials.Certificate')
    @mock.patch('firebase_admin.initialize_app')
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
