"-------------------------------Imports Section-------------------------------"

# Libraries
from pydantic import BaseModel, field_validator
from typing import Optional, Union, List

# Local Dependencies
from app.resources.config_manager import ConfigManager

MIN_BATCH_SIZE, MAX_BATCH_SIZE = ConfigManager.get_conf_value(
    config_file_name="api", section="data", value="batch_size", variable_type="list"
)


# ----------------------------------Jobs---------------------------------

class JobModel(BaseModel):
    id: int
    job: str


class JobUpload(BaseModel):
    jobs: List[JobModel]

    @field_validator("jobs")
    def validate_list_length(cls, value):
        print(MIN_BATCH_SIZE, MAX_BATCH_SIZE)
        if not MIN_BATCH_SIZE <= len(value) <= MAX_BATCH_SIZE:
            raise ValueError(
                f"Batch size must be between {MIN_BATCH_SIZE} and {MAX_BATCH_SIZE}."
            )
        return value
    
# ----------------------------------Departments---------------------------------

class DepartmentModel(BaseModel):
    id: int
    department: str


class DepartmentUpload(BaseModel):
    departments: List[DepartmentModel]

    @field_validator("departments")
    def validate_list_length(cls, value):
        print(MIN_BATCH_SIZE, MAX_BATCH_SIZE)
        if not MIN_BATCH_SIZE <= len(value) <= MAX_BATCH_SIZE:
            raise ValueError(
                f"Batch size must be between {MIN_BATCH_SIZE} and {MAX_BATCH_SIZE}."
            )
        return value

# ----------------------------------Hired Employees---------------------------------

class HiredEmployeeModel(BaseModel):
    id: int
    name: str
    job_id: int
    department_id: int

class HiredEmployeeUpload(BaseModel):
    hired_employees: List[HiredEmployeeModel]

    @field_validator("hired_employees")
    def validate_list_length(cls, value):
        print(MIN_BATCH_SIZE, MAX_BATCH_SIZE)
        if not MIN_BATCH_SIZE <= len(value) <= MAX_BATCH_SIZE:
            raise ValueError(
                f"Batch size must be between {MIN_BATCH_SIZE} and {MAX_BATCH_SIZE}."
            )
        return value