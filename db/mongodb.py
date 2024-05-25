from pymongo import MongoClient
from pymongo.collection import Collection


class MongoDBConfiguration:

    def init_db(self, uri: str, db: str) : 
        """
        Initialize MongoDB configuration

        Args:
            uri (str): The name of the collection to be initialized.
            db (str): The name of the database to be initialized.
        """
        self.MONGO_URI = uri
        self.MONGO_DB = db
        return self
    def init_collection(collection: str) -> Collection:
        """
        Initialize a collection in a MongoDB database.

        Args:
            collection (str): The name of the collection to be initialized.

        Returns:
            Collection: The initialized collection in the MongoDB database.
        """
        mongo = MongoClient(MongoDBConfiguration.MONGO_URI)
        db = mongo[MongoDBConfiguration.MONGO_DB]
        return db[collection]
