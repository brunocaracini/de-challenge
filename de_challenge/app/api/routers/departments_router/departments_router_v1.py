"-------------------------------Imports Section-------------------------------"

# Libraries
from fastapi import APIRouter, Depends, Request, File, UploadFile

# Local Dependencies
from app.resources.utils import Utils

router = APIRouter()
ENDPOINT_BASE_PATH = Utils.router_base_path_calculator(router_name="departments")


@router.post(f"{ENDPOINT_BASE_PATH}/batch-csv/", tags=["Departments"])
async def upload_batch_csv(
    file: UploadFile = File(...)
):
    return True
