import os
import firebase_admin as admin  # type: ignore

from flask import Flask

from springapi.config_helpers import (
    SUBMISSION, TOKEN, decode_json_uri, create_config)
from springapi.helpers import register
from springapi.models.firebase.client import authenticate_firebase
from springapi.models.sqlite import db
from springapi.routes.authorization import (
    request_auth_code, request_exchange_token)
from springapi.routes.healthcheck import healthcheck
from springapi.routes.submissions import (
    get_all, get_single, create_single, update_single)


def create_database_instance(config, model, app=None):
    database_uri = config[model]
    scheme, _ = decode_json_uri(database_uri)

    if scheme == "firebase":
        try:
            admin.get_app()
        except ValueError:
            authenticate_firebase(database_uri)
    elif scheme == "sqlite":
        app.config.from_mapping(
            TOKEN_DB=os.path.join(app.instance_path, f"token.{scheme}"))
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass
        db.init_app(app)
    else:
        raise ValueError(f"Unknown database protocol: {scheme}")


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
