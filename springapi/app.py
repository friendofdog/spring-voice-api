from flask import Flask

import springapi.config as config_file

from springapi.helpers import register
from springapi.routes.healthcheck import healthcheck
from springapi.routes.submissions import get_submissions


def create_app(configuration):
    app = Flask(__name__)
    # app.config.from_object(getattr(config_file, env))
    register(app, healthcheck)
    register(app, get_submissions)
    return app
