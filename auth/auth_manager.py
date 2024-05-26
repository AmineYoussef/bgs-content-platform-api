from models.user import *
from flask import jsonify
from pymongo.collection import Collection
from db.mongodb_connection import MongoDBConnection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity


class AuthManager:
    db: Collection = MongoDBConnection().init_collection("users")

    def register_user(cls, user_input: UserInputModel) -> UserModel:
        username_exists = cls.verify_duplicate_username(user_input.username)
        if username_exists:
            raise ValueError("Username already taken")
        email_exists = cls.verify_duplicate_email(user_input.email)
        if email_exists:
            raise ValueError("Email already taken")
        
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

    def login(cls, login: str, password: str) -> UserModel:
        if get_jwt_identity is not None:
            cls.logout()
        user = cls.db.find_one({"$or": [{"username": login}, {"email": login}]})
        if not user or not check_password_hash(user["password"], password):
            raise ValueError("Incorrect login or password")
        user = UserModel(**user).to_json()
        access_token = create_access_token(identity=user["_id"])
        response = jsonify({"token": access_token})
        set_access_cookies(response, access_token)
        return response
    
    def logout(cls):
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return response
