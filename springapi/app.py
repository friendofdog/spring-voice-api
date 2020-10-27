import os

from flask import Flask

from springapi.config_helpers import decode_json_uri
from springapi.helpers import TOKENS, AUTH, USERS, register
from springapi.models.firebase.authenticate import authenticate_firebase
from springapi.models.users import get_users
from springapi.routes.healthcheck import healthcheck
from springapi.routes.submissions import (
    get_all, get_single, create_single, update_single)
from springapi.routes.authorization import (
    request_auth_code, request_exchange_token)


def create_database_instance(config):
    database_uri = config["DATABASE_URI"]
    scheme, _ = decode_json_uri(database_uri)

    if scheme == "firestore":
        return authenticate_firebase(database_uri)
    else:
        raise ValueError(f"Unknown database protocol: {scheme}")


def get_authorized_users(config):
    user_db_uri = config["USERS"]
    scheme, _ = decode_json_uri(user_db_uri)

    return get_users(scheme, user_db_uri)


def get_auth_credentials(config):
    auth_uri = config[AUTH]
    scheme, json = decode_json_uri(auth_uri)

    if scheme == "google":
        pass
    else:
        raise ValueError(f"Unknown authorization protocol: {scheme}")


def create_app(config):
    config.setdefault("ENV", config.get("FLASK_ENV", "testing"))
    config.setdefault("DEBUG", config["ENV"] == "development")
    assert TOKENS in config
    assert AUTH in config
    assert USERS in config

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
    return app


def main(environ):
    app = create_app(environ)
    create_database_instance(environ)
    users = get_authorized_users(environ)
    print(users)
    get_auth_credentials(environ)
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main(os.environ.copy())
