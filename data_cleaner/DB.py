from pymongo import MongoClient
from bson import ObjectId

def json_serial(obj):
        """JSONエンコードのためのヘルパー関数"""
        if isinstance(obj, ObjectId):
            return str(obj)
        raise TypeError(f"Type {obj.__class__.__name__} not serializable")

class MongoDBHandler:
    def __init__(self, host='localhost', port=27017, db_name='school_schedule_db'):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]

    def insert_to_mongodb(self, json_data, collection_name):
        collection = self.db[collection_name]
        collection.insert_many(json_data)
        print(f"MongoDBにデータを挿入しました: {collection_name}")

    def close(self):
        self.client.close()

    