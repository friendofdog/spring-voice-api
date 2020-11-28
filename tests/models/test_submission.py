from tests.helpers import MockUid
from tests.models.helpers import SubmissionResponseAssertions


class TestSubmissionGetAllSubmissions(SubmissionResponseAssertions):

    def test_get_submissions_returns_all_valid_entries(self):
        valid = {"1": {"name": "a", "message": "b", "location": "c"}}
        invalid = {"2": {"name": "d", "message": "e"}}
        self.assert_get_submissions_returns_all_valid_submissions(
            valid, invalid)

    def test_get_submissions_raises_CollectionNotFound(self):
        self.assert_get_submissions_raises_CollectionNotFound()


class TestSubmissionGetSingleSubmission(SubmissionResponseAssertions):

    def test_get_submission_returns_submission_if_found(self):
        entry_id = "1"
        expected = {
            "id": entry_id, "name": "a", "message": "b", "location": "c"}
        self.assert_get_single_submission_returns_single(entry_id, expected)

    def test_get_submission_raises_EntryNotFound(self):
        entry_id = "1"
        err = {'error': f'{entry_id} was not found in submissions'}
        self.assert_get_single_submission_raises_EntryNotFound(entry_id, err)


class TestSubmissionCreateSubmission(SubmissionResponseAssertions):

    def test_create_submission_returns_json_if_data_valid(self):
        data = {"name": "a", "location": "b", "message": "c"}
        self.assert_create_submission_returns_success(data)

    def test_create_submission_raises_ValidationError_disallowed(self):
        data = {"name": "a", "message": "b", "location": "c", "bad_field": "d"}
        err = {"error": "Not allowed: bad_field"}
        self.assert_create_submission_raises_ValidationError(data, err)

    def test_create_submission_raises_ValidationError_missing(self):
        data = {"name": "a", "message": "b"}
        err = {"error": "Missing: location"}
        self.assert_create_submission_raises_ValidationError(data, err)

    def test_create_submission_raises_ValidationError_type(self):
        data = {"name": "a", "message": "b", "location": 10}
        err = {"error": "location is <class 'int'>, should be <class 'str'>."}
        self.assert_create_submission_raises_ValidationError(data, err)

    def test_create_submission_raises_EntryAlreadyExists(self):
        data = {"name": "a", "location": "b", "message": "c"}
        uid = MockUid.get_mock_uid_base32()
        err = {"error": f"{uid} already exists in submissions"}
        self.assert_create_submission_raises_AlreadyExists(data, err)


class TestSubmissionUpdateSubmission(SubmissionResponseAssertions):

    def test_update_submission_returns_success_if_found_and_valid(self):
        entry_id = "1"
        data = {"name": "a", "location": "b", "message": "c"}
        self.assert_update_submission_returns_success(entry_id, data)

    def test_update_submission_raises_EntryNotFound(self):
        entry_id = "1"
        err = {'error': f'{entry_id} was not found in submissions'}
        data = {"name": "a", "location": "b", "message": "c"}
        self.assert_update_submission_raises_EntryNotFound(entry_id, data, err)

    def test_update_submission_raises_ValidationError_disallowed(self):
        entry_id = "1"
        err = {"error": "Not allowed: bad_field"}
        data = {"name": "a", "location": "b", "message": "c", "bad_field": "d"}
        self.assert_update_submission_raises_ValidationError(
            entry_id, data, err)

    def test_update_submission_raises_ValidationError_missing(self):
        entry_id = "1"
        err = {"error": "Missing: location"}
        data = {"name": "a", "message": "c"}
        self.assert_update_submission_raises_ValidationError(
            entry_id, data, err)

    def test_update_submission_raises_ValidationError_type(self):
        entry_id = "1"
        err = {"error": "location is <class 'int'>, should be <class 'str'>."}
        data = {"name": "a", "location": 123, "message": "c"}
        self.assert_update_submission_raises_ValidationError(
            entry_id, data, err)
