from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional


class User(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {"name": "John Doe", "email": "john@example.com", "age": 30}
        }
