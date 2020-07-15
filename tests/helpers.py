import contextlib

from springapi.app import create_app


@contextlib.contextmanager
def test_client():
    # add setup, configuration, etc. here
    app = create_app()
    with app.test_client() as client:
        yield client
    # add teardown, cleanup, etc. here.
