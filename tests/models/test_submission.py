from tests.helpers import SubmissionResponseAssertions
from springapi.models import exceptions
from unittest import mock


@mock.patch('springapi.models.firebase.client.get_collection')
class TestSubmissionGetAllSubmissions(SubmissionResponseAssertions):

    def test_get_submissions_raises_CollectionNotFound(self, mock_get):
        mock_get.side_effect = exceptions.CollectionNotFound('submissions')
        self.assert_get_submissions_raises_not_found()

    def test_get_submissions_returns_list_if_found(self, mock_get):
        entries = mock_get.return_value = {'a': 'b'}
        self.assert_get_submissions_returns_all_submissions(entries)


@mock.patch('springapi.models.firebase.client.get_entry')
class TestSubmissionGetSingleSubmission(SubmissionResponseAssertions):

    def test_get_submission_raises_EntryNotFound(self, mock_get):
        entry_id = 'abc'
        mock_get.side_effect = exceptions.EntryNotFound(
            entry_id, 'submissions')
        self.assert_get_single_submission_raises_not_found(entry_id)

    def test_get_submission_returns_submission_if_found(self, mock_get):
        entries = {'a': 'this', 'b': 'that'}
        entry_id = 'a'
        returned = mock_get.return_value = entries[entry_id]
        self.assert_get_single_submission_returns_single(returned, entry_id)


class TestSubmissionCreateSubmission(SubmissionResponseAssertions):

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

    @mock.patch('springapi.models.firebase.client.add_entry')
    def test_create_submission_returns_submission_data_if_valid(
            self, mock_add):
        entry_id = 'abc'
        data = {'name': 'a', 'location': 'b', 'message': 'c'}
        mock_add.return_value = {entry_id: data}
        self.assert_create_submission_returns_success(entry_id, data)


class TestSubmissionUpdateSubmission(SubmissionResponseAssertions):

    @mock.patch('springapi.models.firebase.client.update_entry')
    def test_update_submission_raises_EntryNotFound(
            self, mock_update):
        entry_id = 'abc'
        data = {'name': 'a', 'location': 'b', 'message': 'new message'}
        mock_update.side_effect = exceptions.EntryNotFound(entry_id, 'def')
        self.assert_update_submission_raises_not_found(entry_id, data)

    def test_update_submission_raises_ValidationError(self):
        entry_id = 'abc'
        data = {'name': 'a', 'message': 'new message'}
        self.assert_update_submission_raises_validation_error(entry_id, data)

    @mock.patch('springapi.models.firebase.client.update_entry')
    def test_update_submission_returns_submission_data_if_found_and_valid(
            self, mock_update):
        entry_id = 'abc'
        data = {'name': 'a', 'location': 'b', 'message': 'new message'}
        mock_update.return_value = {entry_id: data}
        self.assert_update_submission_returns_success(entry_id, data)
