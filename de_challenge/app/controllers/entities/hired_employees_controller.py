"-------------------------------Imports Section-------------------------------"

# Libraries
from sqlalchemy.orm import Session
from fastapi.responses import Response

# Local Dependencies
from app.resources.utils import Utils
from app.controllers.controller import Controller
from app.database.entities.hired_employees import HiredEmployee as HiredEmployeeData


class HiredEmployeeController(Controller):
    
    @staticmethod
    async def batch_from_csv(
        file: bytes, first_row_headers: bool, headers: list[str], db: Session
    ):
        allowed_headers = (
            Utils.get_class_variables_from_object(HiredEmployeeData)
            if first_row_headers
            else None
        )
        hired_employees = await HiredEmployeeController.read_csv_reader(
            file=file, headers=headers, allowed_headers=allowed_headers
        )
        return await HiredEmployeeData.insert_many(hired_employees=hired_employees, db=db)

    @staticmethod
    async def insert_many(hired_employees: list[dict], db: Session):
        hired_employees = [{**obj.__dict__} for obj in hired_employees]
        return await HiredEmployeeData.insert_many(hired_employees=hired_employees, db=db)

    @staticmethod
    async def get_by_job_and_department(year: int, db: Session):
        return await HiredEmployeeData.get_by_job_and_department(year=year, db=db)

    @staticmethod
    async def get_by_department_higher_than_year_mean(year: int, db: Session):
        return await HiredEmployeeData.get_by_department_higher_than_year_mean(
            year=year, db=db
        )
