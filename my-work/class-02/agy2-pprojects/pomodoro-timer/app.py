from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os

import database

app = FastAPI(title="ZenFlow Pomodoro API", version="1.0.0")

# Enable CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Init database on startup
@app.on_event("startup")
def startup():
    database.init_db()

# Pydantic Schemas
class TaskCreate(BaseModel):
    title: str
    category: Optional[str] = "General"
    est_pomodoros: Optional[int] = 1

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    est_pomodoros: Optional[int] = None
    completed_pomodoros: Optional[int] = None
    status: Optional[str] = None

class SessionLogCreate(BaseModel):
    mode: str  # 'work', 'short_break', 'long_break'
    duration_minutes: int
    task_id: Optional[int] = None

class SettingsUpdate(BaseModel):
    settings: Dict[str, Any]

# API Endpoints
@app.get("/api/tasks")
def list_tasks():
    return database.get_all_tasks()

@app.post("/api/tasks")
def add_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Task title cannot be empty")
    return database.create_task(
        title=task.title.strip(),
        category=task.category or "General",
        est_pomodoros=max(1, task.est_pomodoros or 1)
    )

@app.put("/api/tasks/{task_id}")
def modify_task(task_id: int, task: TaskUpdate):
    updated = database.update_task(
        task_id=task_id,
        title=task.title,
        category=task.category,
        est_pomodoros=task.est_pomodoros,
        completed_pomodoros=task.completed_pomodoros,
        status=task.status
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@app.delete("/api/tasks/{task_id}")
def remove_task(task_id: int):
    success = database.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "deleted", "id": task_id}

@app.post("/api/sessions")
def record_session(session: SessionLogCreate):
    return database.log_session(
        mode=session.mode,
        duration_minutes=session.duration_minutes,
        task_id=session.task_id
    )

@app.get("/api/stats")
def fetch_stats():
    return database.get_stats()

@app.get("/api/settings")
def fetch_settings():
    return database.get_all_settings()

@app.post("/api/settings")
def update_settings(payload: SettingsUpdate):
    database.save_settings(payload.settings)
    return database.get_all_settings()

# Mount Static Files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
