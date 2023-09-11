"-------------------------------Imports Section-------------------------------"

# Libraries
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String

# Local Dependencies
from app.database.db_connection import BaseDBModel, BASE, ENGINE


class Job(BaseDBModel, BASE):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job = Column(String, unique=True)

    @classmethod
    def delete_table(cls):
        cls.metadata.drop_all(ENGINE)

    @classmethod
    def __create_table__(cls):
        cls.metadata.create_all(ENGINE)

    @classmethod
    async def insert_many(cls, jobs, db: Session):
        return await super().insert_many(entities=jobs, model_class=cls, db=db)
