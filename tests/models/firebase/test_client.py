import unittest
from mockfirestore import MockFirestore
from springapi.exceptions import (
    CollectionNotFound, EntryAlreadyExists, EntryNotFound, ValidationError)
from springapi.models.firebase.client import (
    get_collection, get_entry, add_entry, update_entry, get_firebase_users)
from tests.helpers import populate_mock_submissions
from unittest import mock


@mock.patch('springapi.models.firebase.client.firestore.client')
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
        self.assertEqual(response['1'], self.entries['1'])

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


@mock.patch('springapi.models.firebase.client.auth.list_users')
class TestFirebaseCalls(unittest.TestCase):

    def test_get_firebase_users_returns_list_of_users(self, mock_get):
        mock_get.return_value = MockFirebaseUserList(3)
        expected = ['foo0@example.com', 'foo1@example.com', 'foo2@example.com']
        user_list = get_firebase_users()
        self.assertEqual(user_list, expected)

    def test_get_firebase_users_returns_empty_list(self, mock_get):
        mock_get.return_value = MockFirebaseUserList(0)
        expected = []
        user_list = get_firebase_users()
        self.assertEqual(user_list, expected)
