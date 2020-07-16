import contextlib
import sys

from springapi.app import create_app


def test_app_dev():
    sys.argv.append('--env=test')
    app = create_app()
    return app


@contextlib.contextmanager
def test_client():
    app = test_app_dev()
    with app.test_client() as client:
        yield client
