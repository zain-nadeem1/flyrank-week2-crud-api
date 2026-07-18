# FlyRank AI Internship — Week 2 Assignment 1

## Build Your First CRUD API

A beginner backend project developed during the **FlyRank AI Internship (Backend AI Track)**.

This project implements a Task Management API using **Python FastAPI** and demonstrates the fundamentals of backend development:

* API endpoints
* HTTP methods
* CRUD operations
* Request validation
* Status codes
* Swagger API documentation
* Git and GitHub workflow

---

## Tech Stack

* Python 3.10+
* FastAPI
* Uvicorn
* Pydantic
* Swagger UI
* Git & GitHub

---

## Project Features

The API supports complete CRUD functionality:

* Create tasks
* Read tasks
* Update tasks
* Delete tasks

The data is stored using an in-memory list (no database), as required by the assignment.

---

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

Move into the project folder:

```bash
cd flyrank-week2-crud-api
```

Create and activate virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the API

Start the server:

```bash
uvicorn main:app --reload
```

The API will run at:

```
http://127.0.0.1:8000
```

---

## Swagger Documentation

FastAPI automatically provides interactive documentation.

Open:

```
http://127.0.0.1:8000/docs
```

Swagger UI allows testing all API endpoints without using external tools.

![Swagger UI](swagger.png)

---

## API Endpoints

| Method | Endpoint      | Description         |
| ------ | ------------- | ------------------- |
| GET    | `/`           | API information     |
| GET    | `/health`     | Server health check |
| GET    | `/tasks`      | Get all tasks       |
| GET    | `/tasks/{id}` | Get a task by ID    |
| POST   | `/tasks`      | Create a new task   |
| PUT    | `/tasks/{id}` | Update a task       |
| DELETE | `/tasks/{id}` | Delete a task       |

---

## Status Codes Implemented

| Status Code | Meaning                   |
| ----------- | ------------------------- |
| 200         | Successful request        |
| 201         | Task created              |
| 204         | Task deleted successfully |
| 400         | Invalid request data      |
| 404         | Task not found            |

---

## Example API Test

### Create Task

Request:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks \
-H "Content-Type: application/json" \
-d "{\"title\":\"Learn Backend Development\"}"
```

Response:

```json
{
    "id": 4,
    "title": "Learn Backend Development",
    "done": false
}
```

---

## Learning Outcome

Through this assignment, I practiced:

* Building REST APIs with FastAPI
* Understanding request-response flow
* Implementing CRUD operations
* Validating user input
* Documenting APIs using Swagger
* Managing projects with Git and GitHub

---

## Internship Context

This project was completed as part of:

**FlyRank AI Internship**
**Backend AI Track**
**Week 2 — Assignment 1: Build Your First CRUD API**
