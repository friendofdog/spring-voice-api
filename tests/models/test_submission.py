from tests.helpers import SubmissionResponseAssertions
from springapi.models import exceptions
from springapi.models.submission import Submission
from unittest import mock


class TestSubmissionValidation(SubmissionResponseAssertions):

    def test_create_submission_sets_defaults_empty_fields(self):
        data = {'id': '1', 'name': 'a', 'message': 'b', 'location': 'c'}
        defaults = {
            'id': '1',
            'name': 'a',
            'message': 'b',
            'location': 'c',
            'allowSNS': False,
            'allowSharing': False,
            'isApproved': False
        }
        self.assert_missing_fields_get_default_values(data, defaults)

    def test_submission_from_json_rejects_invalid_data(self):
        with self.assertRaises(exceptions.ValidationError):
            Submission.from_json({
                "name": 5,
                "message": "b",
                "location": "c"
            })

    def test_submission_to_json_returns_expected_fields(self):
        submission = Submission.from_json({
            "id": "1",
            "name": "a",
            "message": "b",
            "location": "c"
        })
        self.assertEqual({
            "id": "1",
            "name": "a",
            "message": "b",
            "location": "c",
            "allowSNS": False,
            "allowSharing": False,
            "isApproved": False
        }, submission.to_json())


@mock.patch('springapi.models.firebase.client.get_collection')
class TestSubmissionGetAllSubmissions(SubmissionResponseAssertions):

    def test_get_submissions_returns_list_if_found(self, mock_get):
        mock_get.return_value = {
            "1": {
                "name": "a",
                "message": "b",
                "location": "c"
            }
        }
        results = Submission.get_submissions()
        self.assertEqual([{
            "id": "1",
            "name": "a",
            "message": "b",
            "location": "c",
            "allowSNS": False,
            "allowSharing": False,
            "isApproved": False
        }], [r.to_json() for r in results])
        mock_get.assert_called_with("submissions")

    def test_get_submissions_raises_CollectionNotFound(self, mock_get):
        mock_get.side_effect = exceptions.CollectionNotFound('submissions')
        self.assert_get_submissions_raises_not_found()

    def test_get_submissions_omits_invalid_entries(self, mock_get):
        mock_get.return_value = {
            "1": {
                "name": "a",
                "message": "b",
                "location": "c"
            },
            "2": {
                "name": "one",
                "message": "two",
                "location": "three",
                "bad_field": "invalid"
            },
            "3": {
                "name": "missing",
                "message": "location"
            }
        }
        results = Submission.get_submissions()
        self.assertEqual([{
            "id": "1",
            "name": "a",
            "message": "b",
            "location": "c",
            "allowSNS": False,
            "allowSharing": False,
            "isApproved": False
        }], [r.to_json() for r in results])


@mock.patch('springapi.models.firebase.client.get_entry')
class TestSubmissionGetSingleSubmission(SubmissionResponseAssertions):

    def test_get_submission_returns_submission_if_found(self, mock_get):
        entries = {
            'a': {
                "name": "a",
                "message": "a",
                "location": "a"
            },
            'b': {
                "name": "b",
                "message": "b",
                "location": "b"
            }
        }
        entry_id = 'a'
        mock_get.return_value = entries[entry_id]
        self.assert_get_single_submission_returns_single(
            Submission.from_json({
                "id": "a",
                "name": "a",
                "message": "a",
                "location": "a",
            }), entry_id)
        mock_get.assert_called_with("submissions", entry_id)

    def test_get_submission_raises_EntryNotFound(self, mock_get):
        entry_id = 'abc'
        mock_get.side_effect = exceptions.EntryNotFound(
            entry_id, 'submissions')
        self.assert_get_single_submission_raises_not_found(entry_id)


class TestSubmissionCreateSubmission(SubmissionResponseAssertions):

    @mock.patch('springapi.models.firebase.client.add_entry')
    def test_create_submission_returns_submission_if_valid(
            self, mock_add):
        entry_id = 'abc'
        data = {'id': entry_id, 'name': 'a', 'location': 'b', 'message': 'c'}
        mock_add.return_value = {entry_id: data}
        self.assert_create_submission_returns_success(entry_id, data)
        mock_add.assert_called_with("submissions", data)

    def test_create_submission_raises_ValidationError_disallowed(self):
        data = {'name': 'a', 'message': 'b', 'location': 'c', 'd': 'e'}
        self.assert_create_submission_raises_validation_error(data)

    def test_create_submission_raises_ValidationError_missing(self):
        data = {'name': 'a', 'message': 'b'}
        self.assert_create_submission_raises_validation_error(data)

    def test_create_submission_raises_ValidationError_type(self):
        data = {'name': 'a', 'message': 'b', 'location': 10}
        self.assert_create_submission_raises_validation_error(data)

    @mock.patch('springapi.models.firebase.client.add_entry')
    def test_create_submission_raises_EntryAlreadyExists(
            self, mock_add):
        entry_id = 'abc'
        data = {'name': 'a', 'location': 'b', 'message': 'c'}
        mock_add.side_effect = exceptions.EntryAlreadyExists(
            entry_id, 'submissions')
        self.assert_create_submission_raises_already_exists(entry_id, data)


class TestSubmissionUpdateSubmission(SubmissionResponseAssertions):

    @mock.patch('springapi.models.firebase.client.update_entry')
    def test_update_submission_returns_success_if_found_and_valid(
            self, mocked):
        entry_id = 'abc'
        data = {
            'id': entry_id,
            'name': 'a',
            'location': 'b',
            'message': 'new message'
        }
        expected = mocked.return_value = {'success': f'{entry_id} updated'}
        self.assert_update_submission_returns_success(entry_id, data, expected)
        mocked.assert_called_with("submissions", data, entry_id)

    @mock.patch('springapi.models.firebase.client.update_entry')
    def test_update_submission_raises_EntryNotFound(
            self, mock_update):
        entry_id = 'abc'
        data = {
            'id': entry_id,
            'name': 'a',
            'location': 'b',
            'message': 'new message'
        }
        mock_update.side_effect = exceptions.EntryNotFound(entry_id, 'def')
        self.assert_update_submission_raises_not_found(entry_id, data)

    def test_update_submission_raises_ValidationError(self):
        entry_id = 'abc'
        data = {'id': entry_id, 'name': 'a', 'message': 'new message'}
        self.assert_update_submission_raises_validation_error(entry_id, data)
