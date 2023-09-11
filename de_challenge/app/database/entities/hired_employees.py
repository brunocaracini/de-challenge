"-------------------------------Imports Section-------------------------------"

# Libraries
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
    case,
    extract,
)
from sqlalchemy.orm import Session

# Local Dependencies
from app.database.entities.jobs import Job
from app.database.entities.departments import Department
from app.database.db_connection import BaseDBModel, BASE, ENGINE


class HiredEmployee(BaseDBModel, BASE):
    __tablename__ = "hired_employees"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    datetime = Column(DateTime, default=datetime.utcnow)
    department_id = Column(Integer, ForeignKey("departments.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    @classmethod
    def delete_table(cls):
        cls.metadata.drop_all(ENGINE)

    @classmethod
    def __create_table__(cls):
        cls.metadata.create_all(ENGINE)

    @classmethod
    async def insert_many(cls, hired_employees: list[dict], db: Session):
        return await super().insert_many(entities=hired_employees, model_class=cls, db=db)

    @classmethod
    async def get_by_job_and_department(cls, year: int, db: Session):
        quarter = extract("quarter", HiredEmployee.datetime)
        query = (
            db.query(
                Department.department.label("Department"),
                Job.job.label("Job"),
                func.sum(case((quarter == 1, 1), else_=0)).label("Q1"),
                func.sum(case((quarter == 2, 1), else_=0)).label("Q2"),
                func.sum(case((quarter == 3, 1), else_=0)).label("Q3"),
                func.sum(case((quarter == 4, 1), else_=0)).label("Q4"),
            )
            .join(Department, cls.department_id == Department.id)
            .join(Job, cls.job_id == Job.id)
            .filter(extract("year", cls.datetime) == year)
            .group_by(Department.department, Job.job)
            .order_by(Department.department, Job.job)
        )
        return [row._mapping for row in query.all()]

    @classmethod
    async def get_by_department_higher_than_year_mean(cls, year: int, db: Session):
        subquery = (
            db.query(
                Department.id.label("department_id"),
                func.count(cls.id).label("count"),
            )
            .join(cls, Department.id == cls.department_id)
            .filter(func.extract("year", cls.datetime) == year)
            .group_by(Department.id)
            .subquery()
        )

        # Main query to retrieve department information with hired employee counts
        query = (
            db.query(
                Department.id,
                Department.department,
                func.count(cls.id).label("hired"),
            )
            .join(cls, Department.id == cls.department_id)
            .filter(func.extract("year", cls.datetime) == year)
            .group_by(Department.id, Department.department)
            .having(
                func.count(cls.id)
                > db.query(
                    func.avg(subquery.c.count).label("mean_employees_hired")
                ).scalar()
            )
            .order_by(func.count(cls.id).desc())
        )

        return [row._mapping for row in query.all()]
