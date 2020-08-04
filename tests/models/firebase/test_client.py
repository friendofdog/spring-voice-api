import unittest
from tests.helpers import populate_mock_submissions
from mockfirestore import MockFirestore
from springapi.models.firebase.client \
    import get_collection, get_entry, add_entry, update_entry
from unittest import mock


@mock.patch('springapi.models.firebase.client.firestore.client')
class TestFirebaseCalls(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFirebaseCalls, self).__init__(*args, **kwargs)
        self.entries = {
            "1": {"name": "Some Guy", "message": "Hi there"},
            "2": {"name": "Another Fellow", "message": "Goodbye"}
        }

    def test_get_collection_returns_empty_if_not_found(self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)

        response = get_collection('nonexistent')
        self.assertFalse(response)

    def test_get_collection_returns_collection_if_found(self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)

        response = get_collection('submissions')
        self.assertTrue(response)
        self.assertEqual(response['1'], self.entries['1'])

    def test_get_entry_returns_empty_if_not_found(self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)

        response = get_entry('submissions', 'nonexistent')
        self.assertFalse(response)

    def test_get_entry_returns_entry_if_found(self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)

        response = get_entry('submissions', '1')
        self.assertEqual(response, self.entries['1'])

    def test_add_entry_creates_entry_in_db(self, mock_client):
        data = {"name": "This Person", "message": "Ohayo"}
        mock_client.return_value = MockFirestore()

        response, status = add_entry('submissions', data)
        key = list(response.keys())[0]
        self.assertEqual(response[key], data)
        self.assertEqual(status, "201 CREATED")

    def test_add_entry_returns_409_if_entry_exists(self, mock_client):
        entry_id = '1'
        mock_client.return_value = populate_mock_submissions(self.entries)

        response, status = add_entry('submissions', {}, entry_id)
        self.assertEqual(f'{entry_id} already exists', response)
        self.assertEqual(status, "409 Conflict")

    def test_update_entry_returns_200_if_entry_updated(self, mock_client):
        entry_id = '1'
        data = {"message": "Ohayo"}
        mock_client.return_value = populate_mock_submissions(self.entries)

        response, status = update_entry('submissions', data, entry_id)
        self.assertEqual(response, f'{entry_id} updated')
        self.assertEqual(status, "200 OK")

    def test_update_entry_returns_404_if_entry_not_found(self, mock_client):
        entry_id = 'doesnotexist'
        data = {"message": "Ohayo"}
        mock_client.return_value = populate_mock_submissions(self.entries)

        response, status = update_entry('submissions', data, entry_id)
        self.assertEqual(f'{entry_id} not found', response)
        self.assertEqual(status, "404 NOT FOUND")
