"-------------------------------Imports Section-------------------------------"

# Libraries
from typing import List
from app.database.entities.hired_employees import HiredEmployee
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException

# Local Dependencies
from app.resources.utils import Utils
from app.api.versions.v1.schemas_v1 import HiredEmployeeUpload
from app.controllers.entities.hired_employees_controller import HiredEmployeeController


router = APIRouter()
ENDPOINT_BASE_PATH = Utils.router_base_path_calculator(router_name="hired_employees")


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


@router.post(f"{ENDPOINT_BASE_PATH}batch-csv-upload/", tags=["hired_employees"])
async def upload_batch_csv(
    file: UploadFile = File(...), csv_headers: List[str] = Depends(validate_csv_headers)
):
    return await HiredEmployeeController.batch_from_csv(file=file, headers=csv_headers)


@router.post(f"{ENDPOINT_BASE_PATH}", tags=["hired_employees"])
async def upload(body: HiredEmployeeUpload):
    return await HiredEmployeeController.insert_many(jobs=body.jobs)