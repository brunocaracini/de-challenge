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

    @staticmethod
    def __delete_table__():
        BASE.metadata.tables["hired_employees"].drop(ENGINE)

    @staticmethod
    def __create_table__():
        BASE.metadata.create_all(ENGINE)

    @staticmethod
    async def insert_many(hired_employees: list[dict]):
        return await BaseDBModel.insert_many(
            entities=hired_employees, model_class=HiredEmployee
        )

    @staticmethod
    async def get_by_job_and_department(year: int):
        session = BaseDBModel.session_factory()
        quarter = extract("quarter", HiredEmployee.datetime)

        query = (
            session.query(
                Department.department.label("Department"),
                Job.job.label("Job"),
                func.sum(case((quarter == 1, 1), else_=0)).label("Q1"),
                func.sum(case((quarter == 2, 1), else_=0)).label("Q2"),
                func.sum(case((quarter == 3, 1), else_=0)).label("Q3"),
                func.sum(case((quarter == 4, 1), else_=0)).label("Q4"),
            )
            .join(Department, HiredEmployee.department_id == Department.id)
            .join(Job, HiredEmployee.job_id == Job.id)
            .filter(extract("year", HiredEmployee.datetime) == year)
            .group_by(Department.department, Job.job)
            .order_by(Department.department, Job.job)
        )
        return [row._mapping for row in query.all()]

    @staticmethod
    async def get_by_department_higher_than_year_mean(year: int):
        session = BaseDBModel.session_factory()
        subquery = (
            session.query(
                Department.id.label("department_id"),
                func.count(HiredEmployee.id).label("count"),
            )
            .join(HiredEmployee, Department.id == HiredEmployee.department_id)
            .filter(func.extract("year", HiredEmployee.datetime) == year)
            .group_by(Department.id)
            .subquery()
        )

        # Main query to retrieve department information with hired employee counts
        query = (
            session.query(
                Department.id,
                Department.department,
                func.count(HiredEmployee.id).label("hired"),
            )
            .join(HiredEmployee, Department.id == HiredEmployee.department_id)
            .filter(func.extract("year", HiredEmployee.datetime) == year)
            .group_by(Department.id, Department.department)
            .having(
                func.count(HiredEmployee.id)
                > session.query(
                    func.avg(subquery.c.count).label("mean_employees_hired")
                ).scalar()
            )
            .order_by(func.count(HiredEmployee.id).desc())
        )

        return [row._mapping for row in query.all()]
