import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from app.lib.config import Settings

class MongoDBConnection:
    def __init__(self):
        url = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
        self.client = MongoClient(url)
        self.client.admin.command('ping')

    def execute_query(self, query):
        return self.client[query]

# Initialize a singleton instance
mdb_conn = MongoDBConnection()
