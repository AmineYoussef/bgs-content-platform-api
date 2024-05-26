from models.rating import *
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.collection import Collection, Cursor
from db.mongodb_connection import MongoDBConnection
from db.mongodb_helpers import *
from  models.content import *


class RatingManager:
    db: Collection = MongoDBConnection().init_collection("ratings")
    db_content: Collection = MongoDBConnection().init_collection("content")

    def get_content(cls, content_id: str) -> ContentModel | None:
        if not content_id:
            raise ValueError("content ID is required.")
        try:
            object_id = ObjectId(content_id)
        except (InvalidId, TypeError):
            return None
        content: Cursor = cls.db_content.find_one({"_id": object_id})
        return ContentModel(**content) if content is not None else None
    
    def get_rating(cls, rating_id: str) -> RatingModel | None:
        if not rating_id:
            raise ValueError("rating ID is required.")
        try:
            object_id = ObjectId(rating_id)
        except (InvalidId, TypeError):
            return None
        rating: Cursor = cls.db.find_one({"_id": object_id})
        return RatingModel(**rating) if rating is not None else None

    def get_ratings(
        cls, sort_direction, sort_by, page, page_size, filter_obj
    ) -> ListSuccessResponse:
        rating_list_cursor: Cursor = get_find_cursor(
            cls.db, filter_obj, sort_direction, sort_by, page, page_size
        )
        total_rating_list: int = get_find_cursor(cls.db, filter_obj).count()
        rating_list: List = [
            RatingModel(**doc).to_json() for doc in rating_list_cursor
        ]
        return format_response(
            rating_list, total_rating_list, sort_direction, sort_by, page, page_size
        )

    def add_rating(cls, rating: RatingInputModel) -> RatingModel:
        result = cls.db.insert_one(rating.dict())
        inserted_id = result.inserted_id
        inserted_rating = cls.db.find_one({"_id": inserted_id})
        inserted_rating["_id"] = str(inserted_rating["_id"])

        return RatingModel(**inserted_rating)

    def update_rating(
        cls, rating: Dict, rating_id: str
    ) -> RatingModel:
        try:
            object_id = ObjectId(rating_id)
        except (InvalidId, TypeError):
            return None
        cls.db.update_one({"_id": object_id}, {"$set": rating})
        updated_rating = cls.get_rating(rating_id)
        return updated_rating

    def delete_rating(cls, rating_id: str):
        try:
            object_id = ObjectId(rating_id)
        except (InvalidId, TypeError):
            return None
        return cls.db.delete_one({"_id": object_id})
