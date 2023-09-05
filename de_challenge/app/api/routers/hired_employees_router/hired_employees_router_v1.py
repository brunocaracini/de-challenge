"-------------------------------Imports Section-------------------------------"

# Libraries
import datetime
from typing import List
from app.database.entities.hired_employees import HiredEmployee
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException

# Local Dependencies
from app.resources.utils import Utils
from app.api.versions.v1.schemas_v1 import HiredEmployeeUpload
from app.controllers.entities.hired_employees_controller import HiredEmployeeController


ENDPOINT_BASE_PATH = Utils.router_base_path_calculator(router_name="hired_employees")
router = APIRouter(prefix=ENDPOINT_BASE_PATH)


def validate_csv_headers(csv_headers: List[str], first_row_headers: bool = False):
    allowed_headers = Utils.get_class_variables_from_object(HiredEmployee)
    if not first_row_headers:
        # Check if the uploaded CSV headers match the allowed headers
        if set(allowed_headers) != set(csv_headers) and csv_headers:
            raise HTTPException(
                status_code=400,
                detail=f"CSV headers do not match the allowed header combination. CSV headers must be: {allowed_headers}",
            )
        return csv_headers if csv_headers else allowed_headers
    else:
        return None


def validate_year(year: int = 2021):
    if year < 1900 or year > datetime.datetime.now().year:
        raise HTTPException(status_code=400, detail="Invalid year")
    return year


@router.post(f"/batch-csv-upload/", tags=["Hired Employees"])
async def upload_batch_csv(
    file: UploadFile = File(...),
    first_row_headers: bool = False,
    csv_headers: List[str] = Depends(validate_csv_headers),
):
    return await HiredEmployeeController.batch_from_csv(
        file=file, first_row_headers=first_row_headers, headers=csv_headers
    )


@router.post("/", tags=["Hired Employees"])
async def upload(body: HiredEmployeeUpload):
    return await HiredEmployeeController.insert_many(jobs=body.hired_employees)


@router.get("/by-job-and-department-by-quarter/", tags=["Hired Employees"])
async def get_by_job_and_department(year: int = Depends(validate_year)):
    return await HiredEmployeeController.get_by_job_and_department(year=year)


@router.get("/by-department-higher-than-year-mean/", tags=["Hired Employees"])
async def get_by_department_higher_than_year_mean(year: int = Depends(validate_year)):
    return await HiredEmployeeController.get_by_department_higher_than_year_mean(
        year=year
    )
