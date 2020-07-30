import unittest
from tests.helpers import populate_mock_firestore_submissions
from mockfirestore import MockFirestore
from springapi.models.firebase.db import get_collection, add_entry
from unittest import mock


class TestFirebaseCalls(unittest.TestCase):

    @mock.patch('springapi.models.firebase.db.firestore.client')
    def test_get_collection_returns_empty_if_collection_notfound(self, mocked):
        mocked.return_value = populate_mock_firestore_submissions()

        response = get_collection('nonexistent')
        self.assertFalse(response)

    @mock.patch('springapi.models.firebase.db.firestore.client')
    def test_get_collection_returns_entries_if_collection_exists(self, mocked):
        mocked.return_value = populate_mock_firestore_submissions()

        response = get_collection('submissions')
        self.assertTrue(response)

    @mock.patch('springapi.models.firebase.db.firestore.client')
    def test_add_entry_creates_entry_in_db(self, mocked):
        entry_data = {"name": "This Person", "message": "Ohayo"}
        mocked.return_value = MockFirestore()

        response, status = add_entry('submissions', entry_data)
        self.assertEqual(response, entry_data)
        self.assertEqual(status, "201 CREATED")
