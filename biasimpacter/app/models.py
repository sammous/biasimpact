from pymongo import MongoClient, IndexModel, ASCENDING, DESCENDING

class ModelMongo:
    def __init__(self, uri):
        self.client = MongoClient(uri)

    def build_index(self):
        raise NotImplementedError


class ModelRSS(ModelMongo):
    def build_index(self, collection):
        indexes_model = [
            IndexModel([("media", ASCENDING)]),
            IndexModel([("link", ASCENDING)], unique=True)
        ]
        self.client.database.collection.create_indexes(indexes_model)
