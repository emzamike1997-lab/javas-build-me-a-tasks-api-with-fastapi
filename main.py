import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="build me a tasks API with FastAPI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Task(BaseModel):
    id: int
    title: str
    description: str
    done: bool

tasks = [
    {"id": 1, "title": "Task 1", "description": "This is task 1", "done": False},
    {"id": 2, "title": "Task 2", "description": "This is task 2", "done": False},
    {"id": 3, "title": "Task 3", "description": "This is task 3", "done": False},
]

@app.get("/")
def root(): return {"status": "ok", "service": "build me a tasks API with FastAPI"}

@app.get("/health")
def health(): return {"status": "healthy"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return {"error": "Task not found"}

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task.dict())
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks[i] = task.dict()
            return task
    return {"error": "Task not found"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[i]
            return {"message": "Task deleted"}
    return {"error": "Task not found"}

if __name__ == "__main__":
    print(" FastAPI app starting...")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)