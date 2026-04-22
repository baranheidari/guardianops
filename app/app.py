from flask import Flask, jsonify, render_template_string
import datetime

app = Flask(__name__)

EVENTS = [
    {"id": 1, "timestamp": "2026-04-20 03:14:22", "source_ip": "185.234.219.42", "event_type": "Unauthorized API Call", "severity": "HIGH", "status": "Auto-Blocked", "region": "us-east-1"},
    {"id": 2, "timestamp": "2026-04-20 07:55:10", "source_ip": "10.0.0.45", "event_type": "Unusual S3 Access", "severity": "MEDIUM", "status": "Investigating", "region": "us-east-1"},
    {"id": 3, "timestamp": "2026-04-20 11:02:47", "source_ip": "203.0.113.99", "event_type": "Brute Force Attempt", "severity": "CRITICAL", "status": "Auto-Blocked", "region": "us-west-2"},
    {"id": 4, "timestamp": "2026-04-20 13:30:01", "source_ip": "10.0.1.12", "event_type": "IAM Policy Change", "severity": "LOW", "status": "Resolved", "region": "us-east-1"}
]

FAVICON = '''<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgcng9IjE1IiBmaWxsPSIjMGEwZTFhIi8+PHRleHQgeT0iLjllbSIgZm9udC1zaXplPSI4NSIgeD0iMTAiIGZpbGw9IiMwMGZmODgiPkc8L3RleHQ+PC9zdmc+">'''

CSS = '''<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: Segoe UI, sans-serif; background: #0a0e1a; color: #e0e6f0; }
    nav { background: #0d1117; border-bottom: 1px solid #00ff88; padding: 15px 30px; display: flex; align-items: center; justify-content: space-between; }
    nav .logo { font-size: 1.4rem; font-weight: bold; color: #00ff88; }
    nav .logo span { color: #fff; }
    nav ul { list-style: none; display: flex; gap: 30px; }
    nav ul li a { color: #8892a4; text-decoration: none; font-size: 0.9rem; padding: 8px 16px; border-radius: 4px; transition: all 0.2s; border: 1px solid transparent; }
    nav ul li a:hover, nav ul li a.active { background: #00ff8820; color: #00ff88; border: 1px solid #00ff8840; }
    .hero { padding: 40px 30px 20px; border-bottom: 1px solid #1a2035; }
    .hero h1 { font-size: 1.8rem; color: #fff; }
    .hero p { color: #8892a4; margin-top: 5px; font-size: 0.9rem; }
    .badge { display: inline-block; background: #00ff8815; color: #00ff88; border: 1px solid #00ff8840; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; margin-left: 10px; }
    .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; padding: 30px; }
    .stat-card { background: #0d1117; border: 1px solid #1a2035; border-radius: 8px; padding: 20px; text-align: center; }
    .stat-card .number { font-size: 2.5rem; font-weight: bold; }
    .stat-card .label { font-size: 0.8rem; color: #8892a4; margin-top: 5px; }
    .critical .number { color: #ff4444; }
    .high .number { color: #ff8800; }
    .medium .number { color: #ffcc00; }
    .blocked .number { color: #00ff88; }
    .section { padding: 20px 30px 30px; }
    .section h2 { font-size: 1rem; color: #8892a4; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #1a2035; }
    table { width: 100%; border-collapse: collapse; background: #0d1117; border-radius: 8px; overflow: hidden; }
    th { background: #0a0e1a; color: #8892a4; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; padding: 12px 15px; text-align: left; }
    td { padding: 12px 15px; font-size: 0.88rem; border-bottom: 1px solid #1a2035; }
    tr:last-child td { border-bottom: none; }
    .sev { padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; }
    .CRITICAL { background: #ff444420; color: #ff4444; border: 1px solid #ff444440; }
    .HIGH { background: #ff880020; color: #ff8800; border: 1px solid #ff880040; }
    .MEDIUM { background: #ffcc0020; color: #ffcc00; border: 1px solid #ffcc0040; }
    .LOW { background: #8892a420; color: #8892a4; border: 1px solid #8892a440; }
    .stbadge { padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; }
    .ab { background: #00ff8815; color: #00ff88; border: 1px solid #00ff8840; }
    .inv { background: #ffcc0015; color: #ffcc00; border: 1px solid #ffcc0040; }
    .res { background: #8892a415; color: #8892a4; border: 1px solid #8892a440; }
    .health-card { background: #0d1117; border: 1px solid #00ff8840; border-radius: 8px; padding: 20px; display: flex; align-items: center; gap: 15px; margin: 0 30px 30px; }
    .hdot { width: 12px; height: 12px; background: #00ff88; border-radius: 50%; box-shadow: 0 0 8px #00ff88; animation: pulse 2s infinite; }
    @keyframes pulse { 0%,100%{opacity:1}50%{opacity:0.5} }
    .htext h3 { color: #00ff88; font-size: 0.9rem; }
    .htext p { color: #8892a4; font-size: 0.8rem; margin-top: 2px; }
    .api-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 15px; }
    .api-card { background: #0d1117; border: 1px solid #1a2035; border-radius: 8px; padding: 20px; }
    .api-card h3 { color: #00ff88; font-size: 0.9rem; margin-bottom: 8px; }
    .ep { font-family: monospace; font-size: 0.8rem; color: #8892a4; background: #0a0e1a; padding: 8px; border-radius: 4px; margin-bottom: 10px; }
    .api-card p { font-size: 0.8rem; color: #8892a4; margin-bottom: 12px; }
    .api-card a { display: inline-block; background: #00ff8815; color: #00ff88; border: 1px solid #00ff8840; padding: 6px 14px; border-radius: 4px; font-size: 0.8rem; text-decoration: none; }
    .info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 15px; }
    .info-card { background: #0d1117; border: 1px solid #1a2035; border-radius: 8px; padding: 20px; }
    .info-card h3 { color: #00ff88; font-size: 0.85rem; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; }
    .info-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #1a2035; font-size: 0.85rem; }
    .info-row:last-child { border-bottom: none; }
    .info-row .key { color: #8892a4; }
    .info-row .val { color: #e0e6f0; font-weight: 500; }
    .val.green { color: #00ff88; }
    footer { text-align: center; padding: 20px; color: #8892a420; font-size: 0.75rem; border-top: 1px solid #1a2035; }
</style>'''

