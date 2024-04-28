import os

import pytest
from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture(scope="session")
def init(request):
    print("\nDoing setup")

    def fin():
        print("\nDoing teardown")
        os.remove("data.db")

    request.addfinalizer(fin)


def test_register_user(init):
    user = {"username": "test_user", "password": "password123"}
    response = client.post("/register", json=user)
    print(response)
    assert response.status_code == 200
    assert user == response.json()


def test_register_existing_user(init):
    user = {"username": "test_user", "password": "password123"}
    client.post("/register", json=user)
    response = client.post("/register", json=user)
    assert response.status_code == 400


def test_login_user(init):
    login_data = {"username": "test_user", "password": "password123"}
    response = client.post("/login", json=login_data)
    assert response.status_code == 200


def test_login_invalid_user(init):
    login_data = {"username": "test_user", "password": "wrong_password"}
    response = client.post("/login", json=login_data)
    assert response.status_code == 401


def test_add_task(init):
    task_data = {
        "user_id": 1,
        "task": "Test task",
        "task_status": "ToDo",
        "task_priority": "Normal",
        "task_due_date": "2024-05-01",
    }
    response = client.post("/task", json=task_data)
    assert response.status_code == 200
    assert {"message": "Task added successfully"} == response.json()


def test_view_all_data(init):
    user_id = 1
    response = client.get(f"/tasks/{user_id}")
    assert response.status_code == 200


def test_view_all_task_names(init):
    user_id = 1
    task_data = {
        "user_id": 1,
        "task": "Test task",
        "task_status": "ToDo",
        "task_priority": "Normal",
        "task_due_date": "2024-05-01",
    }
    response = client.post("/task", json=task_data)
    task_data = {
        "user_id": 1,
        "task": "Test2 task",
        "task_status": "ToDo",
        "task_priority": "Normal",
        "task_due_date": "2024-05-01",
    }
    response = client.post("/task", json=task_data)

    response = client.get(f"/tasks/names/{user_id}")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == [["Test task", 1], ["Test task", 2], ["Test2 task", 3]]
