from tests.test_init import client, TestingSessionLocal


def test_create_department():
    department_data = {"department": "Test Department","id": 999}
    payload = {"departments":[department_data]}
    response = client.post("/api/v1/departments/", json=payload)
    assert response.status_code == 200
    created_department = response.json()
    assert created_department["valids"][0]["department"] == department_data["department"]
