"-------------------------------Imports Section-------------------------------"

# Libraries
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, insert

# Local Dependencies
from app.config.env_settings import DB_USER, DB_NAME, DB_PORT, DB_HOST, DB_PASSWORD


# Define module-level variables for the engine, session factory, and session
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create a SQLAlchemy engine
ENGINE = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)

# Define session factory for sessioon creation
SESSION_FACTORY = sessionmaker(bind=ENGINE)

# Define an SQLAlchemy declarative base
BASE = declarative_base()


class BaseDBModel:
    
    @classmethod
    async def insert_many(cls, entities, model_class, db):
        results = {"valids": [], "invalids": []}
        for entity in entities:
            try:
                db.execute(insert(model_class).values(entity))
                results["valids"].append(entity)
                db.commit()
            except Exception as error:
                db.rollback()
                print(str(error))
                error = error.orig.args[0].split("\n")
                entity["error"] = {
                    "description": error[0],
                    "detail": error[1].lstrip("DETAIL:  "),
                }
                results["invalids"].append(entity)
                db.commit()
                continue            
        return results
    
    @staticmethod
    def session_factory():
        return SESSION_FACTORY()
