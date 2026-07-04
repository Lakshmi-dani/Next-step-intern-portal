from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "nextstep_secret_key"

# Simple in-memory data store
interns = [
    {"id": 1, "name": "Alex Johnson", "department": "Engineering", "start_date": "2026-06-01", "status": "Active"},
    {"id": 2, "name": "Maria Garcia", "department": "Design", "start_date": "2026-06-15", "status": "Active"},
    {"id": 3, "name": "James Lee", "department": "Marketing", "start_date": "2026-07-01", "status": "Pending"},
]

tasks = [
    {"id": 1, "intern_id": 1, "title": "Onboarding Documentation", "status": "Completed", "due_date": "2026-06-05"},
    {"id": 2, "intern_id": 1, "title": "Project Setup", "status": "In Progress", "due_date": "2026-07-10"},
    {"id": 3, "intern_id": 2, "title": "Design System Review", "status": "Completed", "due_date": "2026-06-20"},
    {"id": 4, "intern_id": 3, "title": "Team Introduction", "status": "Pending", "due_date": "2026-07-05"},
]

announcements = [
    {"id": 1, "title": "Welcome to NextStep!", "body": "We're excited to have all our interns join us this summer.", "date": "2026-06-01"},
    {"id": 2, "title": "Intern Hackathon", "body": "Join us on July 15th for our annual intern hackathon.", "date": "2026-06-28"},
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    stats = {
        "total_interns": len(interns),
        "active": sum(1 for i in interns if i["status"] == "Active"),
        "pending": sum(1 for i in interns if i["status"] == "Pending"),
        "tasks_done": sum(1 for t in tasks if t["status"] == "Completed"),
    }
    return render_template("dashboard.html", stats=stats, announcements=announcements[:2])

@app.route("/interns")
def interns_list():
    return render_template("interns.html", interns=interns)

@app.route("/interns/<int:intern_id>")
def intern_detail(intern_id):
    intern = next((i for i in interns if i["id"] == intern_id), None)
    if not intern:
        return redirect(url_for("interns_list"))
    intern_tasks = [t for t in tasks if t["intern_id"] == intern_id]
    return render_template("intern_detail.html", intern=intern, tasks=intern_tasks)

@app.route("/tasks")
def tasks_list():
    enriched = []
    for t in tasks:
        intern = next((i for i in interns if i["id"] == t["intern_id"]), {})
        enriched.append({**t, "intern_name": intern.get("name", "Unknown")})
    return render_template("tasks.html", tasks=enriched)

@app.route("/announcements")
def announcements_list():
    return render_template("announcements.html", announcements=announcements)

@app.route("/api/stats")
def api_stats():
    return jsonify({
        "interns": len(interns),
        "active": sum(1 for i in interns if i["status"] == "Active"),
        "tasks_completed": sum(1 for t in tasks if t["status"] == "Completed"),
        "tasks_pending": sum(1 for t in tasks if t["status"] == "Pending"),
    })

if __name__ == "__main__":
    app.run(debug=True)