NAV = '''<nav><div class="logo">Guardian<span>Ops</span></div><ul>
    <li><a href="/" class="{{ 'active' if active == 'dashboard' else '' }}">Dashboard</a></li>
    <li><a href="/events" class="{{ 'active' if active == 'events' else '' }}">Security Events</a></li>
    <li><a href="/stats" class="{{ 'active' if active == 'stats' else '' }}">Statistics</a></li>
    <li><a href="/health-ui" class="{{ 'active' if active == 'health' else '' }}">Health Check</a></li>
</ul></nav>'''

def HEAD(title):
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {FAVICON}<title>{title}</title>{CSS}</head><body>{NAV}'''

def sb(s):
    if s == "Auto-Blocked": return f'<span class="stbadge ab">{s}</span>'
    if s == "Investigating": return f'<span class="stbadge inv">{s}</span>'
    return f'<span class="stbadge res">{s}</span>'

def rows():
    return "".join([f'''<tr><td>{e["id"]}</td><td>{e["timestamp"]}</td><td>{e["source_ip"]}</td>
    <td>{e["event_type"]}</td><td><span class="sev {e["severity"]}">{e["severity"]}</span></td>
    <td>{sb(e["status"])}</td><td>{e["region"]}</td></tr>''' for e in EVENTS])

@app.route("/")
def dashboard():
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(HEAD("GuardianOps") + f'''
    <div class="hero"><h1>Security Dashboard <span class="badge">LIVE</span></h1>
    <p>AI-Powered Cloud Security Platform — us-east-1 | Last updated: {ts}</p></div>
    <div class="stats">
        <div class="stat-card critical"><div class="number">1</div><div class="label">Critical Threats</div></div>
        <div class="stat-card high"><div class="number">1</div><div class="label">High Severity</div></div>
        <div class="stat-card medium"><div class="number">1</div><div class="label">Medium Severity</div></div>
        <div class="stat-card blocked"><div class="number">2</div><div class="label">Auto-Blocked</div></div>
    </div>
    <div class="health-card"><div class="hdot"></div><div class="htext">
        <h3>All Systems Operational</h3>
        <p>Running on AWS EKS v1.30 — 2 pods healthy — Load Balancer active</p></div></div>
    <div class="section"><h2>Recent Security Events</h2>
    <table><thead><tr><th>#</th><th>Timestamp</th><th>Source IP</th><th>Event Type</th>
    <th>Severity</th><th>Status</th><th>Region</th></tr></thead>
    <tbody>{rows()}</tbody></table></div>
    <div class="section"><h2>API Endpoints</h2><div class="api-cards">
        <div class="api-card"><h3>Security Events</h3><div class="ep">GET /events</div>
        <p>Visual security events page.</p><a href="/events">View Page</a></div>
        <div class="api-card"><h3>Statistics</h3><div class="ep">GET /stats</div>
        <p>Security statistics dashboard.</p><a href="/stats">View Page</a></div>
        <div class="api-card"><h3>Health Check</h3><div class="ep">GET /health-ui</div>
        <p>System health and infrastructure.</p><a href="/health-ui">View Page</a></div>
    </div></div>
    <footer>GuardianOps v4.0 — AWS EKS + Kubernetes — Built by Baran Heidari</footer>
    </body></html>''', active="dashboard")

@app.route("/events")
def events_page():
    return render_template_string(HEAD("Security Events — GuardianOps") + f'''
    <div class="hero"><h1>Security Events <span class="badge">{len(EVENTS)} Total</span></h1>
    <p>All detected security events across your cloud infrastructure</p></div>
    <div class="section"><h2>All Security Events</h2>
    <table><thead><tr><th>#</th><th>Timestamp</th><th>Source IP</th><th>Event Type</th>
    <th>Severity</th><th>Status</th><th>Region</th></tr></thead>
    <tbody>{rows()}</tbody></table></div>
    <footer>GuardianOps v4.0 — AWS EKS + Kubernetes</footer></body></html>''', active="events")

@app.route("/stats")
def stats_page():
    return render_template_string(HEAD("Statistics — GuardianOps") + '''
    <div class="hero"><h1>Statistics <span class="badge">Live</span></h1>
    <p>Aggregated security metrics and threat intelligence</p></div>
    <div class="stats">
        <div class="stat-card critical"><div class="number">1</div><div class="label">Critical</div></div>
        <div class="stat-card high"><div class="number">1</div><div class="label">High</div></div>
        <div class="stat-card medium"><div class="number">1</div><div class="label">Medium</div></div>
        <div class="stat-card blocked"><div class="number">1</div><div class="label">Low</div></div>
    </div>
    <div class="section"><h2>Detailed Breakdown</h2><div class="info-grid">
        <div class="info-card"><h3>Threat Summary</h3>
            <div class="info-row"><span class="key">Total Events</span><span class="val">4</span></div>
            <div class="info-row"><span class="key">Auto-Blocked</span><span class="val green">2</span></div>
            <div class="info-row"><span class="key">Investigating</span><span class="val">1</span></div>
            <div class="info-row"><span class="key">Resolved</span><span class="val">1</span></div>
            <div class="info-row"><span class="key">Uptime</span><span class="val green">100%</span></div>
        </div>
        <div class="info-card"><h3>Infrastructure</h3>
            <div class="info-row"><span class="key">Platform</span><span class="val green">AWS EKS v1.30</span></div>
            <div class="info-row"><span class="key">Pods Running</span><span class="val green">2 / 2</span></div>
            <div class="info-row"><span class="key">Nodes</span><span class="val green">2 (t3.medium)</span></div>
            <div class="info-row"><span class="key">Region</span><span class="val">us-east-1</span></div>
            <div class="info-row"><span class="key">Load Balancer</span><span class="val green">Active</span></div>
        </div>
    </div></div>
    <footer>GuardianOps v4.0 — AWS EKS + Kubernetes</footer></body></html>''', active="stats")

@app.route("/health-ui")
def health_ui():
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(HEAD("Health — GuardianOps") + f'''
    <div class="hero"><h1>Health Check <span class="badge">Healthy</span></h1>
    <p>System status as of {ts}</p></div>
    <div class="health-card"><div class="hdot"></div><div class="htext">
        <h3>All Systems Operational</h3>
        <p>All services running normally on AWS EKS</p></div></div>
    <div class="section"><h2>Service Status</h2><div class="info-grid">
        <div class="info-card"><h3>Application</h3>
            <div class="info-row"><span class="key">Service</span><span class="val green">guardianops</span></div>
            <div class="info-row"><span class="key">Version</span><span class="val">4.0</span></div>
            <div class="info-row"><span class="key">Status</span><span class="val green">Healthy</span></div>
            <div class="info-row"><span class="key">Last Check</span><span class="val">{ts}</span></div>
        </div>
        <div class="info-card"><h3>Kubernetes</h3>
            <div class="info-row"><span class="key">Cluster</span><span class="val green">guardianops-cluster</span></div>
            <div class="info-row"><span class="key">Version</span><span class="val">EKS v1.30</span></div>
            <div class="info-row"><span class="key">Pods</span><span class="val green">2 Running</span></div>
            <div class="info-row"><span class="key">Replicas</span><span class="val green">2/2 Ready</span></div>
        </div>
    </div></div>
    <footer>GuardianOps v4.0 — AWS EKS + Kubernetes</footer></body></html>''', active="health")

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "guardianops", "version": "4.0"})

@app.route("/api/events")
def api_events():
    return jsonify(EVENTS)

@app.route("/api/stats")
def api_stats():
    return jsonify({"total_events": 4, "critical": 1, "high": 1, "medium": 1, "low": 1,
        "auto_blocked": 2, "investigating": 1, "resolved": 1, "uptime": "100%", "region": "us-east-1"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
