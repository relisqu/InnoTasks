from pydantic import BaseModel
import database.db as db
import hashlib

db = db.Database()

# Pydantic model for user
class User(BaseModel):
    username: str
    password: str


# Pydantic model for user login
class UserLogin(BaseModel):
    username: str
    password: str


def register_user(user: User):
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    resp = db.register_user(user.username, hashed_password)
    if not resp:
        raise ValueError("User already exists")
    return user


def login_user(user: UserLogin):
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    resp = db.authenticate_user(user.username, hashed_password)
    if not resp:
        raise ValueError("Invalid username or password")
    return resp


# Function to get user details from the repository
def get_user(username: str):
    return db.get_user_by_username(username)

def add_task(user_id: int, task: str, task_status: str, task_priority: str, task_due_date: str):
    db.add_data(user_id, task, task_status, task_priority, task_due_date)
    return {"message": "Task added successfully"}

def view_all_data(user_id: int):
    resp = db.view_all_data(user_id)
    if not resp:
        return []
    return resp

def add_task(user_id, task, task_status, task_priority, task_due_date):
    db.add_data(user_id, task, task_status, task_priority, task_due_date)
    
def view_all_task_names(user_id):
    return db.view_all_task_names(user_id)

def get_task(user_id, task_id):
    return db.get_task(user_id, task_id)

def edit_task_data(user_id, task_id, new_task_name, new_task_status, new_task_priority, new_task_date):
    print('repo edit task data')
    db.edit_task_data(user_id, task_id, new_task_name, new_task_status, new_task_priority, new_task_date)

def delete_data(user_id, task_id):
    db.delete_data(user_id, task_id)