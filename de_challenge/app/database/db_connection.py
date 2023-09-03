# Libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Local Dependencies
from config.env_settings import DB_USER, DB_NAME, DB_PORT, DB_HOST, DB_PASSWORD

# Connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create a SQLAlchemy engine
ENGINE = create_engine(DATABASE_URL)

# Define an SQLAlchemy declarative base
BASE = declarative_base()

# Create a session factory
SESSION = sessionmaker(bind=ENGINE)

# Create a session instance
session = SESSION()

