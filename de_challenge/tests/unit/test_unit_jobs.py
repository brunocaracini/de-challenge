from tests.test_init import TestingSessionLocal
from app.database.entities.jobs import Job


def test_create_job():
    # Create a new job record
    job = Job(job="Test Job")

    with TestingSessionLocal() as test_db:
        # Add the job to the database session
        test_db.add(job)

        # Commit the transaction to the database
        test_db.commit()

        # Refresh the job to fetch any changes from the database
        test_db.refresh(job)

        all_jobs = test_db.query(Job).all()

        # Assert that there is at least one record in the table
        assert len(all_jobs) == 3

        # Optionally, you can assert specific properties of the retrieved records
        assert all_jobs[2].job == "Test Job"
