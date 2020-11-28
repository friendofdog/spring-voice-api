from tests.models.helpers import TokenResponseAssertions
from tests.helpers import MockUid


class TestTokenGetAllTokens(TokenResponseAssertions):

    def test_get_tokens_returns_all_valid_entries(self):
        valid = {"1": {"token": "def456"}}
        invalid = {"2": {"token": 123}, "3": {"bad_field": "qwerty"}}
        self.assert_get_tokens_returns_all_valid_tokens(valid, invalid)

    def test_get_token_raises_CollectionNotFound(self):
        self.assert_get_tokens_raises_CollectionNotFound()


class TestTokenCreateToken(TokenResponseAssertions):

    def test_create_token_returns_json_if_data_valid(self):
        data = {"token": "abc123"}
        self.assert_create_token_returns_success(data)

    def test_create_token_raises_ValidationError_if_bad_field(self):
        data = {"token": "abc123", "bad_field": "err"}
        err = {"error": "Not allowed: bad_field"}
        self.assert_create_token_raises_ValidationError(data, err)

    def test_create_token_raises_ValidationError_if_missing_field(self):
        data = {}
        err = {"error": "Missing: token"}
        self.assert_create_token_raises_ValidationError(data, err)

    def test_create_token_raises_ValidationError_if_bad_field_value(self):
        data = {"token": 123}
        err = {'error': "token is <class 'int'>, should be <class 'str'>."}
        self.assert_create_token_raises_ValidationError(data, err)

    def test_create_token_raises_EntryAlreadyExists_if_id_found(self):
        data = {"token": "abc123"}
        uid = MockUid.get_mock_uid_base32()
        err = {"error": f"{uid} already exists in tokens"}
        self.assert_create_token_raises_EntryAlreadyExists(data, err)
