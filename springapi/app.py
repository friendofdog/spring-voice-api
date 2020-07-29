from flask import Flask
import os

from springapi.helpers import register
from springapi.models.firebase.app import authenticate
from springapi.routes.healthcheck import healthcheck
from springapi.routes.submissions \
    import get_submissions, create_submission, update_submission


def create_app():
    app = Flask(__name__)
    register(app, healthcheck)
    register(app, get_submissions)
    register(app, create_submission)
    register(app, update_submission)
    return app


def main():
    authenticate()
    app = create_app()
    app.run()


if __name__ == "__main__":
    main()
