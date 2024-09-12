from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo import ReturnDocument
from bson.objectid import ObjectId

from app.database import db
from app.models.jobs import Job
from app.errors import handle_database_error

router = APIRouter()


@router.post("/jobs", response_description="Create new job", response_model=Job)
def create_new_job(job: Job):
    try:
        job = jsonable_encoder(job)
        new_job = db["jobs"].insert_one(job)
        return db["jobs"].find_one({"_id": new_job.inserted_id})
    except Exception as e:
        raise handle_database_error(e)


@router.put(
    "/jobs/release/{job_id}",
    response_description="Remove user from a job",
    response_model=Job,
)
def remove_user_from_job(job_id: str):
    try:
        return db["jobs"].find_one_and_update(
            {"_id": ObjectId(job_id)},
            {"$set": {"assigned_user": None}},
            return_document=ReturnDocument.AFTER,
        )
    except Exception as e:
        raise handle_database_error(e)


# return JSONResponse(content={"message": "bla bla"}, status_code=200)
