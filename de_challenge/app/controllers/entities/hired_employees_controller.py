"-------------------------------Imports Section-------------------------------"

# Libraries
from fastapi.responses import Response

# Local Dependencies
from app.controllers.controller import Controller
from app.database.entities.hired_employees import HiredEmployee as HiredEmployeeData


class HiredEmployeeController(Controller):
    
    @staticmethod
    async def batch_from_csv(file: bytes, headers: list[str]):
        hired_employees = await HiredEmployeeController.read_csv_reader(file=file, headers=headers)
        return await HiredEmployeeData.insert_many(hired_employees=hired_employees)

    @staticmethod
    async def insert_many(hired_employees: list[dict]):
        hired_employees = [{**obj.__dict__} for obj in hired_employees]
        return await HiredEmployeeData.insert_many(hired_employees=hired_employees)
    
    @staticmethod
    async def get_by_job_and_department(year: int):
        return await HiredEmployeeData.get_by_job_and_department(year=year)
    
    @staticmethod
    async def get_by_department_higher_than_year_mean(year: int):
        return await HiredEmployeeData.get_by_department_higher_than_year_mean(year=year)