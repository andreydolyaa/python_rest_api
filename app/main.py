from fastapi import FastAPI

from app.database import db, client
from app.routes.users import router as user_routes
from app.routes.jobs import router as job_routes

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    print("Connected to MongoDB Database")


@app.on_event("shutdown")
def shutdown_db_client():
    client.close()


@app.get("/")
async def read_root():
    return {"message": "fastapi mongodb project"}


app.include_router(user_routes, tags=["Users"], prefix="/api")
app.include_router(job_routes, tags=["Jobs"], prefix="/api")


# run app
# uvicorn app.main:app --reload
