from flask import Flask

from springapi.helpers import register
from springapi.models.firebase.app import authenticate
from springapi.routes.healthcheck import healthcheck
import springapi.routes.submissions as submissions


def create_app():
    app = Flask(__name__)
    register(app, healthcheck)
    register(app, submissions.get_all)
    register(app, submissions.get_single)
    register(app, submissions.create_single)
    register(app, submissions.update_single)
    return app


def main():
    authenticate()
    app = create_app()
    app.run()


if __name__ == "__main__":
    main()
