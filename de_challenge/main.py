"-------------------------------Imports Section-------------------------------"

# Libraries
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Local Dependencies
from app.resources.config_manager import ConfigManager

# Global variables
CURRENT_VERSION = ConfigManager.get_conf_value(
    config_file_name="api", section="api", value="current_version"
)


try:
    api_routers = __import__(
        f"app.api.versions.{CURRENT_VERSION}.main_{CURRENT_VERSION}", fromlist=["*"]
    )
except ImportError as error:
    print(
        f"Module 'app.api.versions.{CURRENT_VERSION}.main_{CURRENT_VERSION}' not found."
    )
    raise error


"-------------------------------Server Configuration-------------------------------"

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_routers.jobs_router.router)
app.include_router(api_routers.departments_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
