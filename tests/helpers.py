import contextlib

from app.routes.healthcheck import app


@contextlib.contextmanager
def test_client():
    # add setup, configuration, etc. here
    with app.test_client() as client:
        yield client
    # add teardown, cleanup, etc. here.
