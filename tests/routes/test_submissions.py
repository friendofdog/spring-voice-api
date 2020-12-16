from springapi.exceptions import \
    CollectionNotFound, EntryNotFound, EntryAlreadyExists, ValidationError
from springapi.models.submission import Submission
from tests.routes.helpers import RouteResponseAssertions
from unittest import mock


MOCK_TOKENS = ["abc", "def"]


@mock.patch('springapi.routes.helpers.get_valid_admin_tokens')
@mock.patch('springapi.models.firebase.client.get_collection')
class TestSubmissionsRouteGetAll(RouteResponseAssertions):

    def test_get_all_requires_admin_authentication(self, mocked, auth):
        self.assert_requires_admin_authentication(
            "get", "/api/v1/submissions")

    def test_get_all_returns_entries_if_found(self, mocked, auth):
        auth.return_value = MOCK_TOKENS
        mocked.return_value = {
            "abc": {
                "name": "Some Guy",
                "message": "Hi there",
                "location": "Here"
            },
            "def": {
                "name": "Another Fellow",
                "message": "Goodbye",
                "location": "There"
            }
        }
        expected = [
            Submission.from_json({
                "id": "abc",
                "name": "Some Guy",
                "message": "Hi there",
                "location": "Here"
            }).to_json(),
            Submission.from_json({
                "id": "def",
                "name": "Another Fellow",
                "message": "Goodbye",
                "location": "There"
            }).to_json()
        ]
        self.assert_get_raises_ok(
            '/api/v1/submissions', {'submissions': expected},
            credentials={"Authorization": "Bearer abc"})
        mocked.assert_called_with('submissions')

    def test_get_all_returns_empty_list(self, mocked, auth):
        auth.return_value = MOCK_TOKENS
        mocked.return_value = {}
        self.assert_get_raises_ok(
            '/api/v1/submissions', {'submissions': []},
            credentials={"Authorization": "Bearer abc"})
        mocked.assert_called_with('submissions')

    def test_get_all_omits_entries_with_required_field_missing(
            self, mocked, auth):
        auth.return_value = MOCK_TOKENS
        mocked.return_value = {
            "abc": {
                "name": "Some Guy",
                "message": "Hi there",
                "location": "There"
            },
            "def": {
                "name": "Another Fellow",
                "message": "Goodbye"
            }
        }
        expected = Submission.from_json({
            "id": "abc",
            "name": "Some Guy",
            "message": "Hi there",
            "location": "There"
        }).to_json()
        self.assert_get_raises_ok(
            '/api/v1/submissions', {'submissions': [expected]},
            credentials={"Authorization": "Bearer abc"})
        mocked.assert_called_with('submissions')

    def test_get_all_returns_not_found(self, mocked, auth):
        auth.return_value = MOCK_TOKENS
        err = mocked.side_effect = CollectionNotFound('submissions')
        self.assert_get_raises_not_found(
            '/api/v1/submissions', err.error_response_body(),
            credentials={"Authorization": "Bearer abc"})

    def test_get_all_omits_entries_with_invalid_field(self, mocked, auth):
        auth.return_value = MOCK_TOKENS
        mocked.return_value = {
            "abc": {
                "name": "Some Guy",
                "message": "Hi there",
                "location": "There"
            },
            "def": {
                "name": "Another Fellow",
                "message": "Goodbye",
                "location": "There",
                "bad_field": "invalid"
            }
        }
        expected = Submission.from_json({
            "id": "abc",
            "name": "Some Guy",
            "message": "Hi there",
            "location": "There"
        }).to_json()
        self.assert_get_raises_ok(
            '/api/v1/submissions', {'submissions': [expected]},
            credentials={"Authorization": "Bearer abc"})
        mocked.assert_called_with('submissions')


