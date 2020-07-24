import contextlib
from springapi.app import create_app


@contextlib.contextmanager
def make_test_client(configuration):
    app = create_app(configuration)
    with app.test_client() as client:
        yield client
