"-------------------------------Imports Section-------------------------------"

# Libraries
from sqlalchemy import Column, Integer, String

# Local Dependencies
from app.database.db_connection import BaseDBModel, BASE, ENGINE


class Job(BaseDBModel, BASE):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job = Column(String, unique=True)

    @staticmethod
    def __delete_table__():
        BASE.metadata.tables["jobs"].drop(ENGINE)

    @staticmethod
    def __create_table__():
        BASE.metadata.create_all(ENGINE)

    @staticmethod
    async def insert_many(jobs):
        return await BaseDBModel.insert_many(entities=jobs, model_class=Job)
