import contextlib
from springapi.app import create_app


class MockDatabase(object):

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


@contextlib.contextmanager
def make_test_client():
    app = create_app()
    with app.test_client() as client:
        yield client
