from pydantic import BaseModel
from typing import Optional

class Job(BaseModel):
    title: str
    salary_month: int
    assigned_user: Optional[str] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {"example": {"title": "Bus Driver", "salary_month": 10000}}
