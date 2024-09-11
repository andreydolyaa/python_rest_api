from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from typing import List
from pymongo.errors import PyMongoError

from app.database import db
from app.models.user import User
from app.models.jobs import Job
from app.utils.utils import parse_objectid


router = APIRouter()


@router.post("/users", response_description="Create a new user", response_model=User)
def create_new_user(user: User):
    try:
        user = jsonable_encoder(user)
        new_user = db["users"].insert_one(user)
        created_user = db["users"].find_one({"_id": new_user.inserted_id})
        return created_user
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database Error:{str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")


@router.get("/users", response_description="Get all users", response_model=List[User])
def get_all_users():
    try:
        users = db["users"].find()
        return users
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database Error:{str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")


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
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database Error:{str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")


@router.post("/users/job", response_description="Assign user to a job")
def assign_user_to_a_job(data: dict):
    # {'user_id': '123', 'job_id': 'ooo1'}
    job_id = ObjectId(data["job_id"])
    job = jsonable_encoder(db["jobs"].find({"_id": job_id}))
    # print(job)
    return JSONResponse(content={"message": "bla bla"}, status_code=200)


# return JSONResponse(content={"message": "bla bla"}, status_code=200)
