from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models.py_object_id import PyObjectId, ObjectId
from fastapi.encoders import jsonable_encoder


class RatingModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    content_id: Optional[str]
    user_id: Optional[str]
    rating: Optional[int]
    comment: Optional[str]
    created_at: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)


class RatingInputModel(BaseModel):
    content_id: str = Field(..., description="Content ID")
    user_id: str = Field(..., description="User ID")
    rating: int = Field(..., description="Rating value between 1 and 5", ge=1, le=5)
    comment: Optional[str] = Field(description="Comment attributed to the rating")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Timestamp of rating creation"
    )


class PartialRatingModel(BaseModel):
    rating: int = Field(..., description="Rating value between 1 and 5", ge=1, le=5)
    comment: Optional[str] = Field(description="Comment attributed to the rating")