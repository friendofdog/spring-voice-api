import unittest
from mockfirestore import MockFirestore  # type: ignore
from springapi.models.db import \
    check_required_fields,\
    check_type,\
    get_submissions,\
    get_submission,\
    create_submission
from tests.helpers import populate_mock_firestore_submissions
from unittest import mock


class TestDatabaseValidationCalls(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatabaseValidationCalls, self).__init__(*args, **kwargs)
        self.fields = {
            'name': {'isRequired': True, 'type': str},
            'message': {'isRequired': True, 'type': str},
            'age': {'isRequired': False, 'type': int},
            'location': {'isRequired': False, 'type': str}
        }

    def test_check_required_fields_returns_missing_fields(self):
        data = {'name': 'This Person', 'age': 33}
        missing = check_required_fields(self.fields, data)
        self.assertEqual(missing, ['message'])

    def test_check_required_fields_returns_empty_if_no_missing(self):
        data = {'name': 'This Person', 'message': 'hello', 'age': 33}
        missing = check_required_fields(self.fields, data)
        self.assertFalse(missing)

    def test_check_type_returns_bad_types(self):
        data = {'name': 10, 'message': 'hello'}
        bad_types = check_type(self.fields, data)
        self.assertEqual(bad_types, ['name'])

    def test_check_type_returns_empty_if_types_good(self):
        data = {'name': 'This Person', 'message': 'hello'}
        bad_types = check_type(self.fields, data)
        self.assertEqual(bad_types, [])


class TestDatabaseCalls(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatabaseCalls, self).__init__(*args, **kwargs)
        self.entries = {
            "1": {"name": "Some Guy", "message": "Hi there"},
            "2": {"name": "Another Fellow", "message": "Goodbye"}
        }

    @mock.patch('springapi.models.firebase.client.firestore.client')
    def test_get_submissions_returns_empty_if_none_found(self, mocked):
        mocked.return_value = MockFirestore()

        response = get_submissions()
        self.assertFalse(response)

    @mock.patch('springapi.models.firebase.client.firestore.client')
    def test_get_submissions_returns_list_if_found(self, mocked):
        mocked.return_value = populate_mock_firestore_submissions(self.entries)

        response = get_submissions()
        self.assertEqual(response, self.entries)

    @mock.patch('springapi.models.firebase.client.firestore.client')
    def test_get_submission_returns_404_if_not_found(self, mocked):
        mocked.return_value = populate_mock_firestore_submissions(self.entries)

        entry_id = 'missing-entry'
        not_found = f'Entry with id {entry_id} not found in submissions'

        response, status = get_submission(entry_id)
        self.assertEqual(status, '404 NOT FOUND')
        self.assertEqual(response, not_found)

    @mock.patch('springapi.models.firebase.client.firestore.client')
    def test_get_submission_returns_submission_if_found(self, mocked):
        mocked.return_value = populate_mock_firestore_submissions(self.entries)

        response, status = get_submission('1')
        self.assertEqual(status, '200 OK')
        self.assertEqual(response, self.entries['1'])

    @mock.patch('springapi.models.db.check_type')
    @mock.patch('springapi.models.db.check_required_fields')
    def test_create_submission_returns_missing_field_error(
            self, mock_type, mock_req):
        mock_type.return_value = ['some_field', 'another_field']
        mock_req.return_value = []

        data = {'name': 'This Person'}
        response, status = create_submission(data)
        self.assertEqual(response, 'Missing: some_field, another_field')
        self.assertEqual(status, '400 BAD REQUEST')

    @mock.patch('springapi.models.db.check_type')
    @mock.patch('springapi.models.db.check_required_fields')
    def test_create_submission_returns_type_check_error(
            self, mock_req, mock_type):
        mock_type.return_value = ['name']
        mock_req.return_value = []

        data = {'name': 10, 'message': 'hello'}
        response, status = create_submission(data)
        self.assertEqual(response, f'Fields with type errors: name is int '
                                   f'should be str')
        self.assertEqual(status, '400 BAD REQUEST')

    @mock.patch('springapi.models.db.check_type')
    @mock.patch('springapi.models.db.check_required_fields')
    @mock.patch('springapi.models.firebase.client.firestore.client')
    def test_create_submission_succeeds_if_checks_passed(
            self, mock_client, mock_req, mock_type):
        mock_type.return_value = []
        mock_req.return_value = []
        mock_client.return_value = MockFirestore()

        data = {'name': 'This Person'}
        response, status = create_submission(data)
        self.assertEqual(response, data)
        self.assertEqual(status, '201 CREATED')
