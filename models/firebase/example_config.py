class Config(object):
    PROJECT_ID = 'prod-project-id'
    CREDENTIALS_FILE = 'credentials.json'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    PROJECT_ID = 'dev-project-id'
    CREDENTIALS_FILE = 'credentials-dev.json'


class TestingConfig(Config):
    pass
