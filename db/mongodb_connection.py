from pymongo import MongoClient
from pymongo.collection import Collection
from os import getenv


class MongoDBConnection:
    _instance = None

    def __new__(cls):
        """
        Create a MongoDB connection instance following the singleton pattern
        """
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            cls._instance.MONGO_URI = getenv("MONGO_URI")
            cls._instance.MONGO_DB = getenv("MONGO_DB")
        return cls._instance

    @property
    def db(self):
        if self._db is None:
            raise Exception("Database not initialized. Call init_db first.")
        return self._db

    def init_collection(cls, collection: str) -> Collection:
        """
        Initialize a collection in a MongoDB database.

        Args:
            collection (str): The name of the collection to be initialized.

        Returns:
            Collection: The initialized collection in the MongoDB database.
        """
        mongo = MongoClient(cls.MONGO_URI)
        db = mongo[cls.MONGO_DB]
        return db[collection]
