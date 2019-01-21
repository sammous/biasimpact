from pymongo import MongoClient, IndexModel, ASCENDING, DESCENDING

class ModelMongo:
    def __init__(self, uri, database, collection):
        self.client = MongoClient(uri)
        self.database = self.client[database]
        self.collection = self.client[database][collection]

    def build_index(self):
        raise NotImplementedError


class ModelRSS(ModelMongo):
    """
    Schema 
    raw_item: String
    date_article: Datetime
    desc: String
    title: String
    link: String
    date_parsed: Datetime
    media: String
    """
    def __init__(self, uri, database='biasimpact', collection='rss_feed'):
        super().__init__(uri, database, collection)
        self.build_index()

    def build_index(self):
        indexes_model = [
            IndexModel([("media", ASCENDING)]),
            IndexModel([("link", ASCENDING)], unique=True)
        ]
        self.collection.create_indexes(indexes_model)

class ModelReport(ModelMongo):
    def __init__(self, uri, database='biasimpact', collection='reporting'):
        super().__init__(uri, database, collection)
        self.build_index()

    def build_index(self):
        indexes_model = [
            IndexModel([("date_report", ASCENDING)]),
            IndexModel([("media", ASCENDING)]),
            IndexModel([("success", ASCENDING)])
        ]
        self.collection.create_indexes(indexes_model)
