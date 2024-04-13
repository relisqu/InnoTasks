from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
import sqlite3

# Create a FastAPI instance
app = FastAPI()

# Create a password hashing object
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SQLite database connection
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create a table to store user information
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
conn.commit()

# Pydantic model for user
class User(BaseModel):
    username: str
    password: str

# Pydantic model for user login
class UserLogin(BaseModel):
    username: str
    password: str

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to get user details from the database
def get_user(username: str):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone()

# Route to register a new user
@app.post("/register", response_model=User)
async def register_user(user: User):
    hashed_password = pwd_context.hash(user.password)
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, hashed_password))
    conn.commit()
    return user

# Route for user login
@app.post("/login")
async def login(user: UserLogin):
    db_user = get_user(user.username)
    if db_user:
        if verify_password(user.password, db_user[2]):
            return {"message": "Login successful"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")