from flask import Flask, jsonify, render_template_string
import datetime
import os

app = Flask(__name__)

# ─────────────────────────────────────────
# This will later come from RDS PostgreSQL
# For now it's hardcoded so we can test fast
# ─────────────────────────────────────────
security_events = [
    {
        "id": 1,
        "timestamp": "2026-04-20 03:14:22",
        "source_ip": "185.234.219.42",
        "event_type": "Unauthorized API Call",
        "severity": "HIGH",
        "status": "Auto-Blocked",
        "region": "us-east-1"
    },
    {
        "id": 2,
        "timestamp": "2026-04-20 07:55:10",
        "source_ip": "10.0.0.45",
        "event_type": "Unusual S3 Access",
        "severity": "MEDIUM",
        "status": "Investigating",
        "region": "us-east-1"
    },
    {
        "id": 3,
        "timestamp": "2026-04-20 11:02:47",
        "source_ip": "203.0.113.99",
        "event_type": "Brute Force Attempt",
        "severity": "CRITICAL",
        "status": "Auto-Blocked",
        "region": "us-west-2"
    },
    {
        "id": 4,
        "timestamp": "2026-04-20 13:30:01",
        "source_ip": "10.0.1.12",
        "event_type": "IAM Policy Change",
        "severity": "LOW",
        "status": "Resolved",
        "region": "us-east-1"
    },
]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>GuardianOps — Security Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #0a0e1a;
            color: #e2e8f0;
            padding: 40px;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 20px;
        }
        h1 { color: #38bdf8; font-size: 28px; }
        h1 span { color: #f87171; }
        .subtitle { color: #64748b; margin-top: 4px; font-size: 14px; }
        .stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: #1e293b;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid;
        }
        .stat-card.critical { border-color: #f87171; }
        .stat-card.high     { border-color: #fb923c; }
        .stat-card.medium   { border-color: #facc15; }
        .stat-card.blocked  { border-color: #4ade80; }
        .stat-number { font-size: 32px; font-weight: bold; margin-bottom: 4px; }
        .stat-label  { font-size: 13px; color: #64748b; }
        table { width: 100%; border-collapse: collapse; }
        th {
            background: #1e293b;
            padding: 14px 16px;
            text-align: left;
            color: #38bdf8;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        td { padding: 14px 16px; border-bottom: 1px solid #1e293b; font-size: 14px; }
        tr:hover td { background: #1e293b55; }
        .badge {
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }
        .CRITICAL { background: #f8717133; color: #f87171; }
        .HIGH     { background: #fb923c33; color: #fb923c; }
        .MEDIUM   { background: #facc1533; color: #facc15; }
        .LOW      { background: #4ade8033; color: #4ade80; }
        .blocked-badge  { background: #4ade8033; color: #4ade80; }
        .investigating  { background: #facc1533; color: #facc15; }
        .resolved       { background: #38bdf833; color: #38bdf8; }
        .footer { margin-top: 20px; color: #64748b; font-size: 13px; }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Guardian<span>Ops</span></h1>
            <div class="subtitle">
                AI-Powered Cloud Security Platform — us-east-1
            </div>
        </div>
        <div style="color:#64748b; font-size:13px;">
            Last updated: {{ time }}
        </div>
    </div>

    <div class="stats">
        <div class="stat-card critical">
            <div class="stat-number" style="color:#f87171">1</div>
            <div class="stat-label">Critical Threats</div>
        </div>
        <div class="stat-card high">
            <div class="stat-number" style="color:#fb923c">1</div>
            <div class="stat-label">High Severity</div>
        </div>
        <div class="stat-card medium">
            <div class="stat-number" style="color:#facc15">1</div>
            <div class="stat-label">Medium Severity</div>
        </div>
        <div class="stat-card blocked">
            <div class="stat-number" style="color:#4ade80">2</div>
            <div class="stat-label">Auto-Blocked</div>
        </div>
    </div>

    <table>
        <tr>
            <th>#</th>
            <th>Timestamp</th>
            <th>Source IP</th>
            <th>Event Type</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Region</th>
        </tr>
        {% for event in events %}
        <tr>
            <td>{{ event.id }}</td>
            <td style="color:#64748b">{{ event.timestamp }}</td>
            <td style="font-family:monospace">{{ event.source_ip }}</td>
            <td>{{ event.event_type }}</td>
            <td>
                <span class="badge {{ event.severity }}">
                    {{ event.severity }}
                </span>
            </td>
            <td>
                <span class="badge
                    {%- if event.status == 'Auto-Blocked' %} blocked-badge
                    {%- elif event.status == 'Investigating' %} investigating
                    {%- else %} resolved{% endif %}">
                    {{ event.status }}
                </span>
            </td>
            <td style="color:#64748b">{{ event.region }}</td>
        </tr>
        {% endfor %}
    </table>

    <div class="footer">
        GuardianOps v1.0 — Built on AWS EKS + Bedrock AI
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(
        HTML,
        events=security_events,
        time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "guardianops",
        "version": "1.0"
    }), 200

@app.route('/api/events')
def api_events():
    return jsonify(security_events)

@app.route('/api/stats')
def api_stats():
    return jsonify({
        "total": len(security_events),
        "critical": sum(1 for e in security_events if e["severity"] == "CRITICAL"),
        "high": sum(1 for e in security_events if e["severity"] == "HIGH"),
        "auto_blocked": sum(1 for e in security_events if e["status"] == "Auto-Blocked")
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
