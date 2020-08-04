from flask import Flask

from springapi.helpers import register
from springapi.models.firebase.app import authenticate
from springapi.routes.healthcheck import healthcheck
from springapi.routes.submissions import \
    db_get_submissions,\
    db_get_submission,\
    db_create_submission,\
    db_update_submission


def create_app():
    app = Flask(__name__)
    register(app, healthcheck)
    register(app, db_get_submissions)
    register(app, db_get_submission)
    register(app, db_create_submission)
    register(app, db_update_submission)
    return app


def main():
    authenticate()
    app = create_app()
    app.run()


if __name__ == "__main__":
    main()
