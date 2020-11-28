import os

from flask import Flask

from springapi.config_helpers import (
    SUBMISSION, TOKEN, create_config, create_database_instance)
from springapi.routes.authorization import (
    request_auth_code, request_exchange_token)
from springapi.routes.healthcheck import healthcheck
from springapi.routes.helpers import register
from springapi.routes.submissions import (
    get_all, get_single, create_single, update_single)


def create_app(config):
    app = Flask(__name__)

    for key, value in config.items():
        app.config[key] = value

    register(app, healthcheck)
    register(app, get_all)
    register(app, get_single)
    register(app, create_single)
    register(app, update_single)
    register(app, request_auth_code)
    register(app, request_exchange_token)

    create_database_instance(config, TOKEN, app)

    return app


def main(environ):
    config = create_config(environ)
    app = create_app(config)
    create_database_instance(environ, SUBMISSION)
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main(os.environ.copy())
