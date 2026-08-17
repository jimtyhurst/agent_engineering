# Calm Productivity App with Pomodoro Timer Implementation Plan

Create a full-featured, calm, and aesthetic productivity web application featuring a Pomodoro timer, integrated task manager, ambient background sound synthesis, and analytics dashboard. The application will be backed by a Python FastAPI server running in the existing `.venv` environment (`/Users/jimtyhurst/src/gemini/20260725-agent-engineering/.venv/bin/python3`).

## User Review Required

> [!NOTE]
> The app will run a local Python FastAPI backend server on a local port (e.g. `8000`) and serve a modern SPA frontend built with Vanilla HTML/CSS/JS with zero external heavy frontend frameworks needed.

> [!TIP]
> Ambient sounds (Rain, Ocean, Zen Chime) will be generated natively using the browser's **Web Audio API**, avoiding external audio file downloads and ensuring instant, reliable playback.

## Proposed Changes

### Backend & Database Layer

#### [NEW] [database.py](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/pomodoro-timer/database.py)
- SQLite database helper (`pomodoro.db`) using standard library `sqlite3`.
- Schemas for:
  - `tasks`: id, title, category, est_pomodoros, completed_pomodoros, status, created_at
  - `session_logs`: id, mode (work/short_break/long_break), duration_minutes, task_id, completed_at
  - `user_settings`: key-value settings (work_duration, break_duration, theme, etc.)

#### [NEW] [app.py](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/pomodoro-timer/app.py)
- FastAPI application serving REST endpoints and static files.
- Endpoints:
  - `GET /api/tasks` & `POST /api/tasks`
  - `PUT /api/tasks/{task_id}` & `DELETE /api/tasks/{task_id}`
  - `GET /api/sessions` & `POST /api/sessions`
  - `GET /api/stats`
  - `GET /api/settings` & `POST /api/settings`

### Frontend Application

#### [NEW] [static/index.html](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/pomodoro-timer/static/index.html)
- Clean, semantic HTML structure with accessible elements (`<dialog>`, `<button>`, `<main>`).
- Layout structure:
  - Header: App Title ("ZenFlow Pomodoro"), Theme Selector (Sage, Midnight, Amber, Ocean), Settings & Stats buttons.
  - Main Timer Section: Circular SVG timer ring, timer display, mode pills (Focus, Short Break, Long Break), Active Task indicator, Play/Pause/Reset/Skip control bar.
  - Ambient Sound Controller: Soft toggles for Rain, Waves, Forest with volume controls.
  - Task Manager Panel: Task creation form, filter controls, task items with "Set as Active Task" button and Pomodoro count badges.
  - Modals: Settings modal for timer custom durations & audio; Statistics modal for focus history.

#### [NEW] [static/style.css](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/pomodoro-timer/static/style.css)
- CSS Custom Properties for theme palettes (Sage, Midnight, Amber, Ocean).
- Organic glassmorphism effects (`backdrop-filter: blur(12px)`), soft organic shadows, subtle pulsing animations for timer state.
- Dynamic responsive layout (mobile friendly & desktop split panel).
- Modern scrollbars and transition states (`@starting-style`, `:has()`).

#### [NEW] [static/app.js](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/pomodoro-timer/static/app.js)
- Timer controller logic with web worker / precise timestamp tracking.
- Web Audio API Sound Synthesizer (Ambient noise generators & soft bowl chime notification).
- REST API synchronization for tasks, completed session logging, and settings.
- UI state management and stats visualizer rendering.

### Server Launcher Script

#### [NEW] [main.py](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/agy2-pprojects/pomodoro-timer/main.py)
- Server entrypoint using `uvicorn` and Python executable `/Users/jimtyhurst/src/gemini/20260725-agent-engineering/.venv/bin/python3`.

---

## Verification Plan

### Automated Tests / Health Check
- Run server using `/Users/jimtyhurst/src/gemini/20260725-agent-engineering/.venv/bin/python3 main.py` or uvicorn.
- Test REST API endpoints with HTTP requests (tasks CRUD, sessions logging, settings persistence).

### Manual & Visual Verification
- Open browser preview via `browser_subagent` to verify UI aesthetics, timer operation, theme toggling, sound generation, task binding, and responsive layout.
