import contextlib
from mockfirestore import MockFirestore  # type: ignore
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


def populate_mock_firestore_submissions(entries):

    mock_db = MockFirestore()
    for key, data in entries.items():
        mock_db.collection('submissions').add(data, key)

    return mock_db


@contextlib.contextmanager
def make_test_client():
    app = create_app()
    with app.test_client() as client:
        yield client
