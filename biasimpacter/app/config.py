class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    PROD = True


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
