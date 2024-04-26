from passlib.context import CryptContext
from pydantic import BaseModel
import database.db as db

# Create a password hashing object
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Pydantic model for user
class User(BaseModel):
    username: str
    password: str


# Pydantic model for user login
class UserLogin(BaseModel):
    username: str
    password: str


def add_task(user_id: int, task: str, task_status: str, task_due_date: str):
    db.add_data(user_id, task, task_status, task_due_date)
    return {"message": "Task added successfully"}


# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def register_user(user: User):
    hashed_password = pwd_context.hash(user.password)
    db.register_user(user.username, hashed_password)
    return user


def login_user(user: UserLogin):
    hashed_password = pwd_context.hash(user.password)
    user = db.authenticate_user(user.username, hashed_password)
    if user:
        return {"message": "Login successful"}
    return None


# Function to get user details from the repository
def get_user(username: str):
    return db.get_user_by_username(username)
