import unittest
from repository.repository import *
from unittest.mock import patch
from unittest.mock import MagicMock
import sqlite3
from database.db import *
class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        # Connect to an in-memory database for testing
        self.database = Database(':memory:')
    def test_registration_login_add_task(self):
        # Register a new user
        user = User(username="testuser", password="password123")
        registered_user = register_user(user)
        self.assertEqual(registered_user.username, user.username)

        # Log in with the registered user
        user_login = UserLogin(username="testuser", password="password123")
        logged_in_user = login_user(user_login)
        self.assertEqual(logged_in_user.username, user_login.username)

        # Add a task for the logged-in user
        response = add_task(logged_in_user.id, "Test task", "ToDo", "High", "2024-05-01")
        self.assertEqual(response["message"], "Task added successfully")

        # View all tasks for the logged-in user
        tasks = view_all_data(logged_in_user.id)
        self.assertTrue(tasks)
        self.assertEqual(tasks[0]["task"], "Test task")

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

    def test_add_task_without_login(self):
        # Try to add a task without logging in first
        with self.assertRaises(ValueError):
            add_task(user_id=1, task="Test task", task_status="ToDo", task_priority="High", task_due_date="2024-05-01")

    def test_view_all_tasks_without_login(self):
        # Try to view all tasks without logging in first
        with self.assertRaises(ValueError):
            view_all_data(user_id=1)

if __name__ == '__main__':
    unittest.main()