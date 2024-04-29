import os
import pytest
import unittest
from repository.repository import *


class TestEndToEnd(unittest.TestCase):

    @pytest.fixture(scope="session")
    def init(request):
        print("\nDoing setup")

        def fin():
            print("\nDoing teardown")
            os.remove("data.db")

        request.addfinalizer(fin)

    def test_registration_login_add_task(self):
        # Register a new user
        user = User(username="testuser123", password="password123")
        registered_user = register_user(user)
        self.assertEqual(registered_user.username, user.username)

        # Log in with the registered user
        user_login = UserLogin(username="testuser123", password="password123")
        logged_in_user = login_user(user_login)
        self.assertEqual(logged_in_user[1], user_login.username)

        # Add a task for the logged-in user
        response = add_task(
            Task(
                user_id=logged_in_user[0],
                task="Test task",
                task_status="ToDo",
                task_priority="High",
                task_due_date="2024-05-01",
            )
        )
        self.assertEqual(response["message"], "Task added successfully")

        # View all tasks for the logged-in user
        tasks = view_all_data(logged_in_user[0])
        self.assertTrue(tasks)
        self.assertEqual(tasks[0][0], "Test task")

    def test_invalid_login(self):
        # Try to log in with invalid credentials
        user_login = UserLogin(username="nonexistentuser", password="wrongpassword")
        with self.assertRaises(ValueError):
            login_user(user_login)

    def test_duplicate_registration(self):
        # Try to register a user with a username that already exists
        user = User(username="testuser", password="password123")
        with self.assertRaises(ValueError):
            register_user(user)
            register_user(user)

    def test_view_all_tasks_without_login(self):
        # Try to view all tasks without logging in first
        value = view_all_data(user_id=1)
        print(value)
        assert value == []


if __name__ == "__main__":
    unittest.main()
