from springapi.models import exceptions
from springapi.models.submission import Submission
from tests.helpers import RouteResponseAssertions
from unittest import mock


@mock.patch('springapi.models.firebase.client.get_collection')
class TestSubmissionsRouteGetAll(RouteResponseAssertions):

    def test_get_all_returns_not_found(self, mocked):
        err = mocked.side_effect = exceptions.CollectionNotFound('submissions')
        self.assert_get_raises_not_found(
            '/api/v1/submissions', err.error_response_body())

    def test_get_all_returns_empty_list(self, mocked):
        entries = mocked.return_value = {}
        self.assert_get_raises_ok(
            '/api/v1/submissions', {'submissions': entries})

    def test_get_all_returns_entries_if_found(self, mocked):
        entries = mocked.return_value = {
            "1": {"name": "Some Guy", "message": "Hi there", "location": ""},
            "2": {
                "name": "Another Fellow",
                "message": "Goodbye",
                "location": ""
            }
        }
        self.assert_get_raises_ok(
            '/api/v1/submissions', {'submissions': entries})


@mock.patch('springapi.models.firebase.client.get_entry')
class TestSubmissionsRouteGetSingle(RouteResponseAssertions):

    def test_get_single_returns_not_found(self, mocked):
        entry_id = 'abc'
        err = mocked.side_effect = exceptions.EntryNotFound(
            entry_id, 'submissions')
        self.assert_get_raises_not_found(
            f'/api/v1/submissions/{entry_id}', err.error_response_body())

    def test_get_single_returns_entry_if_found(self, mocked):
        entry_id = 'abc'
        mocked.return_value = {
            'name': 'Guy',
            'message': '',
            'location': 'There'
        }
        expected = Submission.from_json({
            'id': entry_id,
            'name': 'Guy',
            'message': '',
            'location': 'There'
        })
        self.assert_get_raises_ok(
            f'/api/v1/submissions/{entry_id}', expected.to_json())


@mock.patch('springapi.models.firebase.client.add_entry')
class TestSubmissionsRouteCreate(RouteResponseAssertions):

    def test_create_single_returns_conflict_if_already_exists(self, mocked):
        err = mocked.side_effect = exceptions.EntryAlreadyExists(
            'abc', 'submissions')
        body = {
            "id": "abc",
            "name": "a",
            "message": "b",
            "location": "c"
        }
        self.assert_post_raises_already_exists(
            '/api/v1/submissions', body, err.error_response_body())

    def test_create_single_rejects_invalid_json(self, mocked):
        err = exceptions.ValidationError('Invalid JSON')
        self.assert_post_raises_invalid_body(
            '/api/v1/submissions', err.error_response_body())

    def test_create_single_returns_created_on_success(self, mocked):
        data = {
            "id": "abc",
            "name": "b",
            "message": "b",
            "location": "b",
        }
        mocked.return_value = {'abc': data}

        expected = Submission.from_json(data).to_json()
        self.assert_post_raises_ok('/api/v1/submissions', data, expected)
        mocked.assert_called_with("submissions", expected)


@mock.patch('springapi.models.firebase.client.update_entry')
class TestSubmissionsRouteUpdate(RouteResponseAssertions):

    def test_update_single_returns_not_found(self, mocked):
        entry_id = 'abc'
        body = {
            "id": entry_id,
            "name": "",
            "location": "",
            "message": ""
        }
        err = mocked.side_effect = exceptions.EntryNotFound(
            entry_id, 'submissions')
        self.assert_put_raises_not_found(
            f'api/v1/submissions/{entry_id}', body, err.error_response_body())

    def test_update_single_rejects_invalid_json(self, mocked):
        entry_id = 'abc'
        err = exceptions.ValidationError('Invalid JSON')
        self.assert_put_raises_invalid_body(
            f'/api/v1/submissions/{entry_id}',
            err.error_response_body()
        )

    def test_update_single_returns_ok_on_success(self, mocked):
        entry_id = 'abc'
        data = {
            "id": entry_id,
            "name": "b",
            "location": "b",
            "message": "b"
        }
        mocked.return_value = {entry_id: data}
        expected = Submission.from_json(data).to_json()
        self.assert_put_raises_ok(
            f'/api/v1/submissions/{entry_id}', data, expected)
        mocked.assert_called_with("submissions", expected, entry_id)
