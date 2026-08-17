"""
Flask Web Server for Google Cloud Technical Conference Website
"""

from flask import Flask, render_template, jsonify, request
from data.talks import CONFERENCE_INFO, CATEGORIES, TALKS

app = Flask(__name__)

@app.route("/")
def index():
    """Render the main conference schedule homepage."""
    # Count total talks (excluding lunch break)
    actual_talks = [t for t in TALKS if not t.get("is_break")]
    
    # Collect all unique speakers across all talks
    speakers_list = []
    for talk in actual_talks:
        for s in talk.get("speakers", []):
            full_name = f"{s['first_name']} {s['last_name']}"
            if not any(sp["name"] == full_name for sp in speakers_list):
                speakers_list.append({
                    "name": full_name,
                    "role": s.get("role", ""),
                    "company": s.get("company", ""),
                    "linkedin": s.get("linkedin_url", "")
                })

    stats = {
        "total_talks": len(actual_talks),
        "total_speakers": len(speakers_list),
        "total_categories": len(CATEGORIES)
    }

    return render_template(
        "index.html",
        info=CONFERENCE_INFO,
        categories=CATEGORIES,
        talks=TALKS,
        stats=stats
    )

@app.route("/api/talks")
def get_talks():
    """API endpoint to fetch or filter talks data dynamically."""
    query = request.args.get("q", "").strip().lower()
    cat_filter = request.args.get("category", "").strip()

    filtered_talks = []
    
    for talk in TALKS:
        # Keep lunch break visible unless searching specifically
        if talk.get("is_break"):
            if not query and (not cat_filter or cat_filter == "all"):
                filtered_talks.append(talk)
            continue

        # Filter by Category
        if cat_filter and cat_filter != "all":
            # Match by cat-1 / cat-2 or Category 1 / Category 2
            talk_cat_id = talk.get("category_id", "")
            talk_cat_name = talk.get("category_name", "").lower()
            if cat_filter not in [talk_cat_id, "cat-1" if "category 1" in cat_filter.lower() else "cat-2" if "category 2" in cat_filter.lower() else ""]:
                if cat_filter.lower() not in talk_cat_name:
                    continue

        # Filter by Query (Title, Description, Speaker Names)
        if query:
            title_match = query in talk.get("title", "").lower()
            desc_match = query in talk.get("description", "").lower()
            speaker_match = any(
                query in s.get("first_name", "").lower() or
                query in s.get("last_name", "").lower() or
                query in f"{s.get('first_name', '')} {s.get('last_name', '')}".lower()
                for s in talk.get("speakers", [])
            )
            if not (title_match or desc_match or speaker_match):
                continue

        filtered_talks.append(talk)

    return jsonify({
        "success": True,
        "count": len([t for t in filtered_talks if not t.get("is_break")]),
        "talks": filtered_talks
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)

