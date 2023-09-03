from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db_connection import BASE,ENGINE, SESSION
from datetime import datetime

class HiredEmployee(BASE):
    __tablename__ = "hired_employees"

    @staticmethod
    async def insert_one(hired_employee: dict):
        pass

    @staticmethod
    async def insert_many(hired_employees: list[dict]):
        pass