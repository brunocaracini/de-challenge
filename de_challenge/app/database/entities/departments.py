from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db_connection import BASE,ENGINE, SESSION
from datetime import datetime

class Department(BASE):
    __tablename__ = "departments"

    @staticmethod
    async def insert_one(department: dict):
        pass

    @staticmethod
    async def insert_many(departments: list[dict]):
        pass
    