import contextlib
import uuid
from mockfirestore import MockFirestore  # type: ignore

from springapi.app import create_app, create_config
from springapi.config_helpers import (
    AUTH, KEY, SUBMISSION, TOKEN)
from springapi.helpers import encode_json_uri


def populate_mock_submissions(entries):
    mock_db = MockFirestore()
    for key, data in entries.items():
        mock_db.collection('submissions').add(data, key)

    return mock_db


@contextlib.contextmanager
def make_test_client(environ=None, skip_defaults=False):
    auth_credentials = {"web": {"client_id": "abc123"}}
    environ = environ or {}
    if not skip_defaults:
        environ.setdefault(AUTH, encode_json_uri("google", auth_credentials))
        environ.setdefault(KEY, "secretkey")
        environ.setdefault(SUBMISSION, encode_json_uri("firebase", {}))
        environ.setdefault(TOKEN, encode_json_uri("sqlite", {}))
    config = create_config(environ)
    app = create_app(config)
    with app.test_client() as client:
        yield client


class MockUid:

    @classmethod
    def create_mock_uid(cls):
        return uuid.UUID(int=0)

    @classmethod
    def get_mock_uid_base32(cls):
        return "aaaaaaaaaaaaaaaaaaaaaaaaaa"
