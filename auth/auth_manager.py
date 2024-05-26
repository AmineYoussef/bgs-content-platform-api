from models.user import *
from pymongo.collection import Collection
from db.mongodb_connection import MongoDBConnection
from werkzeug.security import generate_password_hash, check_password_hash


class AuthManager:
    db: Collection = MongoDBConnection().init_collection("users")

    def register_user(cls, user_input: UserInputModel) -> UserModel:
        user_input.password = generate_password_hash(user_input.password)
        result = cls.db.insert_one(user_input.dict())
        inserted_id = result.inserted_id
        inserted_user = cls.db.find_one({"_id": inserted_id})
        inserted_user["_id"] = str(inserted_user["_id"])
        return UserModel(**inserted_user)

    def verify_duplicate_email(cls, email: str) -> bool:
        user_count: int = cls.db.count_documents({"email": email})
        return user_count > 0

    def verify_duplicate_username(cls, username: str) -> bool:
        user_count: int = cls.db.count_documents({"username": username})
        return user_count > 0

    def login(cls, email: str, password: str) -> UserModel:
        user = cls.db.find_one({"email": email})
        if not user or not check_password_hash(user["password"], password):
            return None
        return user
