from springapi.exceptions import CollectionNotFound
from tests.helpers import TokenResponseAssertions
from unittest import mock


@mock.patch('springapi.models.firebase.client.get_collection')
class TestTokenGetAllTokens(TokenResponseAssertions):

    def test_get_tokens_returns_list_if_found(self, mock_get):
        expected = mock_get.return_value = {
            "1": {"token": "abc123"},
            "2": {"token": "def456"}
        }
        self.assert_get_tokens_returns_all_valid_tokens(expected)

    def test_get_token_raises_CollectionNotFound(self, mock_get):
        mock_get.side_effect = CollectionNotFound("tokens")
        self.assert_get_tokens_raises_CollectionNotFound()

    def test_get_tokens_omits_invalid_entries(self, mock_get):
        invalid = {"1": {"token": 123}, "2": {"bad_field": "qwerty"}}
        valid = {"3": {"token": "def456"}}
        mock_get.return_value = {**valid, **invalid}
        self.assert_get_tokens_returns_all_valid_tokens(valid)
