# Implementation Plan - 1-Day Technical Conference Website (Google Cloud Technologies)

Building a responsive, high-aesthetic 1-day technical conference website for a Google Cloud conference using Python + Flask backend and Vanilla HTML/CSS/JavaScript frontend.

## User Review Required

> [!NOTE]
> The application will run using the Python environment at `/Users/jimtyhurst/src/gemini/20260725-agent-engineering/.venv/bin/python` with Flask installed.

## Requirements Checklist
1. **Home Page**: Displays date, location, full timetable and schedule.
2. **8 Total Talks**: Distributed across morning and afternoon sessions.
3. **1-2 Speakers per talk**: First Name, Last Name, and LinkedIn profile URL.
4. **Talk Metadata**: ID, Title, Speakers, Category (1 or 2), Description, Time.
5. **Interactive Search**: Filter talks dynamically by Category, Speaker name, or Title.
6. **Lunch Break**: Explicit 60-minute scheduled break (12:50 PM - 1:50 PM).
7. **Dummy Data**: Realistically structured Google Cloud topic talks (Vertex AI, Cloud Run, BigQuery, GKE, Security, Cloud Spanner, Pub/Sub, Anthos).
8. **Tech Stack**: Python (Flask) server, Vanilla HTML/CSS/JS frontend with modern glassmorphism aesthetic.
9. **README & Verification**: Detailed setup/run/customization documentation, tested and launched for live review.

---

## Proposed Changes

### Backend (Python & Flask)

#### [NEW] [app.py](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/app.py)
- Flask server entry point.
- Serves the main conference schedule page.
- Provides `/api/talks` endpoint for client-side live search/filtering and structured data rendering.

#### [NEW] [data/talks.py](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/data/talks.py)
- Contains conference metadata (date, location, event name).
- Contains 8 complete talks with 1-2 speakers each, categories ("Category 1: Cloud & DevOps Infrastructure", "Category 2: AI & Data Engineering"), timing, and descriptions.
- Includes 60-minute lunch break event entry.

---

### Frontend (Templates, Styles & Scripting)

#### [NEW] [templates/index.html](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/templates/index.html)
- Conference header with live date badge, location, stats counter (8 Talks, 12 Speakers, 2 Tracks).
- Search & Filter bar: Search input (title/speaker), Category selector dropdown (All, Category 1, Category 2), reset button.
- Timetable Grid: Interactive talk cards with category pill, speaker avatars, time slots, lunch break highlight banner.
- Modal dialog for detailed talk descriptions and speaker LinkedIn links.

#### [NEW] [static/css/style.css](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/static/css/style.css)
- Dark modern design system with Google Cloud blue/purple gradients, glassmorphism card containers, smooth transitions, responsive grid/flexbox layouts.

#### [NEW] [static/js/main.js](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/static/js/main.js)
- Instant filtering by title, speaker name, and category.
- Modal open/close handler for talk details.
- Active states & search result counter.

---

### Documentation

#### [MODIFY] [README.md](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/README.md)
- Complete guide on prerequisites, setup, running the server, data structure explanation, and how to add/modify talks or categories.

---

## Verification Plan

### Automated / Server Tests
- Run Flask app in test mode to verify route responses (`/` and `/api/talks`).
- Validate JSON payload structure for talk schema (8 talks, speakers, lunch break).

### Manual Verification & UI Testing
- Open browser / curl requests to test filter combinations (e.g. search "Vertex", filter "Category 2", search speaker "Sarah").
- Verify 60-minute lunch break display.
- Confirm LinkedIn URL targets.
