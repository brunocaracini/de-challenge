from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db_connection import BASE,ENGINE, SESSION
from datetime import datetime

class Job(BASE):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    @staticmethod
    async def insert_one(job: dict):
        pass

    @staticmethod
    async def insert_many(jobs: list[dict]):
        pass