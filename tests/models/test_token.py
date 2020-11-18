from springapi.exceptions import CollectionNotFound, EntryAlreadyExists
from tests.helpers import TokenResponseAssertions
from unittest import mock


@mock.patch('springapi.models.firebase.client.get_collection')
class TestTokenGetAllTokens(TokenResponseAssertions):

    def test_get_tokens_returns_all_entries_if_all_valid(self, mock_get):
        expected = mock_get.return_value = {
            "1": {"token": "abc123"},
            "2": {"token": "def456"}
        }
        self.assert_get_tokens_returns_all_valid_tokens(expected)

    def test_get_tokens_omits_invalid_entries(self, mock_get):
        invalid = {
            "1": {"token": 123},
            "2": {"bad_field": "qwerty"}
        }
        valid = {"3": {"token": "def456"}}
        mock_get.return_value = {**valid, **invalid}
        self.assert_get_tokens_returns_all_valid_tokens(valid)

    def test_get_token_raises_CollectionNotFound(self, mock_get):
        mock_get.side_effect = CollectionNotFound("tokens")
        self.assert_get_tokens_raises_CollectionNotFound()


@mock.patch('springapi.models.token.create_uid')
class TestTokenCreateToken(TokenResponseAssertions):

    @mock.patch('springapi.models.firebase.client.add_entry')
    def test_create_token_returns_json_if_valid(
            self, mock_add, mock_id):
        entry_id = mock_id.return_value = "abc"
        data = {"id": entry_id, "token": "abc123"}
        mock_add.return_value = {entry_id: data}
        self.assert_create_token_returns_success(data)
        mock_add.assert_called_with("tokens", data)

    def test_create_token_raises_ValidationError_if_disallowed(
            self, mock_id):
        entry_id = mock_id.return_value = "abc"
        data = {"id": entry_id, "token": "abc123", "bad_field": "err"}
        self.assert_create_token_raises_validation_error(data)

    def test_create_token_raises_ValidationError_if_missing(self, mock_id):
        entry_id = mock_id.return_value = "abc"
        data = {"id": entry_id}
        self.assert_create_token_raises_validation_error(data)

    def test_create_token_raises_ValidationError_if_bad_type(self, mock_id):
        entry_id = mock_id.return_value = "abc"
        data = {"id": entry_id, "token": 123}
        self.assert_create_token_raises_validation_error(data)

    @mock.patch('springapi.models.firebase.client.add_entry')
    def test_create_token_raises_EntryAlreadyExists_if_id_found(
            self, mock_add, mock_id):
        entry_id = mock_id.return_value = "abc"
        data = {"id": entry_id, "token": "abc123"}
        mock_add.side_effect = EntryAlreadyExists(entry_id, "tokens")
        self.assert_create_token_raises_already_exists(entry_id, data)
