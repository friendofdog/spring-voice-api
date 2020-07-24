from flask import Flask

from springapi.helpers import register
from springapi.routes.healthcheck import healthcheck
from springapi.routes.submissions import get_submissions


def create_app():
    app = Flask(__name__)
    register(app, healthcheck)
    register(app, get_submissions)
    return app
