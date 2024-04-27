import unittest
from database.db import *
from unittest.mock import patch
from unittest.mock import MagicMock
import sqlite3


class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        # Connect to an in-memory database for testing
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        create_table()

    def tearDown(self):
        # Close the database connection after each test
        self.conn.close()

    def test_delete_user(self):
        self.clear_test_user()
        register_user("test_user", "password123")
        delete_user('test_user')
        user_after_deletion = get_user_by_username('test_user')
        self.assertIsNone(user_after_deletion, "User should not exist after deletion")

    def test_delete_user_tasks_and_check_existence(self):

        self.clear_test_user()

        user = register_user("test_user", "password123")
        add_data(user[0], 'Task 1', 'ToDo', '2024-04-30')
        add_data(user[0], 'Task 2', 'Doing', '2024-05-01')

        delete_user_tasks(user[0])
        tasks_after_deletion = view_all_data(user[0])
        self.assertEqual(len(tasks_after_deletion), 0, "No tasks should exist after deletion")
    def test_register_user(self):
        # Test user registration
        self.clear_test_user()
        self.assertTrue(register_user("test_user", "password123"))
        self.assertFalse(register_user("test_user", "password123"))  # Duplicate registration should fail

    def test_authenticate_user(self):
        # Test user authentication
        self.clear_test_user()
        register_user("test_user", "password123")
        self.assertTrue(authenticate_user("test_user", "password123"))
        self.assertFalse(authenticate_user("test_user", "wrong_password"))

    def test_add_and_view_task(self):
        # Test adding and viewing tasks
        self.clear_test_user()
        user = register_user("test_user", "password123")
        add_data(user[0], "Test Task", "ToDo", "2024-05-01")
        tasks = view_all_data(user[0])
        self.assertEqual(1,len(tasks) )
        self.assertEqual(tasks[0][2], "Test Task")

    def test_edit_task(self):
        # Test editing a task
        self.clear_test_user()
        user = register_user("test_user", "password123")
        add_data(user[0], "Test Task", "ToDo", "2024-05-01")
        edit_task_data(user[0], "Updated Task", "Done", "2024-05-02", "Test Task", "ToDo", "2024-05-01")
        tasks = view_all_data(user[0])
        self.assertEqual(tasks[0][2], "Updated Task")
        self.assertEqual(tasks[0][3], "Done")
        self.assertEqual(tasks[0][4], "2024-05-02")

    def test_delete_task(self):
        # Test deleting a task
        self.clear_test_user()
        user = register_user("test_user", "password123")
        add_data(user[0], "Test Task", "ToDo", "2024-05-01")
        delete_data(user[0], "Test Task")
        tasks = view_all_data(user[0])
        self.assertEqual(len(tasks), 0)

    def test_get_task_by_status(self):
        # Test getting tasks by status
        self.clear_test_user()
        user = register_user("test_user", "password123")
        add_data(user[0], "Test Task 1", "ToDo", "2024-05-01")
        add_data(user[0], "Test Task 2", "Done", "2024-05-02")
        tasks = get_task_by_status(user[0], "Done")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][2], "Test Task 2")

    def test_get_task_by_username(self):
        # Test getting user by username
        self.clear_test_user()
        register_user("test_user", "password123")
        user = get_user_by_username("test_user")
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "test_user")

    def test_get_task(self):
        # Test getting a task by task name
        self.clear_test_user()
        user = register_user("test_user", "password123")
        add_data(user[0], "Test Task", "ToDo", "2024-05-01")
        task = get_task(user[0], "Test Task")
        self.assertIsNotNone(task)
        self.assertEqual(task[0][2], "Test Task")

    def clear_test_user(self):
        user_id = get_user_by_username("test_user")
        if user_id is not None:
            delete_user_tasks(user_id[0])
            delete_user("test_user")