"-------------------------------Imports Section-------------------------------"

# Libraries
from sqlalchemy.orm import Session
from fastapi.responses import Response

# Local Dependencies
from app.resources.utils import Utils
from app.controllers.controller import Controller
from app.database.entities.jobs import Job as JobData


class JobController(Controller):
    
    @staticmethod
    async def batch_from_csv(
        file: bytes, first_row_headers: bool, headers: list[str], db: Session
    ):
        allowed_headers = (
            Utils.get_class_variables_from_object(JobData)
            if first_row_headers
            else None
        )
        jobs = await JobController.read_csv_reader(
            file=file, headers=headers, allowed_headers=allowed_headers
        )
        return await JobData.insert_many(jobs=jobs, db=db)

    @staticmethod
    async def insert_many(jobs: list[dict], db: Session):
        jobs = [{**obj.__dict__} for obj in jobs]
        return await JobData.insert_many(jobs=jobs, db=db)
