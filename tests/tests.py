import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from main import app
from sqlalchemy.pool import StaticPool
from app.database.db_connection import BASE as Base
from app.database.entities.jobs import Job


@pytest.fixture(scope="module")
def test_db():
    # Create an SQLite in-memory database
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    SQLALCHEMY_DATABASE_URL = "sqlite://"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()

def test_create_job(test_db):
    # Create a new job record
    job = Job(job="Test Job")

    # Add the job to the database session
    test_db.add(job)

    # Commit the transaction to the database
    test_db.commit()

    # Refresh the job to fetch any changes from the database
    test_db.refresh(job)

    # Use a TestClient to make an HTTP request to your API
    client = TestClient(app)

    # Send an HTTP POST request to your endpoint
    response = client.post(
        "/api/v1/jobs/", json={"jobs": [{"id": 199, "job": "Test Job"}]}
    )
    print("------------------------------------------")
    # Perform assertions on the response
    assert response.status_code == 200
    print(response.json())
    assert response.json()["valids"][0]["job"] == "Test Job"

    # Close the database session
    test_db.close()
