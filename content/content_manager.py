from models.content import *
from flask import jsonify
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.collection import Collection, Cursor
from db.mongodb_connection import MongoDBConnection
from db.mongodb_helpers import *
import re


class ContentManager:
    db: Collection = MongoDBConnection().init_collection("content")

    def get_content(cls, content_id: str) -> ContentModel | None:
        if not content_id:
            raise ValueError("content ID is required.")
        try:
            object_id = ObjectId(content_id)
        except (InvalidId, TypeError):
            return None
        content: Cursor = cls.db.find_one({"_id": object_id})
        return ContentModel(**content) if content is not None else None

    def get_content_filter_query(cls, filter_obj: ContentFilterModel) -> Dict:
        query = {}
        filter_obj = filter_obj.dict(exclude_none=True)
        if "title" in filter_obj:
            title = filter_obj["title"]
            query["title"] = {
                "$regex": f".*{re.escape(title)}.*",
                "$options": "i",
            }
        if "category" in filter_obj:
            query["category"] = filter_obj["category"]
        if "tags" in filter_obj:
            query["tags"] = {"$in": [tag for tag in filter_obj["tags"]]}
        return query

    def get_content_list(
        cls,
        sort_direction: Union[Literal[-1], Literal[1]],
        sort_by: str,
        page: int,
        page_size: int,
        filter_obj: ContentFilterModel,
    ) -> ListSuccessResponse:
        if filter_obj:
            filter_obj = cls.get_content_filter_query(filter_obj)
        content_list_cursor: Cursor = get_find_cursor(
            cls.db, filter_obj, sort_direction, sort_by, page, page_size
        )
        total_content_list: int = get_find_cursor(cls.db, filter_obj).count()
        content_list: List = [
            ContentModel(**doc).to_json() for doc in content_list_cursor
        ]
        return format_response(
            content_list, total_content_list, sort_direction, sort_by, page, page_size
        )

    def add_content(cls, content: ContentInputModel) -> ContentModel:
        result = cls.db.insert_one(content.dict())
        inserted_id = result.inserted_id
        inserted_content = cls.db.find_one({"_id": inserted_id})
        inserted_content["_id"] = str(inserted_content["_id"])
        return ContentModel(**inserted_content)

    def update_content(cls, content: Dict, content_id: str) -> ContentModel:
        object_id = ObjectId(content_id)
        cls.db.update_one({"_id": object_id}, {"$set": content})
        updated_content = cls.get_content(content_id)
        return updated_content

    def delete_content(cls, content_id: str):
        try:
            object_id = ObjectId(content_id)
        except (InvalidId, TypeError):
            return None
        return cls.db.delete_one({"_id": object_id})
