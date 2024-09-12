from pydantic import BaseModel, Field
from pydantic.json_schema import JsonSchemaValue
from typing import Optional
from bson import ObjectId


class Job(BaseModel):
    title: str
    salary_month: int
    assigned_user: Optional[dict] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {"example": {"title": "Bus Driver", "salary_month": 10000}}
