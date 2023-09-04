"-------------------------------Imports Section-------------------------------"

# Libraries
from fastapi.responses import Response

# Local Dependencies
from app.controllers.controller import Controller
from app.database.entities.jobs import Job as JobData


class JobController(Controller):
    @staticmethod
    async def batch_from_csv(file: bytes, headers: list[str]):
        jobs = await JobController.read_csv_reader(file=file, headers=headers)
        return await JobData.insert_many(jobs=jobs)

    @staticmethod
    async def insert_many(jobs: list[dict]):
        jobs = [{**obj.__dict__} for obj in jobs]
        return await JobData.insert_many(jobs=jobs)