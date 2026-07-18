"""
Task Management REST API
FastAPI + in-memory storage (Python list)

Run with:
    pip install fastapi uvicorn --break-system-packages
    uvicorn main:app --reload

Swagger docs available at:  http://127.0.0.1:8000/docs
ReDoc docs available at:    http://127.0.0.1:8000/redoc
"""

from itertools import count
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple in-memory Task Management REST API built with FastAPI.",
)

# --------------------------------------------------------------------------
# In-memory storage
# --------------------------------------------------------------------------
tasks: List[dict] = []
_id_counter = count(1)  # auto-incrementing task IDs, starting at 1


# --------------------------------------------------------------------------
# Schemas
# --------------------------------------------------------------------------
class TaskCreate(BaseModel):
    title: str = Field(..., description="Title of the task")

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v: str) -> str:
        if v is None or not v.strip():
            raise ValueError("title must not be empty")
        return v


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Updated title of the task")
    done: Optional[bool] = Field(None, description="Updated completion status")

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank_if_present(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("title must not be empty")
        return v


class Task(BaseModel):
    id: int
    title: str
    done: bool


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def find_task(task_id: int) -> Optional[dict]:
    return next((t for t in tasks if t["id"] == task_id), None)


def error_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"error": message})


# --------------------------------------------------------------------------
# Validation error handling -> force 400 instead of FastAPI's default 422
# --------------------------------------------------------------------------
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Build a readable error message from pydantic's error list
    messages = []
    for err in exc.errors():
        loc = ".".join(str(x) for x in err.get("loc", []) if x != "body")
        msg = err.get("msg", "Invalid input")
        messages.append(f"{loc}: {msg}" if loc else msg)
    return error_response(status.HTTP_400_BAD_REQUEST, "; ".join(messages) or "Invalid input")


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------
@app.get("/", tags=["Meta"], summary="API info")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", tags=["Meta"], summary="Health check")
def health_check():
    return {"status": "ok"}


@app.get("/tasks", response_model=List[Task], tags=["Tasks"], summary="List all tasks")
def get_tasks():
    return tasks


@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
    summary="Get a single task",
    responses={404: {"description": "Task not found"}},
)
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        return error_response(status.HTTP_404_NOT_FOUND, "Task not found")
    return task


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Create a new task",
    responses={400: {"description": "Invalid input"}},
)
def create_task(payload: TaskCreate):
    new_task = {"id": next(_id_counter), "title": payload.title.strip(), "done": False}
    tasks.append(new_task)
    return new_task


@app.put(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
    summary="Update a task",
    responses={400: {"description": "Invalid input"}, 404: {"description": "Task not found"}},
)
def update_task(task_id: int, payload: TaskUpdate):
    task = find_task(task_id)
    if task is None:
        return error_response(status.HTTP_404_NOT_FOUND, "Task not found")

    if payload.title is None and payload.done is None:
        return error_response(
            status.HTTP_400_BAD_REQUEST, "At least one of 'title' or 'done' must be provided"
        )

    if payload.title is not None:
        task["title"] = payload.title.strip()
    if payload.done is not None:
        task["done"] = payload.done

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Delete a task",
    responses={404: {"description": "Task not found"}},
)
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        return error_response(status.HTTP_404_NOT_FOUND, "Task not found")
    tasks.remove(task)
    return Nones