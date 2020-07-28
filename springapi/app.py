from flask import Flask
from dotenv import load_dotenv

from springapi.helpers import register
from springapi.routes.healthcheck import healthcheck
from springapi.routes.submissions \
    import get_submissions, create_submission, update_submission


def create_app():
    load_dotenv()
    app = Flask(__name__)
    register(app, healthcheck)
    register(app, get_submissions)
    register(app, create_submission)
    register(app, update_submission)
    return app
