"-------------------------------Imports Section-------------------------------"

# Libraries
from typing import List
from app.database.entities.hired_employees import HiredEmployee
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException

# Local Dependencies
from app.resources.utils import Utils
from app.api.versions.v1.schemas_v1 import HiredEmployeeUpload
from app.controllers.entities.hired_employees_controller import HiredEmployeeController


ENDPOINT_BASE_PATH = Utils.router_base_path_calculator(router_name="hired_employees")
router = APIRouter(prefix=ENDPOINT_BASE_PATH)


def validate_csv_headers(csv_headers: List[str]):
    allowed_headers = Utils.get_class_variables_from_object(HiredEmployee)
    if csv_headers:
        if set(allowed_headers) != set(csv_headers):
            raise HTTPException(
                status_code=400,
                detail=f"'{csv_headers}' is not an allowed header combination. CSV headers must be: {allowed_headers}",
            )
    else:
        return allowed_headers
    return csv_headers


@router.post(f"/batch-csv-upload/", tags=["Hired Employees"])
async def upload_batch_csv(
    file: UploadFile = File(...), csv_headers: List[str] = Depends(validate_csv_headers)
):
    return await HiredEmployeeController.batch_from_csv(file=file, headers=csv_headers)


@router.post("/", tags=["Hired Employees"])
async def upload(body: HiredEmployeeUpload):
    return await HiredEmployeeController.insert_many(jobs=body.hired_employees)


@router.get("/by-job-and-department-by-quarter/", tags=["Hired Employees"])
async def get_by_job_and_department(year: int = 2021):
    return await HiredEmployeeController.get_by_job_and_department(year=year)


@router.get("/by-department-higher-than-year-mean/", tags=["Hired Employees"])
async def get_by_department_higher_than_year_mean(year: int = 2021):
    return await HiredEmployeeController.get_by_department_higher_than_year_mean(year=year)