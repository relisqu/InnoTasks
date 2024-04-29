import unittest
from database.db import Database


class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        # Connect to an in-memory database for testing
        self.database = Database(db_path=":memory:")

    def test_delete_user(self):
        self.database.register_user("test_user", "password123")
        self.database.delete_user("test_user")
        user_after_deletion = self.database.get_user_by_username("test_user")
        self.assertIsNone(user_after_deletion, "User should not exist after deletion")

    def test_delete_user_tasks_and_check_existence(self):
        user = self.database.register_user("test_user", "password123")
        self.database.add_data(user[0], "Task 1", "ToDo", "Important", "2024-04-30")
        self.database.add_data(user[0], "Task 2", "Doing", "Important", "2024-05-01")

        self.database.delete_user_tasks(user[0])
        tasks_after_deletion = self.database.view_all_data(user[0])
        self.assertEqual(
            0, len(tasks_after_deletion), "No tasks should exist after deletion"
        )

    def test_register_user(self):
        self.assertTrue(self.database.register_user("test_user", "password123"))
        self.assertFalse(
            self.database.register_user("test_user", "password123")
        )  # Duplicate registration should fail

    def test_authenticate_user(self):
        self.database.register_user("test_user", "password123")
        self.assertTrue(self.database.authenticate_user("test_user", "password123"))
        self.assertFalse(self.database.authenticate_user("test_user", "wrong_password"))

    def test_add_and_view_task(self):
        user = self.database.register_user("test_user", "password123")
        self.database.add_data(user[0], "Test Task", "ToDo", "Important", "2024-05-01")
        tasks = self.database.view_all_data(user[0])
        self.assertEqual(1, len(tasks))
        self.assertEqual("Test Task", tasks[0][0])

    def test_edit_task(self):
        user = self.database.register_user("test_user", "password123")
        self.database.add_data(user[0], "Test Task", "ToDo", "Important", "2024-05-01")
        self.database.edit_task_data(
            user[0], 1, "Updated Task", "Done", "Not Important", "2024-05-02"
        )
        tasks = self.database.view_all_data(user[0])
        self.assertEqual("Updated Task", tasks[0][0])
        self.assertEqual("Done", tasks[0][1])
        self.assertEqual("Not Important", tasks[0][2])
        self.assertEqual("2024-05-02", tasks[0][3])

    def test_delete_task(self):
        user = self.database.register_user("test_user", "password123")
        self.database.add_data(user[0], "Test Task", "ToDo", "Important", "2024-05-01")

        user_tasks = self.database.view_all_task_names(user[0])
        self.database.delete_data(user[0], dict(user_tasks)["Test Task"])
        tasks = self.database.view_all_data(user[0])
        self.assertEqual(len(tasks), 0)

    def test_get_task_by_status(self):
        user = self.database.register_user("test_user", "password123")
        self.database.add_data(
            user[0], "Test Task 1", "ToDo", "Important", "2024-05-01"
        )
        self.database.add_data(
            user[0], "Test Task 2", "Done", "Important", "2024-05-02"
        )
        tasks = self.database.get_task_by_status(user[0], "Done")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][2], "Test Task 2")

    def test_get_task_by_username(self):
        self.database.register_user("test_user", "password123")
        user = self.database.get_user_by_username("test_user")
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "test_user")

    def test_get_task(self):
        user = self.database.register_user("test_user", "password123")
        self.database.add_data(user[0], "Test Task", "ToDo", "Important", "2024-05-01")
        user_tasks = self.database.view_all_task_names(user[0])
        task = self.database.get_task(user[0], dict(user_tasks)["Test Task"])
        self.assertIsNotNone(task)
        self.assertEqual(task[0][2], "Test Task")


if __name__ == "__main__":
    unittest.main()
