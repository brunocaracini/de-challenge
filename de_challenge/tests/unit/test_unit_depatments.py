from tests.test_init import TestingSessionLocal
from app.database.entities.departments import Department


def test_create_department():
    with TestingSessionLocal() as test_db:
        # Create a new job record
        department = Department(department="Test Department 4")

        # Add the department to the database session
        test_db.add(department)

        # Commit the transaction to the database
        test_db.commit()

        # Refresh the job to fetch any changes from the database
        test_db.refresh(department)

        all_departments = test_db.query(Department).all()

        # Assert that there is at least one record in the table
        assert len(all_departments) == 3

        # Optionally, you can assert specific properties of the retrieved records
        assert all_departments[2].department == "Test Department 4"
