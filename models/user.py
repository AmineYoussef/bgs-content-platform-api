from pydantic import BaseModel, Field, validator, EmailStr
from models.py_object_id import PyObjectId
from typing import Optional
from bson import ObjectId
from fastapi.encoders import jsonable_encoder


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: str
    password: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
    
    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

class UserInputModel(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        regex="^[a-zA-Z0-9_]+$",
        description="Username must be between 3 and 50 characters long, and contain only letters, numbers, and underscores.",
    )
    email: EmailStr
    password: str = Field(
        ..., min_length=8, description="Password must be at least 8 characters long."
    )


    @validator("password")
    def validate_password(cls, value: str) -> str:
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter.")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/`~" for char in value):
            raise ValueError("Password must contain at least one special character.")
        return value

class UserCredentials(BaseModel):
    email: EmailStr
    password: str