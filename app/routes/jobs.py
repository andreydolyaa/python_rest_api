from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.database import db
from app.models.jobs import Job

router = APIRouter()


@router.post("/jobs", response_description="Create new job", response_model=Job)
def create_new_job(job: Job):
    try:
        job = jsonable_encoder(job)
        new_job = db["jobs"].insert_one(job)
        created_job = db["jobs"].find_one({"_id": new_job.inserted_id})
        return created_job
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database Error:{str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")
