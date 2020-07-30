import contextlib
from mockfirestore import MockFirestore
from springapi.app import create_app


class MockDatabase(object):

    def __init__(self):
        self._submissions = []

    def add_entry(self, submission):
        self._submissions.append(submission)
        return self._submissions[-1], 201

    def update_entry(self, update):
        i, sub = next(([i, s] for i, s in enumerate(self._submissions)
                       if s['id'] == update['id']), ['', ''])
        if sub:
            self._submissions[i] = update
            return self._submissions[i], 200
        else:
            add = self.add_entry(update)
            return add

    def get_collection(self):
        return self._submissions


def populate_mock_firestore_submissions():
    initial_entries = [
        {"name": "Some Guy", "message": "Hi there"},
        {"name": "Another Fellow", "message": "Goodbye"}
    ]

    mock_db = MockFirestore()
    for entry in initial_entries:
        mock_db.collection('submissions').add(entry)

    return mock_db


@contextlib.contextmanager
def make_test_client():
    app = create_app()
    with app.test_client() as client:
        yield client
