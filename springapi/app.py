from flask import Flask

import springapi.config as config_file
import argparse

from springapi.helpers import register
from springapi.routes.healthcheck import healthcheck


def get_env_name():
    environments = {
        'prod': 'ProductionConfig',
        'dev': 'DevelopmentConfig',
        'test': 'TestingConfig'
    }
    parser = argparse.ArgumentParser()
    parser.add_argument('--env',
                        default='prod',
                        choices=['dev', 'prod', 'test'],
                        help='runtime environment, default production')
    args = parser.parse_known_args()[0]
    conf_env = environments[args.env]
    return conf_env


def create_app():
    env = get_env_name()
    app = Flask(__name__)
    app.config.from_object(getattr(config_file, env))
    register(app, healthcheck)
    return app
