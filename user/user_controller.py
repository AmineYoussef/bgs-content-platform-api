from models.user import UserModel
from bson import ObjectId
from pymongo.collection import Collection, Cursor
from db.mongodb_connection import MongoDBConnection
from db.mongodb_helpers import *


class UserController:
    db: Collection = MongoDBConnection().init_collection("users")

    def __init__(self):
        return super(UserController, self).__init__()

    def get_user(self, user_id: str) -> UserModel | None:
        if not user_id:
            raise ValueError("User ID is required.")

        object_id = ObjectId(user_id)
        user: Cursor = self.db.find_one({"_id": object_id})
        return UserModel(**user) if user is not None else None

    def get_users(self, sort_direction, sort_by, page, page_size, filter_obj):
        users_cursor: Cursor = get_find_cursor(
            self.db, filter_obj, sort_direction, sort_by, page, page_size
        )
        total_users: int = get_find_cursor(self.db, filter_obj).count()
        users: List = [UserModel(**doc).to_json() for doc in users_cursor]

        return format_response(
            users, total_users, sort_direction, sort_by, page, page_size
        )
