from pymongo import MongoClient, IndexModel, ASCENDING, DESCENDING

class ModelMongo:
    def __init__(self, uri):
        self.client = MongoClient(uri)

    def build_index(self):
        raise NotImplementedError


class ModelRSS(ModelMongo):
    def __init__(self, uri, database='biasimpact', collection='rss_feed'):
        self.client = MongoClient(uri)
        self.database = self.client[database]
        self.collection = self.client[database][collection]
        self.build_index()

    def build_index(self):
        indexes_model = [
            IndexModel([("media", ASCENDING)]),
            IndexModel([("link", ASCENDING)], unique=True)
        ]
        self.collection.create_indexes(indexes_model)
