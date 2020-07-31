import unittest
from tests.helpers import populate_mock_firestore_submissions
from mockfirestore import MockFirestore
from springapi.models.firebase.client \
    import get_collection, get_entry, add_entry, update_entry
from unittest import mock


class TestFirebaseCalls(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFirebaseCalls, self).__init__(*args, **kwargs)
        self.entries = {
            "1": {"name": "Some Guy", "message": "Hi there"},
            "2": {"name": "Another Fellow", "message": "Goodbye"}
        }

    @mock.patch('springapi.models.firebase.client.firestore.client')
    def test_get_collection_returns_empty_if_collection_notfound(self, mocked):
        mocked.return_value = populate_mock_firestore_submissions(self.entries)

        response = get_collection('nonexistent')
        self.assertFalse(response)

    @mock.patch('springapi.models.firebase.client.firestore.client')
    def test_get_collection_returns_entries_if_collection_exists(self, mocked):
        mocked.return_value = populate_mock_firestore_submissions(self.entries)

        response = get_collection('submissions')
        self.assertTrue(response)
        self.assertEqual(response['1'], self.entries['1'])

    @mock.patch('springapi.models.firebase.client.firestore.client')
    def test_get_entry_returns_empty_if_notfound(self, mocked):
        mocked.return_value = populate_mock_firestore_submissions(self.entries)

        response = get_entry('submissions', 'nonexistent')
        self.assertFalse(response)

    @mock.patch('springapi.models.firebase.client.firestore.client')
    def test_get_entry_returns_expected_entry_if_found(self, mocked):
        mocked.return_value = populate_mock_firestore_submissions(self.entries)

        response = get_entry('submissions', '1')
        self.assertEqual(response, self.entries['1'])

    @mock.patch('springapi.models.firebase.client.firestore.client')
    def test_add_entry_creates_entry_in_db(self, mocked):
        data = {"name": "This Person", "message": "Ohayo"}
        mocked.return_value = MockFirestore()

        response, status = add_entry('submissions', data)
        self.assertEqual(response, data)
        self.assertEqual(status, "201 CREATED")

    @mock.patch('springapi.models.firebase.client.firestore.client')
    def test_add_entry_fails_if_document_exists(self, mocked):
        mocked.return_value = populate_mock_firestore_submissions(self.entries)

        response, status = add_entry('submissions', {}, '1')
        self.assertIn('409 Document already exists', response)
        self.assertEqual(status, "409 Conflict")

    @mock.patch('springapi.models.firebase.client.firestore.client')
    def test_update_entry_returns_updated_entry_data(self, mocked):
        entry_id = '1'
        data = {"message": "Ohayo"}
        mocked.return_value = populate_mock_firestore_submissions(self.entries)

        response, status = update_entry('submissions', data, entry_id)
        self.assertEqual(response, f'{entry_id} updated')
        self.assertEqual(status, "200 OK")

    @mock.patch('springapi.models.firebase.client.firestore.client')
    def test_update_entry_creates_entry_if_notfound(self, mocked):
        entry_id = 'doesnotexist'
        data = {"message": "Ohayo"}
        mocked.return_value = populate_mock_firestore_submissions(self.entries)

        response, status = update_entry('submissions', data, entry_id)
        self.assertIn('404 No document to update', response)
        self.assertEqual(status, "404 NOT FOUND")
