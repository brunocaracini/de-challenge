from app.database.entities.jobs import Job
from app.database.entities.departments import Department
from app.database.entities.hired_employees import HiredEmployee

def create_all_tables():

    Job.__create_table__()
    Department.__create_table__()
    HiredEmployee.__create_table__()

def delete_all_tables():
    Job.__delete_table()
    Department.__delete_table()
    HiredEmployee.__delete_table()