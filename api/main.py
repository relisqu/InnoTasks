from fastapi import FastAPI
from fastapi import HTTPException, status
import repository.repository as repo

app = FastAPI()


# Route to register a new user
@app.post("/register", response_model=repo.User)
async def register_user(user: repo.User):
    try:
        repo.register_user(user)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    return user


# Route for user login
@app.post("/login")
async def login(user: repo.UserLogin):
    try:
        return repo.login_user(user)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )


@app.post("/task")
async def add_task(task: repo.Task):
    try:
        repo.add_task(task)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Task could not be added"
        )
    return {"message": "Task added successfully"}


@app.get("/task/{user_id}/{task_id}")
async def get_task(user_id: int, task_id: int):
    try:
        return repo.get_task(user_id, task_id)
    except ValueError:
        print("get /task error", ValueError)


@app.put("/task")
async def edit_task_data(task: repo.TaskEdit):
    try:
        return repo.edit_task_data(task)
    except ValueError:
        print("put /task error", ValueError)


@app.delete("/task/{user_id}/{task_id}")
async def delete_data(user_id: int, task_id: int):
    try:
        return repo.delete_data(user_id, task_id)
    except ValueError:
        print("delete /task error", ValueError)


@app.get("/tasks/{user_id}")
async def view_all_data(user_id: int):
    try:
        return repo.view_all_data(user_id)
    except ValueError:
        print("get /tasks error", ValueError)


@app.get("/tasks/names/{user_id}")
async def view_all_task_names(user_id: int):
    try:
        return repo.view_all_task_names(user_id)
    except ValueError:
        print("get /tasks/names error", ValueError)
