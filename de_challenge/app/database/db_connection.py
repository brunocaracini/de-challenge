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

# Define an SQLAlchemy declarative base
BASE = declarative_base()

SESSION_FACTORY = sessionmaker(bind=ENGINE)


class BaseDBModel:
    
    @staticmethod
    async def insert_many(entities, model_class):
        results = {"valids": [], "invalids": []}
        with BaseDBModel.session_factory() as session:
            for entity in entities:
                try:
                    session.execute(insert(model_class).values(entity))
                    results["valids"].append(entity)
                    session.commit()
                except Exception as error:
                    session.rollback()
                    error = error.orig.args[0].split("\n")
                    entity["error"] = {
                        "description": error[0],
                        "detail": error[1].lstrip("DETAIL:  "),
                    }
                    results["invalids"].append(entity)
                    session.commit()
                    continue
            
            session.close()
        return results
    
    @staticmethod
    def session_factory():
        return SESSION_FACTORY()