@mock.patch('springapi.routes.helpers.get_valid_admin_tokens')
@mock.patch('springapi.models.firebase.client.get_entry')
class TestSubmissionsRouteGetSingle(RouteResponseAssertions):

    def test_get_single_requires_admin_authentication(self, mocked, auth):
        auth.return_value = MOCK_TOKENS
        self.assert_requires_admin_authentication(
            "get", "/api/v1/submissions/abc")

    def test_get_single_returns_entry_if_found(self, mocked, auth):
        auth.return_value = MOCK_TOKENS
        entry_id = 'abc'
        mocked.return_value = {
            'name': 'Guy',
            'message': 'Hi',
            'location': 'There'
        }
        expected = Submission.from_json({
            'id': entry_id,
            'name': 'Guy',
            'message': 'Hi',
            'location': 'There'
        })
        self.assert_get_raises_ok(
            f'/api/v1/submissions/{entry_id}', expected.to_json(),
            credentials={"Authorization": "Bearer abc"})
        mocked.assert_called_with("submissions", entry_id)

    def test_get_single_returns_not_found(self, mocked, auth):
        auth.return_value = MOCK_TOKENS
        entry_id = 'abc'
        err = mocked.side_effect = EntryNotFound(
            entry_id, 'submissions')
        self.assert_get_raises_not_found(
            f'/api/v1/submissions/{entry_id}', err.error_response_body(),
            credentials={"Authorization": "Bearer abc"})

    def test_get_single_returns_error_if_disallowed_field(self, mocked, auth):
        auth.return_value = MOCK_TOKENS
        entry_id = 'abc'
        mocked.return_value = {
            'name': 'Guy',
            'message': 'Hi',
            'location': 'There',
            'bad_field': 'not allowed'
        }
        expected = {
            'error': 'validation_failure', 'message': 'Not allowed: bad_field'}
        self.assert_get_raises_invalid_body(
            f'/api/v1/submissions/{entry_id}', expected,
            credentials={"Authorization": "Bearer abc"})

    def test_get_single_returns_error_if_missing_required_field(
            self, mocked, auth):
        auth.return_value = MOCK_TOKENS
        entry_id = 'abc'
        mocked.return_value = {
            'name': 'Guy',
            'message': 'Hi'
        }
        expected = {
            'error': 'validation_failure', 'message': 'Missing: location'}
        self.assert_get_raises_invalid_body(
            f'/api/v1/submissions/{entry_id}', expected,
            credentials={"Authorization": "Bearer abc"})


@mock.patch('springapi.models.firebase.client.add_entry')
class TestSubmissionsRouteCreate(RouteResponseAssertions):

    @mock.patch('springapi.models.submission.create_uid')
    def test_create_single_returns_created_on_success(self, mock_id, mock_add):
        entry_id = mock_id.return_value = 'abc'
        data = {"name": "a", "message": "b", "location": "c"}
        mock_add.return_value = {entry_id: data}

        data["id"] = entry_id  # _create_uid()
        expected = Submission.from_json(data).to_json()
        self.assert_post_raises_created('/api/v1/submissions', data, expected)
        mock_add.assert_called_with("submissions", expected)

    @mock.patch('springapi.models.submission.create_uid')
    def test_create_single_raises_EntryAlreadyExists(self, mock_id, mock_add):
        entry_id = mock_id.return_value = 'abc'
        err = mock_add.side_effect = EntryAlreadyExists(
            entry_id, 'submissions')
        body = {"name": "a", "message": "b", "location": "c"}
        self.assert_post_raises_already_exists(
            '/api/v1/submissions', body, err.error_response_body())

    def test_create_single_rejects_invalid_json(self, mock_add):
        invalid_body = b"foobar"
        err = mock_add.side_effect = ValidationError(
            [[invalid_body, type(invalid_body), "json"]], "type")
        self.assert_post_raises_invalid_body(
            '/api/v1/submissions', err.error_response_body(), invalid_body)


@mock.patch('springapi.routes.helpers.get_valid_admin_tokens')
@mock.patch('springapi.models.firebase.client.update_entry')
class TestSubmissionsRouteUpdate(RouteResponseAssertions):

    def test_update_single_returns_success(self, mocked, auth):
        auth.return_value = MOCK_TOKENS
        entry_id = 'abc'
        data = {"id": entry_id, "name": "b", "location": "b", "message": "b"}
        expected = mocked.return_value = {'success': f'{entry_id} updated'}
        self.assert_put_raises_ok(
            f'/api/v1/submissions/{entry_id}', data, expected,
            credentials={"Authorization": "Bearer abc"})
        mocked.assert_called_with(
            "submissions", Submission.from_json(data).to_json(), entry_id)

    def test_update_single_returns_not_found(self, mocked, auth):
        auth.return_value = MOCK_TOKENS
        entry_id = 'abc'
        body = {"id": entry_id, "name": "", "location": "", "message": ""}
        err = mocked.side_effect = EntryNotFound(
            entry_id, 'submissions')
        self.assert_put_raises_not_found(
            f'api/v1/submissions/{entry_id}', body, err.error_response_body(),
            credentials={"Authorization": "Bearer abc"})

    def test_update_single_rejects_invalid_json(self, mocked, auth):
        auth.return_value = MOCK_TOKENS
        entry_id = 'abc'
        invalid_body = b"foobar"
        err = mocked.side_effect = ValidationError(
            [[invalid_body, type(invalid_body), "json"]], "type")
        self.assert_put_raises_invalid_body(
            f'/api/v1/submissions/{entry_id}', err.error_response_body(),
            invalid_body, credentials={"Authorization": "Bearer abc"})
