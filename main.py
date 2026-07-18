# Stage 1
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class TaskCreate(BaseModel):
    title: str | None = None
    done: bool | None = None


# Stage 2
tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Upload project to GitHub",
        "done": True
    }
]


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# Stage 3
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    if task.title is None or not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


# Stage 4
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskCreate):

    for task in tasks:
        if task["id"] == task_id:

            if updated_task.title is None and updated_task.done is None:
                raise HTTPException(
                    status_code=400,
                    detail="No data provided for update"
                )

            if updated_task.title is not None:

                if not updated_task.title.strip():
                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty"
                    )

                task["title"] = updated_task.title

            if updated_task.done is not None:
                task["done"] = updated_task.done

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )