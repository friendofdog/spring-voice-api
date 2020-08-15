from springapi.models import exceptions
from tests.helpers import ResponseAssertions
from unittest import mock


class TestSubmissionsRoute(ResponseAssertions):

    @mock.patch('springapi.routes.submissions.Submission.get_submissions')
    def test_get_all_returns_not_found(self, mocked):
        err = mocked.side_effect = exceptions.CollectionNotFound('submissions')
        self.assert_get_raises_not_found(
            '/api/v1/submissions', err.error_response_body())

    @mock.patch('springapi.routes.submissions.Submission.get_submissions')
    def test_get_all_returns_empty_list(self, mocked):
        entries = mocked.return_value = {}
        self.assert_get_raises_ok(
            '/api/v1/submissions', {'submissions': entries})

    @mock.patch('springapi.routes.submissions.Submission.get_submissions')
    def test_get_all_returns_entries_if_found(self, mocked):
        entries = mocked.return_value = {
            "1": {"name": "Some Guy", "message": "Hi there"},
            "2": {"name": "Another Fellow", "message": "Goodbye"}
        }
        self.assert_get_raises_ok(
            '/api/v1/submissions', {'submissions': entries})

    @mock.patch('springapi.routes.submissions.Submission.get_submission')
    def test_get_single_returns_not_found(self, mocked):
        entry_id = 'abc'
        err = mocked.side_effect = exceptions.EntryNotFound(
            entry_id, 'submissions')
        self.assert_get_raises_not_found(
            f'/api/v1/submissions/{entry_id}', err.error_response_body())

    @mock.patch('springapi.routes.submissions.Submission.get_submission')
    def test_get_single_returns_entry_if_found(self, mocked):
        entry_id = 'abc'
        data = mocked.return_value = {'name': 'Guy', 'location': 'There'}
        self.assert_get_raises_ok(
            f'/api/v1/submissions/{entry_id}', {entry_id: data})

    @mock.patch('springapi.routes.submissions.Submission.create_submission')
    def test_create_single_returns_conflict_if_already_exists(self, mocked):
        err = mocked.side_effect = exceptions.EntryAlreadyExists(
            'abc', 'submissions')
        self.assert_post_raises_already_exists(
            '/api/v1/submissions', err.error_response_body())

    @mock.patch('springapi.routes.submissions.Submission.create_submission')
    def test_create_single_rejects_invalid_json(self, mocked):
        err = mocked.side_effect = exceptions.ValidationError('invalid')
        self.assert_post_raises_invalid_body(
            '/api/v1/submissions', err.error_response_body())

    @mock.patch('springapi.routes.submissions.Submission.create_submission')
    def test_create_single_returns_created_on_success(self, mocked):
        data = mocked.return_value = {'abc': {'a': 'b'}}
        self.assert_post_raises_ok('/api/v1/submissions', data)

    @mock.patch('springapi.routes.submissions.Submission.update_submission')
    def test_update_single_returns_not_found(self, mocked):
        entry_id = 'abc'
        err = mocked.side_effect = exceptions.EntryNotFound(
            entry_id, 'submissions')
        self.assert_put_raises_not_found(
            f'api/v1/submissions/{entry_id}', err.error_response_body())

    @mock.patch('springapi.routes.submissions.Submission.update_submission')
    def test_update_single_rejects_invalid_json(self, mocked):
        entry_id = 'abc'
        err = mocked.side_effect = exceptions.ValidationError('invalid')
        self.assert_put_raises_invalid_body(
            f'/api/v1/submissions/{entry_id}',
            err.error_response_body()
        )

    @mock.patch('springapi.routes.submissions.Submission.update_submission')
    def test_update_single_returns_ok_on_success(self, mocked):
        entry_id = 'abc'
        data = mocked.return_value = {entry_id: {'a': 'b'}}
        self.assert_put_raises_ok(f'/api/v1/submissions/{entry_id}', data)
