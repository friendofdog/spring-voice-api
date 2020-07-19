from flask import Flask

from springapi.helpers import register
from springapi.routes.healthcheck import healthcheck


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    register(app, healthcheck)
    return app
