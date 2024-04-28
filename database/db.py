import sqlite3
import shutil
from datetime import datetime


class Database:
    def __init__(self, db_path="data.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.c = self.conn.cursor()
        self.create_table()
        self.backup_sqlite_db()

    def create_table(self):
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash TEXT
            )
        """
        )

        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS taskstable (
                id INTEGER PRIMARY KEY, 
                user_id INTEGER,
                task TEXT,
                task_status TEXT,
                task_priority TEXT,
                task_due_date DATE,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """
        )

        self.conn.commit()

    def get_user_by_username(self, username):
        self.c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = self.c.fetchone()
        return user

    def delete_user(self, username):
        self.c.execute("DELETE FROM users WHERE username=?", (username,))
        self.conn.commit()

    def delete_user_tasks(self, user_id):
        self.c.execute("DELETE FROM taskstable WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def register_user(self, username, password_hash):
        user = self.get_user_by_username(username)
        if user:
            return False
        self.c.execute(
            "INSERT INTO users(username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        self.conn.commit()
        return self.get_user_by_username(username)

    def authenticate_user(self, username, password_hash):
        user = self.get_user_by_username(username)
        if not user:
            return False
        if user[2] == password_hash:
            return user
        return False

    def add_data(self, user_id, task, task_status, task_priority, task_due_date):
        self.c.execute(
            """INSERT INTO taskstable(
            user_id, 
            task, 
            task_status, 
            task_priority, 
            task_due_date
            ) VALUES (?, ?, ?, ?, ?)""",
            (user_id, task, task_status, task_priority, task_due_date),
        )
        self.conn.commit()

    def view_all_data(self, user_id):
        self.c.execute(
            """SELECT 
                task, 
                task_status, 
                task_priority, 
                task_due_date 
            FROM taskstable WHERE user_id=?""",
            (user_id,),
        )
        data = self.c.fetchall()
        return data

    def view_all_task_names(self, user_id):
        self.c.execute(
            "SELECT DISTINCT task, id FROM taskstable WHERE user_id=?",
            (user_id,)
        )
        data = self.c.fetchall()
        return data

    def get_task(self, user_id, task_id):
        self.c.execute(
            "SELECT * FROM taskstable WHERE user_id=? AND id=?",
            (user_id, task_id)
        )
        data = self.c.fetchall()
        return data

    def get_task_by_status(self, user_id, task_status):
        self.c.execute(
            "SELECT * FROM taskstable WHERE user_id=? AND task_status=?",
            (user_id, task_status),
        )
        data = self.c.fetchall()
        return data

    def edit_task_data(
            self,
            user_id,
            task_id,
            new_task_name,
            new_task_status,
            new_task_priority,
            new_task_date,
    ):
        self.c.execute(
            """UPDATE taskstable SET 
                task=?, 
                task_status=?, 
                task_priority=?, 
                task_due_date=? 
            WHERE user_id=? AND id=?""",
            (
                new_task_name,
                new_task_status,
                new_task_priority,
                new_task_date,
                user_id,
                task_id,
            ),
        )
        self.conn.commit()
        data = self.c.fetchall()
        return data

    def delete_data(self, user_id, task_id):
        self.backup_sqlite_db()
        self.c.execute(
            "DELETE FROM taskstable WHERE user_id=? AND id=?",
            (user_id, task_id)
        )
        self.conn.commit()

    def backup_sqlite_db(self):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_filename = f"backup_{timestamp}.sqlite"
            backup_path = f"../../backups/{backup_filename}"
            shutil.copy2(self.db_path, backup_path)
            print(f"Backup created: {backup_path}")
        except Exception as e:
            print(f"Error creating backup: {e}")
        finally:
            self.conn.close()
