# Google Cloud Technical Conference Website - Walkthrough & Verification

The 1-day technical conference web application is fully built, configured, and launched on local server port **5001**.

---

## 🚀 Accomplishments

### 1. Flask Web Application Core ([app.py](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/app.py))
- Implemented Flask server serving the conference home page and a `/api/talks` JSON endpoint.
- Configured dynamic statistics calculation (talk counts, speaker counts, category metadata).

### 2. Dataset Infrastructure ([data/talks.py](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/data/talks.py))
- Created realistic 8-talk Google Cloud Technologies schedule.
- Included 1-2 expert speakers per talk with first name, last name, role, company, and LinkedIn URL.
- Assigned talks to **Category 1 (Cloud & DevOps Infrastructure)** and **Category 2 (AI & Data Engineering)**.
- Added explicit **60-minute networking lunch break** (12:15 PM - 1:15 PM).

### 3. High-Aesthetic Frontend Interface ([templates/index.html](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/templates/index.html))
- Header hero banner featuring date badge, location, schedule format, and stats cards.
- Control panel with real-time search box and category filter dropdown.
- Schedule cards with time badges, category tags, speaker avatars, and clickable LinkedIn buttons.
- Lunch break highlight banner.

### 4. Custom Styling & Interactive Filtering ([static/css/style.css](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/static/css/style.css), [static/js/main.js](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/static/js/main.js))
- Modern dark mode aesthetic using Google Cloud accent colors (`#4285F4`, `#34A853`, `#FBBC04`, `#EA4335`).
- Glassmorphism containers, smooth hover transitions, responsive mobile & desktop layout.
- Instant client-side search and filtering by speaker, title, or category.

### 5. Detailed Setup & Maintenance Guide ([README.md](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/README.md))
- Complete instructions for environment setup, launching the application, testing endpoints, and modifying talks/categories.

---

## 🧪 Runtime Verification Results

### 1. Server Launch & Health Check
- Command: `python app.py` running on `http://127.0.0.1:5001`
- Status: Active & healthy.

### 2. API Endpoint Verification
```bash
curl -s http://127.0.0.1:5001/api/talks
```
- **Response**: `{"count": 8, "success": true, "talks": [...]}`

```bash
curl -s "http://127.0.0.1:5001/api/talks?q=spanner"
```
- **Response**: Returns matching talk for Cloud Spanner.

### 3. HTML Page Rendering
```bash
curl -s http://127.0.0.1:5001/
```
- **Response**: Renders title `Google Cloud Tech Summit 2026`, hero banner, date, location, schedule, and scripts.

---

## 🔗 Live Application Access
You can access and review the running application in your web browser at:
👉 **[http://127.0.0.1:5001](http://127.0.0.1:5001)**
