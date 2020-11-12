import os
import firebase_admin as admin  # type: ignore

from flask import Flask

from springapi.config_helpers import decode_json_uri
from springapi.helpers import AUTH, USERS, TOKEN, register
from springapi.models.firebase.authenticate import authenticate_firebase
from springapi.models.sqlite import db
from springapi.routes.authorization import (
    request_auth_code, request_exchange_token)
from springapi.routes.healthcheck import healthcheck
from springapi.routes.submissions import (
    get_all, get_single, create_single, update_single)


def create_database_instance(config):
    database_uri = config["DATABASE_URI"]
    scheme, _ = decode_json_uri(database_uri)

    if scheme == "firestore":
        return authenticate_firebase(database_uri)
    else:
        raise ValueError(f"Unknown database protocol: {scheme}")


def create_user_database_instance(config):
    database_uri = config["USERS"]
    scheme, _ = decode_json_uri(database_uri)

    if scheme == "firebase":
        if not admin.get_app():
            return authenticate_firebase(database_uri)
        else:
            return "Skipping user database instantiation. "\
                   f"{scheme} database instance already created"
    else:
        raise ValueError(f"Unknown user database protocol: {scheme}")


def verify_auth_credentials(config):
    auth_uri = config[AUTH]
    scheme, _ = decode_json_uri(auth_uri)

    if scheme == "google":
        pass
    else:
        raise ValueError(f"Unknown authorization protocol: {scheme}")


def create_token_database_instance(config, app):
    scheme = config[TOKEN]

    if scheme == "sqlite":
        app.config.from_mapping(
            TOKEN_DB=os.path.join(app.instance_path, f"token.{scheme}"))

        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        db.init_app(app)
    else:
        raise ValueError(f"Unknown token database protocol: {scheme}")


def create_app(config):
    config.setdefault("ENV", config.get("FLASK_ENV", "testing"))
    config.setdefault("DEBUG", config["ENV"] == "development")
    assert AUTH in config
    assert USERS in config
    assert TOKEN in config

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

    create_token_database_instance(config, app)

    return app


def main(environ):
    app = create_app(environ)
    create_database_instance(environ)
    create_user_database_instance(environ)
    verify_auth_credentials(environ)
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main(os.environ.copy())
