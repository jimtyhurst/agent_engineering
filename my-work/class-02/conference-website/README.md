# Google Cloud Tech Summit 2026 - 1-Day Technical Conference Website

An interactive, responsive 1-day technical conference website built with **Python & Flask** on the server side and **Vanilla HTML, CSS, and JavaScript** on the front end.

---

## 🌟 Features & Highlights

1. **Home Page & Schedule Banner**:
   - Event metadata displaying current conference date, venue location, schedule timetable, and interactive stats counter.
2. **8 Expert Technical Talks**:
   - Focused on Google Cloud Technologies (Vertex AI, Cloud Run, BigQuery, Cloud Spanner, GKE, Security & IAM, Dataflow, TPU v5p).
3. **Speaker Profiles (1 to 2 Max per Talk)**:
   - Includes First Name, Last Name, Role, Company, and verified LinkedIn profile links.
4. **Comprehensive Talk Metadata**:
   - Every talk features a unique ID (e.g. `#talk-1`), Title, Speakers, Category badge, Description, and designated Time Slot.
5. **Category System**:
   - **Category 1**: Cloud & DevOps Infrastructure
   - **Category 2**: AI & Data Engineering
6. **60-Minute Scheduled Lunch Break**:
   - Highlights a 1-hour catered networking and partner expo break (12:15 PM - 1:15 PM).
7. **Instant Dynamic Search & Filtering**:
   - Filter talks by category tab/dropdown, speaker name, or talk title in real time.
8. **JSON API Endpoint**:
   - `/api/talks` endpoint for dynamic programmatic querying.

---

## 🛠 Tech Stack

- **Backend**: Python 3, Flask framework
- **Data Store**: `data/talks.py` (Python data structure)
- **Frontend**: Vanilla HTML5, Modern Vanilla CSS3 (Custom properties, glassmorphism, responsive grid), Vanilla JavaScript (ES6+)

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+ installed
- Virtual environment at `/Users/jimtyhurst/src/gemini/20260725-agent-engineering/.venv`

### Step 1: Activate Virtual Environment
```bash
source /Users/jimtyhurst/src/gemini/20260725-agent-engineering/.venv/bin/activate
```

### Step 2: Install Dependencies
Flask is already installed in the virtual environment. If setting up on a new environment, run:
```bash
uv add flask
# OR
pip install flask
```

---

## 💻 Running the Web Application

To launch the Flask web server:

```bash
/Users/jimtyhurst/src/gemini/20260725-agent-engineering/.venv/bin/python app.py
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Testing Functionality

### 1. Manual Browser UI Testing
- **Search Test**: Type `Vertex` or `Maya` in the search bar. Observe instant filtering of matching talks.
- **Category Filter Test**: Select **Category 1: Cloud & DevOps Infrastructure** from the dropdown. Verify only Cat 1 talks remain visible.
- **LinkedIn Link Test**: Click any speaker's **LinkedIn** pill button to confirm external link opens in a new tab.
- **60-Minute Lunch Break**: Verify the 12:15 PM - 1:15 PM lunch card displays prominently.

### 2. API Endpoint Testing
You can query the JSON API endpoint using `curl`:
```bash
# Fetch all talks
curl http://127.0.0.1:5000/api/talks

# Filter by category
curl "http://127.0.0.1:5000/api/talks?category=cat-1"

# Search by keyword
curl "http://127.0.0.1:5000/api/talks?q=spanner"
```

---

## 🔧 How to Make Further Changes

### Adding or Modifying Talks / Speakers
All event data is stored in [`data/talks.py`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/data/talks.py).
To add a new talk or edit an existing speaker:
1. Open `data/talks.py`.
2. Add a new dictionary object to the `TALKS` list following the structure:
   ```python
   {
       "id": "talk-9",
       "title": "Your Custom Talk Title",
       "time": "04:35 PM - 05:20 PM",
       "category_id": "cat-1",
       "category_name": "Category 1: Cloud & DevOps Infrastructure",
       "description": "Talk overview description...",
       "speakers": [
           {
               "first_name": "Jane",
               "last_name": "Doe",
               "role": "Cloud Architect",
               "company": "Google",
               "linkedin_url": "https://www.linkedin.com/in/janedoe"
           }
       ]
   }
   ```

### Modifying Design & Styling
- Styles are located in [`static/css/style.css`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/static/css/style.css).
- Theme colors and CSS variables are configured under `:root`.

### Modifying HTML Layout & Templates
- HTML template is located in [`templates/index.html`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/templates/index.html).

### Modifying Search & Interactive Filtering
- Interactive logic is located in [`static/js/main.js`](file:///Users/jimtyhurst/src/gemini/20260725-agent-engineering/agent_engineering/my-work/class-02/conference-website/static/js/main.js).
