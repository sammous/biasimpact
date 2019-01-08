class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    FIREBASE_PROJECTID = "projectId"
    FIREBASE_APIKEY = "apiKey"
    FIREBASE_AUTHDOMAIN = "{}.firebaseapp.com".format(FIREBASE_PROJECTID)
    FIREBASE_DATABASEURL = "https://databaseName.firebaseio.com"
    FIREBASE_STORAGEBUCKET = "projectId.appspot.com"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    FIREBASE_PROJECTID = "projectId"
    FIREBASE_APIKEY = "XXX"
    FIREBASE_AUTHDOMAIN = "{}.firebaseapp.com".format(FIREBASE_PROJECTID)
    FIREBASE_DATABASEURL = "https://databaseName.firebaseio.com"
    FIREBASE_STORAGEBUCKET = "projectId.appspot.com"
