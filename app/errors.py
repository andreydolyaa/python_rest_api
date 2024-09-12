from fastapi import HTTPException
from pymongo.errors import PyMongoError


def handle_database_error(e: Exception):
    if isinstance(e, PyMongoError):
        return HTTPException(status_code=500, detail=f"Database Error:{str(e)}")
    return HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")
