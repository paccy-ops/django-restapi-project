from core.mongodb_data_query import DataBaseMongo


class MongoData:
    def __init__(self):
        self.database = DataBaseMongo()
        self.data = []

    def get_client_data(self, collection, limit=0):
        for data in self.database.load_from_db(collection).find().limit(limit):
            yield data
