import os

from flask import Flask

from springapi.config_helpers import decode_json_uri
from springapi.helpers import register
from springapi.models.firebase.app import authenticate
from springapi.routes.healthcheck import healthcheck
import springapi.routes.submissions as submissions


def create_database_instance(config):
    database_uri = config["DATABASE_URI"]
    scheme, _ = decode_json_uri(database_uri)

    if scheme == "firestore":
        return authenticate(database_uri)
    else:
        raise ValueError(f"Unknown database protocol: {scheme}")


def create_app(config):
    config.setdefault("ENV", config.get("FLASK_ENV", "testing"))
    config.setdefault("DEBUG", config["ENV"] == "development")

    app = Flask(__name__)

    for key, value in config.items():
        app.config[key] = value

    register(app, healthcheck)
    register(app, submissions.get_all)
    register(app, submissions.get_single)
    register(app, submissions.create_single)
    register(app, submissions.update_single)
    return app


def main(environ):
    app = create_app(environ)
    create_database_instance(environ)
    app.run()


if __name__ == "__main__":
    main(os.environ.copy())
