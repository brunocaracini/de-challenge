"-------------------------------Imports Section-------------------------------"

# Libraries
from sqlalchemy.orm import Session
from fastapi.responses import Response

# Local Dependencies
from app.resources.utils import Utils
from app.controllers.controller import Controller
from app.database.entities.departments import Department as DepartmentData


class DepartmentController(Controller):
    
    @staticmethod
    async def batch_from_csv(
        file: bytes, first_row_headers: bool, headers: list[str], db: Session
    ):
        allowed_headers = (
            Utils.get_class_variables_from_object(DepartmentData)
            if first_row_headers
            else None
        )
        departments = await DepartmentController.read_csv_reader(
            file=file, headers=headers, allowed_headers=allowed_headers
        )
        return await DepartmentData.insert_many(departments=departments, db=db)

    @staticmethod
    async def insert_many(departments: list[dict], db: Session):
        departments = [{**obj.__dict__} for obj in departments]
        return await DepartmentData.insert_many(departments=departments, db=db)
