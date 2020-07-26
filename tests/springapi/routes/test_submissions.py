import unittest
from unittest import mock
from tests.springapi.helpers import make_test_client


class MockFirebase(object):

    def __init__(self):
        self._submissions = []

    def add_submission(self, submission):
        self._submissions.append(submission)
        return submission

    def update_submission(self, submission):
        self._submissions[0] = submission
        return submission

    def get_submissions(self):
        return self._submissions


class TestSubmissionsRoute(unittest.TestCase):

    @mock.patch('springapi.routes.submissions.get_collection')
    def test_get_returns_empty_list_without_submissions(self, mocked):
        empty_list = []
        mocked.return_value = empty_list

        with make_test_client() as client:
            response = client.get("/api/v1/submissions")
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual({"submissions": empty_list}, json)

    @mock.patch('springapi.routes.submissions.get_collection')
    def test_get_returns_submissions_in_list(self, mocked):
        mock_firebase = MockFirebase()
        mock_submission = {"name": "Foo Bar", "message": "foobar"}
        mock_firebase.add_submission(mock_submission)
        mocked.return_value = mock_firebase.get_submissions()

        with make_test_client() as client:
            response = client.get("/api/v1/submissions")
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual({"submissions": [mock_submission]}, json)

    @mock.patch('springapi.routes.submissions.add_entry')
    def test_post_returns_submission(self, mocked):
        mock_firebase = MockFirebase()
        mock_submission = {"name": "Some Guy", "message": "Hi there"}
        mocked.return_value = mock_firebase.add_submission(mock_submission)

        with make_test_client() as client:
            response = client.post("/api/v1/submission", data=mock_submission)
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual(mock_submission, json)

    @mock.patch('springapi.routes.submissions.update_entry')
    def test_put_returns_updated_submission(self, mocked):
        mock_firebase = MockFirebase()
        mock_submission = {"name": "Other Guy", "message": "Hi there"}
        mock_update = {"name": "Some Guy", "message": "Goodbye"}
        mock_firebase.add_submission(mock_submission)
        mocked.return_value = mock_firebase.update_submission(mock_update)
        print(mock_firebase)

        with make_test_client() as client:
            response = client.put("/api/v1/submission", data=mock_update)
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual(mock_update, json)
