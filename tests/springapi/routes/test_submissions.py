import unittest

from tests.springapi.helpers import make_test_client
from springapi.config import Configuration


class MockFirebase(object):

    def __init__(self):
        self._submissions = []

    def add_submission(self, submission):
        self._submissions.append(submission)

    def get_submissions(self):
        return self._submissions


class TestSubmissionsRoute(unittest.TestCase):

    def test_get_returns_empty_submission_list_without_submissions(self):
        with make_test_client() as client:
            response = client.get("/api/v1/submissions")
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual({"submissions": []}, json)

    def test_get_returns_submissions_in_list(self):
        mock_firebase = MockFirebase()
        mock_submission = {"name": "Foo Bar", "message": "foobar"}
        mock_firebase.add_submission(mock_submission)
        config = Configuration(firebase=mock_firebase)

        with make_test_client(config) as client:
            response = client.get("/api/v1/submissions")
            self.assertEqual("200 OK", response.status)
            json = response.get_json()
            self.assertEqual(
                "application/json", response.headers["Content-type"])
            self.assertEqual({"submissions": [mock_submission]}, json)
