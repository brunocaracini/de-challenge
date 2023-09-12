from tests.test_init import client, TestingSessionLocal


def test_create_job():
    job_data = {"job": "Test Job 999", "id": 999}
    payload = {"jobs":[job_data]}
    response = client.post("/api/v1/jobs/", json=payload)
    assert response.status_code == 200
    created_job = response.json()
    assert created_job["valids"][0]["job"] == job_data["job"]