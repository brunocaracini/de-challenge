"-------------------------------Imports Section-------------------------------"

# Libraries
from typing import List
from app.database.entities.departments import Department
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException

# Local Dependencies
from app.resources.utils import Utils
from app.api.versions.v1.schemas_v1 import DepartmentUpload
from app.controllers.entities.departments_controller import DepartmentController


ENDPOINT_BASE_PATH = Utils.router_base_path_calculator(router_name="departments")
router = APIRouter(prefix=ENDPOINT_BASE_PATH)


def validate_csv_headers(csv_headers: List[str]):
    allowed_headers = Utils.get_class_variables_from_object(Department)
    if csv_headers:
        if set(allowed_headers) != set(csv_headers):
            raise HTTPException(
                status_code=400,
                detail=f"'{csv_headers}' is not an allowed header combination. CSV headers must be: {allowed_headers}",
            )
    else:
        return allowed_headers
    return csv_headers


@router.post(f"/batch-csv-upload/", tags=["Departments"])
async def upload_batch_csv(
    file: UploadFile = File(...), csv_headers: List[str] = Depends(validate_csv_headers)
):
    return await DepartmentController.batch_from_csv(file=file, headers=csv_headers)


@router.post(f"/", tags=["Departments"])
async def upload(body: DepartmentUpload):
    return await DepartmentController.insert_many(jobs=body.departments)