from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from models.py_object_id import PyObjectId, ObjectId
from fastapi.encoders import jsonable_encoder

class ContentModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(..., description="Title of the content item")
    description: str = Field(..., description="Description of the content item")
    category: str = Field(..., description="Category of the content (game, video, artwork, music)")
    thumbnail_url: Optional[str] = Field(default=None, description="URL of the content's thumbnail image")
    content_url: str = Field(..., description="URL of the actual content")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp of content creation")
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
    
    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
    
class ContentInputModel(BaseModel):
    title: str = Field(..., description="Title of the content item")
    description: str = Field(..., description="Description of the content item")
    category: str = Field(..., description="Category of the content (game, video, artwork, music)")
    thumbnail_url: Optional[str] = Field(default=None, description="URL of the content's thumbnail image")
    content_url: str = Field(..., description="URL of the actual content")

    @validator("category")
    def validate_password(cls, value: str) -> str:
        if value not in ["game", "video", "artwork", "music"]:
            raise ValueError("category must be one of the following values: game | video | artwork | music")
        return value
    
class PartialContentModel(BaseModel):
    title: Optional[str] = Field(default=None, description="Title of the content item")
    description: Optional[str] = Field(default=None, description="Description of the content item")
    category: Optional[str] = Field(default=None, description="Category of the content (game, video, artwork, music)")
    thumbnail_url: Optional[str] = Field(default=None, description="URL of the content's thumbnail image")
    content_url: Optional[str] = Field(default=None, description="URL of the actual content")

    @validator("category")
    def validate_password(cls, value: str) -> str:
        if value not in ["game", "video", "artwork", "music"]:
            raise ValueError("category must be one of the following values: game | video | artwork | music")
        return value
    