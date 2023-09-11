"-------------------------------Imports Section-------------------------------"

# Libraries
from sqlalchemy import Column, Integer, String

# Local Dependencies
from app.database.db_connection import BaseDBModel, BASE, ENGINE


class Department(BaseDBModel, BASE):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    department = Column(String, unique=True)

    @classmethod
    def delete_table(cls):
        cls.metadata.drop_all(ENGINE)

    @classmethod
    def __create_table__(cls):
        cls.metadata.create_all(ENGINE)

    @classmethod
    async def insert_many(cls, departments):
        return await super().insert_many(entities=departments, model_class=cls)
    