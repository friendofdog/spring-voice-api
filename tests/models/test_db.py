import unittest
from mockfirestore import MockFirestore  # type: ignore
from springapi.models.db import Submission, get_submission, get_submissions
from tests.helpers import populate_mock_submissions
from unittest import mock


class TestDataValidation(unittest.TestCase):

    def test_check_required_fields_returns_missing_fields(self):
        submission = Submission()

        data = {'name': 'This Person', 'message': 'hello'}
        missing = submission._check_required_fields(data)
        self.assertEqual(missing, ['location'])

    def test_check_required_fields_returns_empty_if_no_missing(self):
        submission = Submission()

        data = {'name': 'This Person', 'message': 'hello', 'location': 'here'}
        missing = submission._check_required_fields(data)
        self.assertFalse(missing)

    def test_check_type_returns_bad_types(self):
        submission = Submission()

        data = {'name': 10, 'message': 'hello'}
        bad_types = submission._check_type(data)
        self.assertEqual(bad_types, ['name'])

    def test_check_type_returns_empty_if_types_good(self):
        submission = Submission()

        data = {'name': 'This Person', 'message': 'hello'}
        bad_types = submission._check_type(data)
        self.assertEqual(bad_types, [])

    @mock.patch('springapi.models.db.Submission._check_type')
    @mock.patch('springapi.models.db.Submission._check_required_fields')
    def test_validate_data_returns_missing_field_error_message(
            self, mock_type, mock_req):
        mock_type.return_value = ['some_field', 'another_field']
        mock_req.return_value = []

        submission = Submission()

        data = {'name': 'This Person'}
        response = submission._validate_data(data)
        self.assertEqual(response[0], 'Missing: some_field, another_field')

    @mock.patch('springapi.models.db.Submission._check_type')
    @mock.patch('springapi.models.db.Submission._check_required_fields')
    def test_validate_data_returns_type_check_error_message(
            self, mock_type, mock_req):
        mock_type.return_value = []
        mock_req.return_value = ['name']

        submission = Submission()

        data = {'name': 10, 'message': 'hello'}
        response = submission._validate_data(data)
        self.assertEqual(
            response[0], 'Fields with type errors: name is int, should be str.'
        )


@mock.patch('springapi.models.firebase.client.firestore.client')
class TestDatabaseCalls(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatabaseCalls, self).__init__(*args, **kwargs)
        self.entries = {
            "1": {"name": "Some Guy", "message": "Hi there"},
            "2": {"name": "Another Fellow", "message": "Goodbye"}
        }

    def test_get_submissions_returns_empty_if_none_found(self, mock_client):
        mock_client.return_value = MockFirestore()

        response = get_submissions()
        self.assertFalse(response)

    def test_get_submissions_returns_list_if_found(self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)

        response = get_submissions()
        self.assertEqual(response, self.entries)

    def test_get_submission_returns_404_if_not_found(self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)

        entry_id = 'missing-entry'
        not_found = f'Entry with id {entry_id} not found in submissions'

        response, status = get_submission(entry_id)
        self.assertEqual(status, '404 NOT FOUND')
        self.assertEqual(response, not_found)

    def test_get_submission_returns_submission_if_found(self, mock_client):
        mock_client.return_value = populate_mock_submissions(self.entries)

        response, status = get_submission('1')
        self.assertEqual(status, '200 OK')
        self.assertEqual(response, self.entries['1'])

    @mock.patch('springapi.models.db.Submission._validate_data')
    def test_create_submission_fails_if_validation_checks_fail(
            self, mock_validation, __):
        error = mock_validation.return_value = ['some error occured']

        submission = Submission()

        response, status = submission.create_submission({})
        self.assertEqual(response, error[0])
        self.assertEqual(status, '400 BAD REQUEST')

    @mock.patch('springapi.models.db.Submission._validate_data')
    def test_create_submission_succeeds_if_validation_checks_pass(
            self, mock_validation, __):
        mock_validation.return_value = []

        submission = Submission()

        data = {'name': 'This Person'}
        response, status = submission.create_submission(data)
        self.assertEqual(response, data)
        self.assertEqual(status, '201 CREATED')

    @mock.patch('springapi.models.firebase.client.add_entry')
    @mock.patch('springapi.models.db.Submission._validate_data')
    def test_create_submission_returns_server_error_message(
            self, mock_validation, mock_add, __):
        mock_validation.return_value = []
        error = mock_add.return_value = ['some error happened', '500']

        submission = Submission()

        response, status = submission.create_submission({})
        self.assertEqual('An error occured:\r\n'
                         f'{error[0]}', response)
        self.assertEqual(status, error[1])
