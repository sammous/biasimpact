from dataprovider import Date, Validator, RSSReader, StoryRSS
from models import ModelRSS
from threading import Thread
import logging
import schedule
import time
import json
import os


logging.basicConfig(filename=os.getenv("BIASIMPACTER_OUTPUT"), 
                    level=logging.INFO, 
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())


def set_up_mongo():
    try:
        mongo_host = os.getenv("BIASIMPACTER_DC_MONGO_HOST")
        mongo_port = os.getenv("MONGO_PORT")
        mongo_db = os.getenv("APP_MONGO_DB")
        mongo_user = os.getenv("APP_MONGO_USER")
        mongo_pw = os.getenv("APP_MONGO_PASS")
        mongo_uri = "mongodb://{}:{}@{}:{}/{}".format(
            mongo_user, mongo_pw, mongo_host, mongo_port, mongo_db)
        logging.info(mongo_uri)
        return  mongo_uri
    except Exception() as e:
        logging.error(e)

def read_source(datapath=os.path.join(os.path.dirname(os.path.dirname(__file__)), "source.txt")):
    with open(datapath, 'r') as f:
        return [line.rstrip().split(", ") for line in f]

if __name__ == "__main__":
    uri = set_up_mongo()
    mongo_rss = ModelRSS(uri)
    urls = read_source()
    for name, url in urls:
        try:
            logging.info("Reading story: {}".format(name))
            story = StoryRSS(name, url, mongo_rss)
            story.save_story()
        except Exception as e:
            logging.error(e)
