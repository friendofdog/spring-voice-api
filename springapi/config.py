class Configuration(object):

    def __init__(self, firebase):
        self.firebase = firebase


"""
class Config(object):
    DEBUG = False
    ENV = 'production'
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'


class TestingConfig(Config):
    TESTING = True
"""
