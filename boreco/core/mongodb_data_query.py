from pymongo import MongoClient


class DataBaseMongo(MongoClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = MongoClient(
            'mongodb://divisor:0l6YIeoLMjL4yEpQ@104.40.187.114:27017/divisor?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false')
        self.database = self.client.get_default_database()

    def load_from_db(self, collection):
        return self.database.get_collection(collection)
