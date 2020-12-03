from springapi.models.token import COLLECTION, Token
from tests.models.helpers import ModelResponseAssertions


class TestTokenGetAllTokens(ModelResponseAssertions):

    def test_get_tokens_returns_all_valid_entries(self):
        valid = {"1": {"token": "def456"}}
        invalid = {"2": {"token": 123}, "3": {"bad_field": "qwerty"}}
        self.assert_get_collection_returns_all_valid_entries(
            COLLECTION, Token.get_tokens, valid, invalid)

    def test_get_token_raises_CollectionNotFound(self):
        self.assert_get_collection_raises_CollectionNotFound(
            COLLECTION, Token.get_tokens)


class TestTokenCreateToken(ModelResponseAssertions):

    def test_create_token_returns_json_if_data_valid(self):
        data = {"token": "abc123"}
        self.assert_create_entry_returns_success(
            COLLECTION, Token, Token.create_token, data)

    def test_create_token_raises_ValidationError_not_allowed(self):
        data = {"token": "abc123", "bad_field": "err"}
        message = "bad_field"
        self.assert_create_entry_raises_ValidationError(
            Token.create_token, data, message, "not_allowed")

    def test_create_token_raises_ValidationError_missing(self):
        data = {}
        message = "token"
        self.assert_create_entry_raises_ValidationError(
            Token.create_token, data, message, "missing")

    def test_create_token_raises_ValidationError_type(self):
        data = {"token": 123}
        message = "token is <class 'int'>, should be <class 'str'>."
        self.assert_create_entry_raises_ValidationError(
            Token.create_token, data, message, "type")

    def test_create_token_raises_EntryAlreadyExists(self):
        data = {"token": "abc123"}
        self.assert_create_entry_raises_EntryAlreadyExists(
            COLLECTION, Token.create_token, data)
