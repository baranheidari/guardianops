from flask import Flask, jsonify, render_template
import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__, template_folder='templates', static_folder='static')

EVENTS = [
    {"id":1,"timestamp":"2026-04-20 03:14:22","source_ip":"185.234.219.42","event_type":"Unauthorized API Call","severity":"HIGH",    "status":"Auto-Blocked", "region":"us-east-1","ip_type":"external"},
    {"id":2,"timestamp":"2026-04-20 07:55:10","source_ip":"10.0.0.45",     "event_type":"Unusual S3 Access",    "severity":"MEDIUM",  "status":"Investigating","region":"us-east-1","ip_type":"internal"},
    {"id":3,"timestamp":"2026-04-20 11:02:47","source_ip":"203.0.113.99",  "event_type":"Brute Force Attempt",  "severity":"CRITICAL","status":"Auto-Blocked", "region":"us-west-2","ip_type":"external"},
    {"id":4,"timestamp":"2026-04-20 13:30:01","source_ip":"10.0.1.12",     "event_type":"IAM Policy Change",    "severity":"LOW",     "status":"Resolved",     "region":"us-east-1","ip_type":"internal"},
    {"id":5,"timestamp":"2026-04-21 02:11:05","source_ip":"198.51.100.77", "event_type":"Port Scan Detected",   "severity":"HIGH",    "status":"Investigating","region":"us-east-2","ip_type":"external"},
    {"id":6,"timestamp":"2026-04-21 08:44:33","source_ip":"10.0.2.88",     "event_type":"Privilege Escalation", "severity":"CRITICAL","status":"Auto-Blocked", "region":"us-east-1","ip_type":"internal"},
]

def get_stats():
    return {
        "total":        len(EVENTS),
        "critical":     sum(1 for e in EVENTS if e["severity"]=="CRITICAL"),
        "high":         sum(1 for e in EVENTS if e["severity"]=="HIGH"),
        "medium":       sum(1 for e in EVENTS if e["severity"]=="MEDIUM"),
        "low":          sum(1 for e in EVENTS if e["severity"]=="LOW"),
        "blocked":      sum(1 for e in EVENTS if e["status"]=="Auto-Blocked"),
        "investigating":sum(1 for e in EVENTS if e["status"]=="Investigating"),
        "resolved":     sum(1 for e in EVENTS if e["status"]=="Resolved"),
        "ext":          sum(1 for e in EVENTS if e["ip_type"]=="external"),
    }

def now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4))).strftime("%Y-%m-%d %H:%M:%S EDT")

@app.route("/")
def dashboard():
    s = get_stats()
    return render_template("dashboard.html", ts=now(), recent=EVENTS[-4:], **s)

@app.route("/events")
def events_page():
    s = get_stats()
    return render_template("events.html", events=EVENTS,
        ext_count=s["ext"], int_count=s["total"]-s["ext"])

@app.route("/stats")
def stats_page():
    return render_template("stats.html", ts=now(), **get_stats())

@app.route("/playbooks")
def playbooks_page():
    return render_template("playbooks.html")

@app.route("/health-ui")
def health_ui():
    return render_template("health.html", ts=now(), total=len(EVENTS))

@app.route("/health")
def health():
    return jsonify({"status":"healthy","service":"guardianops","version":"6.0","events":len(EVENTS)})

@app.route("/api/events")
def api_events():
    return jsonify(EVENTS)

@app.route("/api/stats")
def api_stats():
    return jsonify(get_stats())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
