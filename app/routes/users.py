from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from typing import List
from pymongo.errors import PyMongoError
from pymongo import ReturnDocument

from app.database import db
from app.models.user import User
from app.models.jobs import Job
from app.utils.utils import parse_objectid
from app.errors import handle_database_error


router = APIRouter()


@router.post("/users", response_description="Create a new user", response_model=User)
def create_new_user(user: User):
    try:
        user = jsonable_encoder(user)
        new_user = db["users"].insert_one(user)
        return db["users"].find_one({"_id": new_user.inserted_id})
    except Exception as e:
        raise handle_database_error(e)


@router.get("/users", response_description="Get all users", response_model=List[User])
def get_all_users():
    try:
        return db["users"].find()
    except Exception as e:
        raise handle_database_error(e)


@router.get(
    "/users/{user_name}", response_description="Get user by name", response_model=User
)
def get_user_by_name(user_name: str):
    try:
        user_name = jsonable_encoder(user_name)
        regex = {"$regex": user_name, "$options": "i"}
        user = db["users"].find_one({"name": regex})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            parse_objectid(user)
        return jsonable_encoder(user)
    except Exception as e:
        raise handle_database_error(e)


@router.post(
    "/users/job", response_description="Assign user to a job", response_model=Job
)
def assign_user_to_a_job(data: dict):
    try:
        job = db["jobs"].find_one({"_id": ObjectId(data["job_id"])})
        user = db["users"].find_one({"_id": ObjectId(data["user_id"])})
        if not job or not user:
            raise HTTPException(status_code=404, detail="Wrong job/user id")

        job = parse_objectid(job)
        user = parse_objectid(user)

        updated_job = db["jobs"].find_one_and_update(
            {"_id": ObjectId(job["_id"])},
            {"$set": {"assigned_user": user}},
            return_document=ReturnDocument.AFTER,
        )
        if not updated_job:
            raise HTTPException(status_code=500, detail="Failed to assign user to job")

        return updated_job

    except Exception as e:
        raise handle_database_error(e)


# return JSONResponse(content={"message": "bla bla"}, status_code=200)
