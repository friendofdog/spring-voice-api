import unittest
from springapi.models.exceptions import \
    CollectionNotFound, EntryNotFound, EntryAlreadyExists, ValidationError
from springapi.models.submission import Submission
from unittest import mock


@mock.patch('springapi.models.submission.Submission._check_type')
@mock.patch('springapi.models.submission.Submission._check_required_fields')
class TestDataValidation(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDataValidation, self).__init__(*args, **kwargs)
        self.submission = Submission()

    def test_validate_data_returns_missing_field_error_message(
            self, mock_type, mock_req):
        fields = mock_type.return_value = ['some_field', 'another_field']
        mock_req.return_value = []

        with self.assertRaises(ValidationError) as context:
            self.submission._validate_data({})

        self.assertEqual(
            context.exception.error_response_body(),
            {'error': f'Missing: {", ".join(fields)}'}
        )

    def test_validate_data_returns_type_check_error_message(
            self, mock_type, mock_req):
        data = {'name': 10, 'message': 'hello'}

        mock_type.return_value = []
        mock_req.return_value = ['name']

        with self.assertRaises(ValidationError) as context:
            self.submission._validate_data(data)

        self.assertEqual(
            context.exception.error_response_body(),
            {'error': 'name is int, should be str.'}
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
    def test_get_submissions_raises_CollectionNotFound(self, mock_get):
        mock_get.side_effect = CollectionNotFound('abc')

        with self.assertRaises(CollectionNotFound):
            self.submission.get_submissions()

    @mock.patch('springapi.models.firebase.client.get_collection')
    def test_get_submissions_returns_list_if_found(self, mock_get):
        mock_get.return_value = self.entries

        response = self.submission.get_submissions()
        self.assertEqual(response, self.entries)

    @mock.patch('springapi.models.firebase.client.get_entry')
    def test_get_submission_raises_EntryNotFound(self, mock_get):
        mock_get.side_effect = EntryNotFound('a', 'b')

        with self.assertRaises(EntryNotFound):
            self.submission.get_submission('abc')

    @mock.patch('springapi.models.firebase.client.get_entry')
    def test_get_submission_returns_submission_if_found(self, mock_get):
        entry_id = '1'
        mock_get.return_value = self.entries[entry_id]

        response = self.submission.get_submission(entry_id)
        self.assertEqual(response, self.entries[entry_id])

    @mock.patch('springapi.models.submission.Submission._validate_data')
    def test_create_submission_raises_ValidationError(
            self, mock_validation):
        error = 'invalid'
        mock_validation.return_value = [error]

        with self.assertRaises(ValidationError) as context:
            self.submission.create_submission({})

        self.assertEqual(
            context.exception.error_response_body(),
            ValidationError(error).error_response_body()
        )

    @mock.patch('springapi.models.firebase.client.add_entry')
    @mock.patch('springapi.models.submission.Submission._validate_data')
    def test_create_submission_raises_EntryAlreadyExists(
            self, mock_validation, mock_add):
        mock_validation.return_value = []
        mock_add.side_effect = EntryAlreadyExists('a', 'b')

        with self.assertRaises(EntryAlreadyExists):
            self.submission.create_submission({})

    @mock.patch('springapi.models.firebase.client.add_entry')
    @mock.patch('springapi.models.submission.Submission._validate_data')
    def test_create_submission_returns_submission_data_if_validation_passes(
            self, mock_validation, mock_add):
        data = {'abc': {'name': 'This Person'}}
        mock_validation.return_value = []
        mock_add.return_value = data

        response = self.submission.create_submission(data)
        self.assertEqual(response, data)

    @mock.patch('springapi.models.firebase.client.update_entry')
    @mock.patch('springapi.models.submission.Submission._validate_data')
    def test_update_submission_raises_EntryNotFound(
            self, mock_validation, mock_update):
        entry_id = 'abc'
        mock_validation.return_value = []
        mock_update.side_effect = EntryNotFound(entry_id, 'def')

        with self.assertRaises(EntryNotFound):
            self.submission.update_submission(entry_id, {})

    @mock.patch('springapi.models.submission.Submission._validate_data')
    def test_update_submission_raises_ValidationError(
            self, mock_validation):
        mock_validation.return_value = ['invalid']

        with self.assertRaises(ValidationError):
            self.submission.update_submission('abc', {})

    @mock.patch('springapi.models.firebase.client.update_entry')
    @mock.patch('springapi.models.submission.Submission._validate_data')
    def test_update_submission_returns_submission_data_if_found_and_valid(
            self, mock_validation, mock_update):
        entry_id = '1'
        data = {'name': 'New Name', 'message': 'new message'}
        update = mock_update.return_value = [f'Entry {entry_id} updated',
                                             '200 OK']
        mock_validation.return_value = []

        response, status = self.submission.update_submission(data, entry_id)
        self.assertEqual(response, update[0])
        self.assertEqual(status, update[1])
