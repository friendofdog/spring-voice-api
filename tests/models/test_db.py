import unittest
from unittest import mock
from tests.helpers import populate_mock_firestore_submissions
from springapi.models.db import get_submissions


class TestDatabaseCalls(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatabaseCalls, self).__init__(*args, **kwargs)
        self.entries = {
            "1": {"name": "Some Guy", "message": "Hi there"},
            "2": {"name": "Another Fellow", "message": "Goodbye"}
        }

    @mock.patch('springapi.models.firebase.client.firestore.client')
    def test_get_submissions_returns_empty_if_none_found(self, mocked):
        mocked.return_value = populate_mock_firestore_submissions(self.entries)

        response = get_submissions()
        self.assertEqual(response['1'], self.entries['1'])
