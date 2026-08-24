import sys
import pytest
from fastapi.testclient import TestClient

from app import app
import database

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Ensure database schema is initialized before each test."""
    database.init_db()

def test_tasks_crud_flow():
    # 1. GET initial tasks
    response = client.get("/api/tasks")
    assert response.status_code == 200
    initial_tasks = response.json()
    assert isinstance(initial_tasks, list)

    # 2. POST create a new task
    new_task_payload = {
        "title": "API Test Task",
        "category": "Testing",
        "est_pomodoros": 3
    }
    create_resp = client.post("/api/tasks", json=new_task_payload)
    assert create_resp.status_code == 200
    created_task = create_resp.json()
    assert created_task["title"] == "API Test Task"
    assert created_task["category"] == "Testing"
    assert created_task["est_pomodoros"] == 3
    assert created_task["completed_pomodoros"] == 0
    assert created_task["status"] == "pending"
    task_id = created_task["id"]

    # 3. POST validation failure (empty title)
    invalid_task_resp = client.post("/api/tasks", json={"title": "   ", "category": "Work"})
    assert invalid_task_resp.status_code == 400
    assert invalid_task_resp.json()["detail"] == "Task title cannot be empty"

    # 4. PUT update the task
    update_payload = {
        "title": "API Test Task Updated",
        "completed_pomodoros": 1,
        "status": "in_progress"
    }
    update_resp = client.put(f"/api/tasks/{task_id}", json=update_payload)
    assert update_resp.status_code == 200
    updated_task = update_resp.json()
    assert updated_task["title"] == "API Test Task Updated"
    assert updated_task["completed_pomodoros"] == 1
    assert updated_task["status"] == "in_progress"

    # 5. PUT update nonexistent task (404)
    non_existent_update = client.put("/api/tasks/99999", json={"title": "Ghost Task"})
    assert non_existent_update.status_code == 404
    assert non_existent_update.json()["detail"] == "Task not found"

    # 6. DELETE the created task
    delete_resp = client.delete(f"/api/tasks/{task_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json() == {"status": "deleted", "id": task_id}

    # 7. DELETE nonexistent task (404)
    non_existent_delete = client.delete("/api/tasks/99999")
    assert non_existent_delete.status_code == 404
    assert non_existent_delete.json()["detail"] == "Task not found"


def test_sessions_and_stats():
    # 1. POST record session
    session_payload = {
        "mode": "work",
        "duration_minutes": 25,
        "task_id": None
    }
    session_resp = client.post("/api/sessions", json=session_payload)
    assert session_resp.status_code == 200
    logged_session = session_resp.json()
    assert logged_session["mode"] == "work"
    assert logged_session["duration_minutes"] == 25

    # 2. GET stats
    stats_resp = client.get("/api/stats")
    assert stats_resp.status_code == 200
    stats = stats_resp.json()
    assert "today_minutes" in stats
    assert "today_sessions" in stats
    assert "total_minutes" in stats
    assert "total_sessions" in stats
    assert "completed_tasks" in stats
    assert "weekly_history" in stats


def test_settings_flow():
    # 1. GET settings
    get_resp = client.get("/api/settings")
    assert get_resp.status_code == 200
    settings = get_resp.json()
    assert isinstance(settings, dict)

    # 2. POST update settings
    update_payload = {
        "settings": {
            "work_duration": 30,
            "short_break_duration": 10,
            "theme": "Midnight"
        }
    }
    post_resp = client.post("/api/settings", json=update_payload)
    assert post_resp.status_code == 200
    updated_settings = post_resp.json()
    assert updated_settings.get("work_duration") == "30" or updated_settings.get("work_duration") == 30
    assert updated_settings.get("short_break_duration") == "10" or updated_settings.get("short_break_duration") == 10
    assert updated_settings.get("theme") == "Midnight"
