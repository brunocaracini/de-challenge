"-------------------------------Imports Section-------------------------------"

# Libraries
from fastapi import APIRouter

# Local Dependencies
from app.database.db_connection import BaseDBModel

router = APIRouter(tags=["Health"])


@router.get("/")
async def app_health():
    return "App is up and running :)"


@router.get("/db-health/")
async def database_health():
    with BaseDBModel.session_factory() as session:
        session.connection()
        session.close()
        return "Database is up and running :)"
