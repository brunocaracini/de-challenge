"-------------------------------Imports Section-------------------------------"

# Libraries
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

# Local Dependencies
from app.database.db_connection import BaseDBModel, BASE, ENGINE


class HiredEmployee(BaseDBModel, BASE):
    __tablename__ = "hired_employees"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    datetime = Column(DateTime, default=datetime.utcnow)
    department_id = Column(Integer, ForeignKey('departments.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))

    @staticmethod
    def __delete_table__():
        BASE.metadata.tables["hired_employees"].drop(ENGINE)

    @staticmethod
    def __create_table__():
        BASE.metadata.create_all(ENGINE)

    @staticmethod
    async def insert_many(hired_employees):
        return await BaseDBModel.insert_many(entities=hired_employees, model_class=HiredEmployee)