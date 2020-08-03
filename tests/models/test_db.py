import unittest
from springapi.models.db import Submission, get_submission, get_submissions
from unittest import mock


class TestDataValidation(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDataValidation, self).__init__(*args, **kwargs)
        self.submission = Submission()

    def test_check_required_fields_returns_missing_fields(self):
        data = {'name': 'This Person', 'message': 'hello'}
        missing = self.submission._check_required_fields(data)
        self.assertEqual(missing, ['location'])

    def test_check_required_fields_returns_empty_if_no_missing(self):
        data = {'name': 'This Person', 'message': 'hello', 'location': 'here'}
        missing = self.submission._check_required_fields(data)
        self.assertFalse(missing)

    def test_check_type_returns_bad_types(self):
        data = {'name': 10, 'message': 'hello'}
        bad_types = self.submission._check_type(data)
        self.assertEqual(bad_types, ['name'])

    def test_check_type_returns_empty_if_types_good(self):
        data = {'name': 'This Person', 'message': 'hello'}
        bad_types = self.submission._check_type(data)
        self.assertEqual(bad_types, [])

    @mock.patch('springapi.models.db.Submission._check_type')
    @mock.patch('springapi.models.db.Submission._check_required_fields')
    def test_validate_data_returns_missing_field_error_message(
            self, mock_type, mock_req):
        fields = mock_type.return_value = ['some_field', 'another_field']
        mock_req.return_value = []

        response = self.submission._validate_data({})
        self.assertEqual(response[0], f'Missing: {", ".join(fields)}')

    @mock.patch('springapi.models.db.Submission._check_type')
    @mock.patch('springapi.models.db.Submission._check_required_fields')
    def test_validate_data_returns_type_check_error_message(
            self, mock_type, mock_req):
        data = {'name': 10, 'message': 'hello'}

        mock_type.return_value = []
        mock_req.return_value = ['name']

        response = self.submission._validate_data(data)
        self.assertEqual(
            response[0], 'Fields with type errors: name is int, should be str.'
        )


class TestDatabaseCalls(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatabaseCalls, self).__init__(*args, **kwargs)
        self.entries = {
            "1": {"name": "Some Guy", "message": "Hi there"},
            "2": {"name": "Another Fellow", "message": "Goodbye"}
        }
        self.submission = Submission()

    @mock.patch('springapi.models.firebase.client.get_collection')
    def test_get_submissions_returns_empty_if_none_found(self, mock_get):
        mock_get.return_value = []

        response = get_submissions()
        self.assertFalse(response)

    @mock.patch('springapi.models.firebase.client.get_collection')
    def test_get_submissions_returns_list_if_found(self, mock_get):
        mock_get.return_value = self.entries

        response = get_submissions()
        self.assertEqual(response, self.entries)

    @mock.patch('springapi.models.firebase.client.get_entry')
    def test_get_submission_returns_404_if_not_found(self, mock_get):
        entry_id = 'missing-entry'

        mock_get.return_value = {}

        response, status = get_submission(entry_id)
        self.assertEqual(status, '404 NOT FOUND')
        self.assertEqual(response, f'Entry with id {entry_id} '
                                   f'not found in submissions')

    @mock.patch('springapi.models.firebase.client.get_entry')
    def test_get_submission_returns_submission_if_found(self, mock_get):
        entry_id = '1'

        mock_get.return_value = self.entries[entry_id]

        response, status = get_submission(entry_id)
        self.assertEqual(status, '200 OK')
        self.assertEqual(response, self.entries[entry_id])

    @mock.patch('springapi.models.db.Submission._validate_data')
    def test_create_submission_fails_if_validation_checks_fail(
            self, mock_validation):
        error = mock_validation.return_value = ['some error occured']

        response, status = self.submission.create_submission({})
        self.assertEqual(response, error[0])
        self.assertEqual(status, '400 BAD REQUEST')

    @mock.patch('springapi.models.firebase.client.add_entry')
    @mock.patch('springapi.models.db.Submission._validate_data')
    def test_create_submission_returns_server_error_message(
            self, mock_validation, mock_add):
        mock_validation.return_value = []
        error = mock_add.return_value = ['some error happened', '500']

        response, status = self.submission.create_submission({})
        self.assertEqual('An error occured:\r\n'
                         f'{error[0]}', response)
        self.assertEqual(status, error[1])

    @mock.patch('springapi.models.firebase.client.add_entry')
    @mock.patch('springapi.models.db.Submission._validate_data')
    def test_create_submission_succeeds_if_validation_checks_pass(
            self, mock_validation, mock_add):
        data = {'name': 'This Person'}
        expected_status = '201 CREATED'

        mock_validation.return_value = []
        mock_add.return_value = [data, expected_status]

        response, status = self.submission.create_submission(data)
        self.assertEqual(response, data)
        self.assertEqual(status, expected_status)
