from app.prepare import Date, Validator, RSSReader
from flask import Flask
from flask_restplus import Resource, Api
import pyrebase


def create_app(test_config=False):
    app = Flask(__name__)
    if test_config:
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.ProductionConfig')

    firebase_config = {
        "apiKey": app.config['FIREBASE_APIKEY'],
        "authDomain": app.config['FIREBASE_AUTHDOMAIN'],
        "storageBucket": app.config['FIREBASE_STORAGEBUCKET'],
        "databaseURL": app.config['FIREBASE_DATABASEURL'],
        "projectId": app.config['FIREBASE_PROJECTID']
    }
    firebase = pyrebase.initialize_app(firebase_config)
    storage = firebase.storage()

    return app

