import sqlite3

conn = sqlite3.connect('../data.db', check_same_thread=False)
c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT)')

    c.execute(
        'CREATE TABLE IF NOT EXISTS taskstable(id INTEGER PRIMARY KEY, user_id INTEGER, task TEXT, task_status TEXT, '
        'task_due_date DATE, FOREIGN KEY(user_id) REFERENCES users(id))')


def get_user_by_username(username):
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    user = c.fetchone()
    print(user)
    return user


def register_user(username, password_hash):
    c.execute('INSERT INTO users(username, password_hash) VALUES (?, ?)', (username, password_hash))
    conn.commit()


def authenticate_user(username, password_hash):
    c.execute('SELECT * FROM users WHERE username=? AND password_hash=?', (username, password_hash))
    user = c.fetchone()
    return user


def add_data(user_id, task, task_status, task_due_date):
    c.execute('INSERT INTO taskstable(user_id, task, task_status, task_due_date) VALUES (?, ?, ?, ?)',
              (user_id, task, task_status, task_due_date))
    conn.commit()


def view_all_data(user_id):
    c.execute('SELECT * FROM taskstable WHERE user_id=?', (user_id,))
    data = c.fetchall()
    return data


def view_all_task_names(user_id):
    c.execute('SELECT DISTINCT task FROM taskstable WHERE user_id=?', (user_id,))
    data = c.fetchall()
    return data


def get_task(user_id, task):
    c.execute('SELECT * FROM taskstable WHERE user_id=? AND task=?', (user_id, task))
    data = c.fetchall()
    return data


def get_task_by_status(user_id, task_status):
    c.execute('SELECT * FROM taskstable WHERE user_id=? AND task_status=?', (user_id, task_status))
    data = c.fetchall()
    return data


def edit_task_data(user_id, new_task, new_task_status, new_task_date, task, task_status, task_due_date):
    c.execute(
        "UPDATE taskstable SET task=?, task_status=?, task_due_date=? WHERE user_id=? AND task=? AND task_status=? AND task_due_date=?",
        (new_task, new_task_status, new_task_date, user_id, task, task_status, task_due_date))
    conn.commit()
    data = c.fetchall()
    return data


def delete_data(user_id, task):
    c.execute('DELETE FROM taskstable WHERE user_id=? AND task=?', (user_id, task))
    conn.commit()


create_table()
