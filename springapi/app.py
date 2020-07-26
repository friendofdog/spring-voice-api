from flask import Flask

from springapi.helpers import register
from springapi.routes.healthcheck import healthcheck
from springapi.routes.submissions import get_submissions
from springapi.routes.submission import create_submission, update_submission


def create_app():
    app = Flask(__name__)
    register(app, healthcheck)
    register(app, get_submissions)
    register(app, create_submission)
    register(app, update_submission)
    return app
