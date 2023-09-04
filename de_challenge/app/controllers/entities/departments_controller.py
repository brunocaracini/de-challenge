"-------------------------------Imports Section-------------------------------"

# Libraries
from fastapi.responses import Response

# Local Dependencies
from app.controllers.controller import Controller
from app.database.entities.departments import Department as DepartmentData


class DepartmentController(Controller):
    @staticmethod
    async def batch_from_csv(file: bytes, headers: list[str]):
        departments = await DepartmentController.read_csv_reader(file=file, headers=headers)
        return await DepartmentData.insert_many(departments=departments)

    @staticmethod
    async def insert_many(departments: list[dict]):
        departments = [{**obj.__dict__} for obj in departments]
        return await DepartmentData.insert_many(departments=departments)