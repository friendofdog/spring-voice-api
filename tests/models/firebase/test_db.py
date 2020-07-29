import unittest
from mockfirestore import MockFirestore
from unittest import mock
from springapi.models.firebase.db import get_collection


class TestFirebaseCalls(unittest.TestCase):

    @mock.patch('springapi.models.firebase.db.firestore.client')
    def test_get_collection_returns_empty_if_none_found(self, mocked):
        mock_db = MockFirestore()
        mocked.return_value = mock_db

        response = get_collection('submissions')
        self.assertEqual(response, {})

    @mock.patch('springapi.models.firebase.db.firestore.client')
    def test_get_collection_contains_expected_entry(self, mocked):
        entry_data = {"name": "qwerty", "message": "Hi there"}
        entry_id = '1'
        collection = 'submissions'

        mock_db = MockFirestore()
        mock_db.collection(collection).add(entry_data, entry_id)
        mocked.return_value = mock_db

        response = get_collection(collection)
        self.assertEqual(response[entry_id], entry_data)
