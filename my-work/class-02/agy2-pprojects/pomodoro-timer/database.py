import sqlite3
import os
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "pomodoro.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            est_pomodoros INTEGER DEFAULT 1,
            completed_pomodoros INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Session logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS session_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            task_id INTEGER,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL
        )
    """)
    
    # Settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)
    
    # Insert default settings if not exists
    default_settings = {
        "work_duration": "25",
        "short_break_duration": "5",
        "long_break_duration": "15",
        "auto_start_breaks": "false",
        "auto_start_pomodoros": "false",
        "sound_volume": "50",
        "theme": "sage"
    }
    
    for key, val in default_settings.items():
        cursor.execute("INSERT OR IGNORE INTO user_settings (key, value) VALUES (?, ?)", (key, val))
        
    conn.commit()
    conn.close()

# Task Helpers
def get_all_tasks() -> List[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY status ASC, id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def create_task(title: str, category: str = "General", est_pomodoros: int = 1) -> Dict[str, Any]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, category, est_pomodoros) VALUES (?, ?, ?)",
        (title, category, est_pomodoros)
    )
    task_id = cursor.lastrowid
    conn.commit()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)

def update_task(task_id: int, title: Optional[str] = None, category: Optional[str] = None, 
                est_pomodoros: Optional[int] = None, completed_pomodoros: Optional[int] = None, 
                status: Optional[str] = None) -> Optional[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    
    fields = []
    values = []
    if title is not None:
        fields.append("title = ?")
        values.append(title)
    if category is not None:
        fields.append("category = ?")
        values.append(category)
    if est_pomodoros is not None:
        fields.append("est_pomodoros = ?")
        values.append(est_pomodoros)
    if completed_pomodoros is not None:
        fields.append("completed_pomodoros = ?")
        values.append(completed_pomodoros)
    if status is not None:
        fields.append("status = ?")
        values.append(status)
        
    if not fields:
        conn.close()
        return None
        
    values.append(task_id)
    query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, tuple(values))
    conn.commit()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def delete_task(task_id: int) -> bool:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

# Session Helpers
def log_session(mode: str, duration_minutes: int, task_id: Optional[int] = None) -> Dict[str, Any]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO session_logs (mode, duration_minutes, task_id) VALUES (?, ?, ?)",
        (mode, duration_minutes, task_id)
    )
    session_id = cursor.lastrowid
    
    # If a task was linked to a completed work pomodoro, increment task's completed_pomodoros
    if mode == "work" and task_id:
        cursor.execute(
            "UPDATE tasks SET completed_pomodoros = completed_pomodoros + 1 WHERE id = ?",
            (task_id,)
        )
        
    conn.commit()
    cursor.execute("SELECT * FROM session_logs WHERE id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)

def get_stats() -> Dict[str, Any]:
    conn = get_db()
    cursor = conn.cursor()
    
    # Total focus minutes today
    cursor.execute("""
        SELECT COALESCE(SUM(duration_minutes), 0) as today_minutes, COUNT(*) as today_sessions
        FROM session_logs 
        WHERE mode = 'work' AND DATE(completed_at) = DATE('now', 'localtime')
    """)
    today_row = cursor.fetchone()
    
    # Total focus minutes all time
    cursor.execute("""
        SELECT COALESCE(SUM(duration_minutes), 0) as total_minutes, COUNT(*) as total_sessions
        FROM session_logs 
        WHERE mode = 'work'
    """)
    total_row = cursor.fetchone()
    
    # Past 7 days breakdown
    cursor.execute("""
        SELECT DATE(completed_at) as date, COALESCE(SUM(duration_minutes), 0) as minutes, COUNT(*) as count
        FROM session_logs
        WHERE mode = 'work' AND completed_at >= DATE('now', '-6 days', 'localtime')
        GROUP BY DATE(completed_at)
        ORDER BY date ASC
    """)
    weekly_rows = [dict(r) for r in cursor.fetchall()]
    
    # Completed tasks count
    cursor.execute("SELECT COUNT(*) as completed_count FROM tasks WHERE status = 'completed'")
    completed_tasks = cursor.fetchone()["completed_count"]
    
    conn.close()
    
    return {
        "today_minutes": today_row["today_minutes"],
        "today_sessions": today_row["today_sessions"],
        "total_minutes": total_row["total_minutes"],
        "total_sessions": total_row["total_sessions"],
        "completed_tasks": completed_tasks,
        "weekly_history": weekly_rows
    }

# Settings Helpers
def get_all_settings() -> Dict[str, str]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM user_settings")
    rows = cursor.fetchall()
    conn.close()
    return {row["key"]: row["value"] for row in rows}

def save_settings(settings: Dict[str, str]):
    conn = get_db()
    cursor = conn.cursor()
    for k, v in settings.items():
        cursor.execute("INSERT OR REPLACE INTO user_settings (key, value) VALUES (?, ?)", (k, str(v)))
    conn.commit()
    conn.close()
