import contextlib
from springapi.app import create_app


@contextlib.contextmanager
def make_test_client():
    app = create_app('TestingConfig')
    with app.test_client() as client:
        yield client
