"-------------------------------Imports Section-------------------------------"

# Libraries
from sqlalchemy import Column, Integer, String

# Local Dependencies
from app.database.db_connection import BaseDBModel, BASE, ENGINE


class Department(BaseDBModel, BASE):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    department = Column(String, unique=True)

    @staticmethod
    def __delete_table__():
        BASE.metadata.tables["departments"].drop(ENGINE)

    @staticmethod
    def __create_table__():
        BASE.metadata.create_all(ENGINE)

    @staticmethod
    async def insert_many(departments):
        return await BaseDBModel.insert_many(entities=departments, model_class=Department)
    