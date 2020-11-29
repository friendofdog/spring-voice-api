from springapi.models.submission import COLLECTION, Submission
from tests.models.helpers import ResponseAssertions


class TestSubmissionGetAllSubmissions(ResponseAssertions):

    def test_get_submissions_returns_all_valid_entries(self):
        valid = {"1": {"name": "a", "message": "b", "location": "c"}}
        invalid = {"2": {"name": "d", "message": "e"}}
        self.assert_get_collection_returns_all_valid_entries(
            COLLECTION, Submission.get_submissions, valid, invalid)

    def test_get_submissions_raises_CollectionNotFound(self):
        self.assert_get_collection_raises_CollectionNotFound(
            COLLECTION, Submission.get_submissions)


class TestSubmissionGetSingleSubmission(ResponseAssertions):

    def test_get_submission_returns_submission_if_found_and_valid(self):
        entry_id = "1"
        expected = {
            "id": entry_id, "name": "a", "message": "b", "location": "c"}
        self.assert_get_single_entry_returns_entry(
            COLLECTION, Submission, Submission.get_submission, entry_id,
            expected)

    def test_get_submission_raises_EntryNotFound(self):
        self.assert_get_single_entry_raises_EntryNotFound(
            COLLECTION, Submission.get_submission, "1")


class TestSubmissionCreateSubmission(ResponseAssertions):

    def test_create_submission_returns_json_if_data_valid(self):
        data = {"name": "a", "location": "b", "message": "c"}
        self.assert_create_entry_returns_success(
            COLLECTION, Submission, Submission.create_submission, data)

    def test_create_submission_raises_ValidationError_not_allowed(self):
        message = "bad_field"
        data = {"name": "a", "message": "b", "location": "c", "bad_field": "d"}
        self.assert_create_entry_raises_ValidationError(
            Submission.create_submission, data, message, "not_allowed")

    def test_create_submission_raises_ValidationError_missing(self):
        message = "location"
        data = {"name": "a", "message": "b"}
        self.assert_create_entry_raises_ValidationError(
            Submission.create_submission, data, message, "missing")

    def test_create_submission_raises_ValidationError_type(self):
        data = {"name": "a", "message": "b", "location": 10}
        message = "location is <class 'int'>, should be <class 'str'>."
        self.assert_create_entry_raises_ValidationError(
            Submission.create_submission, data, message, "type")

    def test_create_submission_raises_EntryAlreadyExists(self):
        data = {"name": "a", "location": "b", "message": "c"}
        self.assert_create_entry_raises_EntryAlreadyExists(
            COLLECTION, Submission.create_submission, data)


class TestSubmissionUpdateSubmission(ResponseAssertions):

    def test_update_submission_returns_success_if_found_and_valid(self):
        entry_id = "1"
        data = {"name": "a", "location": "b", "message": "c"}
        self.assert_update_single_entry_returns_success(
            COLLECTION, Submission.update_submission, entry_id, data)

    def test_update_submission_raises_EntryNotFound(self):
        entry_id = "1"
        data = {"name": "a", "location": "b", "message": "c"}
        self.assert_update_single_entry_raises_EntryNotFound(
            COLLECTION, Submission.update_submission, entry_id, data)

    def test_update_submission_raises_ValidationError_not_allowed(self):
        message = "bad_field"
        data = {"name": "a", "location": "b", "message": "c", "bad_field": "d"}
        self.assert_update_single_entry_raises_ValidationError(
            Submission.update_submission, data, message, "not_allowed")

    def test_update_submission_raises_ValidationError_missing(self):
        message = "location"
        data = {"name": "a", "message": "c"}
        self.assert_update_single_entry_raises_ValidationError(
            Submission.update_submission, data, message, "missing")

    def test_update_submission_raises_ValidationError_type(self):
        message = "location is <class 'int'>, should be <class 'str'>."
        data = {"name": "a", "location": 123, "message": "c"}
        self.assert_update_single_entry_raises_ValidationError(
            Submission.update_submission, data, message, "type")
