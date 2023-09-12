import os
from app.resources.config_manager import ConfigManager


if not os.getenv("ENVIRONMENT", False):
    from dotenv import load_dotenv

    print("Container database will be used as no environment has been defined")
    load_dotenv(
        "./.env",
    )
else:
    print(f"Running into environment: {os.environ.get('ENVIRONMENT')}")


# Database env variables
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")


# Server env variables
ORIGINS = ConfigManager.get_conf_value(
    config_file_name="api", section="api", value="origins", variable_type="list"
) if os.getenv("ORIGINS", True) else os.environ.get("ORIGINS")

ALLOW_METHODS = ConfigManager.get_conf_value(
    config_file_name="api", section="api", value="allow_methods", variable_type="list"
) if os.getenv("ALLOW_METHODS", True) else os.environ.get("ALLOW_METHODS")

# Retrieve the value for ALLOW_HEADERS
ALLOW_HEADERS = ConfigManager.get_conf_value(
    config_file_name="api", section="api", value="allow_headers", variable_type="list"
) if os.getenv("ALLOW_HEADERS", True) else os.environ.get("ALLOW_HEADERS")

# Retrieve the value for ALLOW_CREDENTIALS
ALLOW_CREDENTIALS = ConfigManager.get_conf_value(
    config_file_name="api", section="api", value="allow_credentials", variable_type="bool"
) if os.getenv("ALLOW_CREDENTIALS", True) else os.environ.get("ALLOW_CREDENTIALS")
