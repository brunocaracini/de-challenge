"-------------------------------Imports Section-------------------------------"

# Libraries
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Local Dependencies
from app.config.env_settings import (
    ORIGINS,
    ALLOW_CREDENTIALS,
    ALLOW_HEADERS,
    ALLOW_METHODS,
)
from app.resources.config_manager import ConfigManager
from app.database.table_creations import create_all_tables, delete_all_tables

# Global variables
CURRENT_VERSION = ConfigManager.get_conf_value(
    config_file_name="api", section="api", value="current_version"
)

try:
    api_routers = __import__(f"app.api.versions.{CURRENT_VERSION}", fromlist=["*"])
except ImportError as error:
    print(
        f"Module 'app.api.versions.{CURRENT_VERSION}.main_{CURRENT_VERSION}' not found."
    )
    raise error


"-------------------------------Server Configuration-------------------------------"

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)


if "create_tables" in sys.argv:
    create_all_tables()
elif "delete_tables" in sys.argv:
    delete_all_tables()


app.include_router(api_routers.health_router.router)
app.include_router(api_routers.jobs_router.router)
app.include_router(api_routers.departments_router.router)
app.include_router(api_routers.hired_employees_router.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
