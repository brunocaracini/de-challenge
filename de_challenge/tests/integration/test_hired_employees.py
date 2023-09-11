from tests.test_init import client


def test_create_department_for_hired_employee():
    department_data = {"department": "Test Department 101", "id": 101}
    payload = {"departments": [department_data]}
    response = client.post("/api/v1/departments/", json=payload)
    assert response.status_code == 200
    created_department = response.json()
    assert (
        created_department["valids"][0]["department"] == department_data["department"]
    )


def test_create_job_for_hired_employee():
    job_data = {"job": "Test Job 101", "id": 101}
    payload = {"jobs": [job_data]}
    response = client.post("/api/v1/jobs/", json=payload)
    assert response.status_code == 200
    created_job = response.json()
    assert created_job["valids"][0]["job"] == job_data["job"]


def test_create_hired_employee():
    employee_data = {
        "id": 999,
        "name": "John Doe 999",
        "department_id": 101,
        "job_id": 101,
    }
    payload = {"hired_employees": [employee_data]}
    response = client.post("/api/v1/hired-employees/", json=payload)
    assert response.status_code == 200
    created_employee = response.json()
    assert created_employee["valids"][0]["name"] == employee_data["name"]


def test_get_employees_by_job_and_department():
    response = client.get("/api/v1/hired-employees/by-job-and-department-by-quarter/")
    assert response.status_code == 200

