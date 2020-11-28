import firebase_admin as admin  # type: ignore
import os

from springapi.helpers import decode_json_uri
from springapi.models.firebase.client import authenticate_firebase
from springapi.models.sqlite import db


AUTH = "AUTH"
CLIENT_ID = "CLIENT_ID"
KEY = "KEY"
SUBMISSION = "SUBMISSION"
TOKEN = "TOKEN"
VERSION = "v1"


def _verify_auth_credentials(config):
    auth_uri = config[AUTH]
    scheme, credentials = decode_json_uri(auth_uri)

    if scheme == "google":
        pass
    else:
        raise ValueError(f"Unknown authorization protocol: {scheme}")

    return credentials


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


def create_config(environ):
    config = {}
    config["ENV"] = environ.get("FLASK_ENV", "testing")
    config["DEBUG"] = config["ENV"] == "development"

    assert AUTH in environ
    assert KEY in environ
    assert SUBMISSION in environ
    assert TOKEN in environ

    auth_credentials = _verify_auth_credentials(environ)
    config[AUTH] = auth_credentials
    config[KEY] = environ[KEY]
    config[TOKEN] = environ[TOKEN]

    assert "web" in config[AUTH]
    assert "client_id" in config[AUTH]["web"]

    config[CLIENT_ID] = config[AUTH]["web"]["client_id"]
    return config
