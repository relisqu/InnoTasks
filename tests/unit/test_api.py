import unittest
from fastapi.testclient import TestClient
from api.main import app
from repository.repository import User, UserLogin


class TestApp(unittest.TestCase):
    client = TestClient(app)

    def test_register_user(self):
        user = {"username": "test_user", "password_hash": "password123"}
        response = self.client.post("/register", json=user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), user)

    def test_register_existing_user(self):
        user = {"username": "test_user", "password_hash": "password123"}
        self.client.post("/register", json=user)
        response = self.client.post("/register", json=user)
        self.assertEqual(response.status_code, 400)

    def test_login_user(self):
        user = {"username": "test_user", "password_hash": "password123"}
        self.client.post("/register", json=user)
        login_data = {"username": "test_user", "password_hash": "password123"}
        response = self.client.post("/login", json=login_data)
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_user(self):
        user = {"username": "test_user", "password_hash": "password123"}
        self.client.post("/register", json=user)
        login_data = {"username": "test_user", "password_hash": "wrong_password"}
        response = self.client.post("/login", json=login_data)
        self.assertEqual(response.status_code, 422)

    def test_add_task(self):
        task_data = {"user_id": 1, "task": "Test task", "task_status": "ToDo", "task_due_date": "2024-05-01"}
        response = self.client.post("/task", json=task_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Task added successfully"})

    def test_view_all_data(self):
        user_id = 1
        response = self.client.get(f"/tasks/{user_id}")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
