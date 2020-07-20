from models.firebase.app import authenticate
from springapi.app import create_app
import argparse


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
    environment = environments[args.env]
    return environment


if __name__ == '__main__':
    env = get_env_name()
    authenticate(env)
    app = create_app(env)
    app.run()
