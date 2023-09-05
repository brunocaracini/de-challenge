"-------------------------------Imports Section-------------------------------"

# Libraries
from typing import List
from app.database.entities.jobs import Job
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException

# Local Dependencies
from app.resources.utils import Utils
from app.api.versions.v1.schemas_v1 import JobUpload
from app.controllers.entities.jobs_controller import JobController


ENDPOINT_BASE_PATH = Utils.router_base_path_calculator(router_name="jobs")
router = APIRouter(prefix=ENDPOINT_BASE_PATH)


def validate_csv_headers(csv_headers: List[str], first_row_headers: bool = False):
    allowed_headers = Utils.get_class_variables_from_object(Job)
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


@router.post(f"/batch-csv-upload/", tags=["Hired Employees"])
async def upload_batch_csv(
    file: UploadFile = File(...),
    first_row_headers: bool = False,
    csv_headers: List[str] = Depends(validate_csv_headers),
):
    return await JobController.batch_from_csv(
        file=file, first_row_headers=first_row_headers, headers=csv_headers
    )


@router.post(f"/", tags=["Jobs"])
async def upload(body: JobUpload):
    return await JobController.insert_many(jobs=body.jobs)
