import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException, status
import repository.repository as repo

app = FastAPI()

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("api.main:app", host="0.0.0.0", port=3000)


# Route to register a new user
@app.post("/register", response_model=repo.User)
async def register_user(user: repo.User):
    try:
        repo.register_user(user)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return user


# Route for user login
@app.post("/login")
async def login(user: repo.UserLogin):
    try:
        return repo.login_user(user)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")


@app.post("/task")
async def add_task(user_id: int, task: str, task_status: str, task_priority: str, task_due_date: str):
    repo.add_task(user_id, task, task_status, task_priority, task_due_date)
    return {"message": "Task added successfully"}

@app.get('/tasks/{user_id}')
async def view_all_data(user_id: int):
    try: 
        return repo.view_all_data(user_id)
    except ValueError:
        print('get /tasks error', ValueError)