from flask import Flask, render_template_string, jsonify
import json

app = Flask(__name__)

# ─── SHARED CSS + JS ──────────────────────────────────────────────────────────
SHARED_CSS = """
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg: #f8f9fa;
  --surface: #ffffff;
  --border: #e5e7eb;
  --border-light: #f0f1f3;
  --text: #111827;
  --text-2: #6b7280;
  --text-3: #9ca3af;
  --accent: #10b981;
  --accent-dim: #d1fae5;
  --critical: #ef4444;
  --critical-dim: #fee2e2;
  --high: #f97316;
  --high-dim: #ffedd5;
  --medium: #eab308;
  --medium-dim: #fef9c3;
  --low: #6b7280;
  --low-dim: #f3f4f6;
  --info: #3b82f6;
  --sidebar-w: 220px;
  --header-h: 56px;
  --mono: 'IBM Plex Mono', monospace;
  --sans: 'IBM Plex Sans', sans-serif;
}

body {
  font-family: var(--sans);
  background: var(--bg);
  color: var(--text);
  font-size: 14px;
  line-height: 1.5;
  overflow-x: hidden;
}

/* ── SIDEBAR ── */
.sidebar {
  position: fixed; left: 0; top: 0; bottom: 0;
  width: var(--sidebar-w);
  background: var(--surface);
  border-right: 1px solid var(--border);
  display: flex; flex-direction: column;
  z-index: 100;
}

.sidebar-brand {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  text-decoration: none;
}

.brand-icon {
  width: 36px; height: 36px;
  background: var(--text);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.brand-icon svg { width: 20px; height: 20px; }

.brand-text { line-height: 1.2; }
.brand-name { font-size: 15px; font-weight: 600; color: var(--text); }
.brand-name span { color: var(--accent); }
.brand-sub { font-size: 9px; font-weight: 500; letter-spacing: .08em;
             text-transform: uppercase; color: var(--text-3); }

.sidebar-section { padding: 20px 10px 8px; }
.sidebar-label {
  font-size: 10px; font-weight: 600; letter-spacing: .1em;
  text-transform: uppercase; color: var(--text-3);
  padding: 0 8px; margin-bottom: 4px;
}

.sidebar-nav { list-style: none; }
.sidebar-nav li a {
  display: flex; align-items: center; gap: 8px;
  padding: 7px 8px; border-radius: 6px;
  text-decoration: none; color: var(--text-2);
  font-size: 13.5px; font-weight: 400;
  transition: all .15s;
  position: relative;
}
.sidebar-nav li a:hover { background: var(--bg); color: var(--text); }
.sidebar-nav li a.active {
  background: var(--accent-dim); color: var(--accent);
  font-weight: 500;
}
.sidebar-nav li a svg { width: 16px; height: 16px; flex-shrink: 0; }

.nav-badge {
  margin-left: auto;
  background: var(--critical);
  color: #fff;
  font-size: 10px; font-weight: 600;
  padding: 1px 5px; border-radius: 10px;
  font-family: var(--mono);
}
.nav-badge.green { background: var(--accent); }
.nav-badge.orange { background: var(--high); }
.nav-badge.gray { background: var(--text-3); color: #fff; }

.sidebar-live {
  display: flex; align-items: center; gap: 6px;
  padding: 7px 8px; margin: 0 0;
}
.live-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--accent);
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: .4; }
}

.sidebar-footer {
  margin-top: auto;
  padding: 12px 10px;
  border-top: 1px solid var(--border);
}
.sidebar-user {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 8px; border-radius: 6px;
  cursor: pointer;
}
.sidebar-user:hover { background: var(--bg); }
.user-avatar {
  width: 28px; height: 28px; border-radius: 50%;
  background: var(--accent);
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 600; color: #fff;
  flex-shrink: 0;
}
.user-info { flex: 1; min-width: 0; }
.user-name { font-size: 13px; font-weight: 500; color: var(--text);
             white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-role { font-size: 11px; color: var(--text-3); }
.user-logout { color: var(--text-3); }
.user-logout:hover { color: var(--text); }

/* ── TOPBAR ── */
.topbar {
  position: fixed; top: 0; left: var(--sidebar-w); right: 0;
  height: var(--header-h);
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 12px;
  padding: 0 20px;
  z-index: 90;
}

.search-wrap {
  flex: 1; max-width: 480px;
  position: relative;
}
.search-wrap svg {
  position: absolute; left: 10px; top: 50%; transform: translateY(-50%);
  color: var(--text-3); width: 15px; height: 15px;
}
.search-input {
  width: 100%; padding: 7px 36px 7px 32px;
  background: var(--bg); border: 1px solid var(--border);
  border-radius: 7px; font-family: var(--sans); font-size: 13px;
  color: var(--text); outline: none;
  transition: border-color .15s;
}
.search-input:focus { border-color: var(--accent); }
.search-input::placeholder { color: var(--text-3); }
.search-kbd {
  position: absolute; right: 8px; top: 50%; transform: translateY(-50%);
  font-family: var(--mono); font-size: 10px; color: var(--text-3);
  background: var(--border-light); padding: 1px 4px; border-radius: 3px;
}

.topbar-spacer { flex: 1; }

.ingestion-badge {
  display: flex; align-items: center; gap: 6px;
  background: var(--accent-dim); border: 1px solid var(--accent);
  border-radius: 20px; padding: 4px 10px;
  font-size: 12px; font-weight: 500; color: var(--accent);
  font-family: var(--mono);
}
.ingestion-badge::before {
  content: '';
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--accent);
}

.topbar-actions { display: flex; align-items: center; gap: 4px; }
.topbar-btn {
  width: 32px; height: 32px; border-radius: 7px;
  border: 1px solid var(--border); background: var(--surface);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: var(--text-2);
  transition: all .15s;
}
.topbar-btn:hover { background: var(--bg); color: var(--text); }
.topbar-btn svg { width: 16px; height: 16px; }
.topbar-btn.notif { position: relative; }
.notif-dot {
  position: absolute; top: 5px; right: 5px;
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--critical);
  border: 1.5px solid var(--surface);
}

/* ── MAIN CONTENT ── */
.main {
  margin-left: var(--sidebar-w);
  padding-top: var(--header-h);
  min-height: 100vh;
}

.page-header {
  padding: 24px 28px 0;
}
.page-title {
  font-size: 22px; font-weight: 600; color: var(--text);
  display: flex; align-items: baseline; gap: 8px;
}
.page-title span { color: var(--text-3); font-weight: 400; }
.page-subtitle {
  font-size: 13px; color: var(--text-2); margin-top: 3px;
}

.page-actions { display: flex; align-items: center; gap: 8px; }

.btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 7px 14px; border-radius: 7px;
  font-family: var(--sans); font-size: 13px; font-weight: 500;
  cursor: pointer; border: none; text-decoration: none;
  transition: all .15s;
}
.btn-primary { background: var(--accent); color: #fff; }
.btn-primary:hover { background: #0ea574; }
.btn-outline {
  background: var(--surface); border: 1px solid var(--border);
  color: var(--text-2);
}
.btn-outline:hover { border-color: var(--text-3); color: var(--text); }
.btn-danger { background: var(--critical-dim); color: var(--critical); border: 1px solid var(--critical); }
.btn-danger:hover { background: var(--critical); color: #fff; }
.btn svg { width: 14px; height: 14px; }

.page-content { padding: 20px 28px 40px; }

/* ── CARDS / METRICS ── */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.metric-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px 20px;
  position: relative;
  overflow: hidden;
}
.metric-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
}
.metric-card.critical::before { background: var(--critical); }
.metric-card.high::before { background: var(--high); }
.metric-card.medium::before { background: var(--medium); }
.metric-card.success::before { background: var(--accent); }

.metric-label {
  font-size: 11px; font-weight: 600; letter-spacing: .08em;
  text-transform: uppercase; color: var(--text-3);
  margin-bottom: 8px;
}
.metric-value {
  font-size: 32px; font-weight: 700; color: var(--text);
  font-family: var(--mono); line-height: 1;
  margin-bottom: 6px;
}
.metric-card.critical .metric-value { color: var(--critical); }
.metric-card.high .metric-value { color: var(--high); }
.metric-card.medium .metric-value { color: var(--medium); }
.metric-card.success .metric-value { color: var(--accent); }

.metric-delta {
  font-size: 12px; color: var(--text-3);
  display: flex; align-items: center; gap: 4px;
}
.metric-delta.up { color: var(--critical); }
.metric-delta.down { color: var(--accent); }

.metric-sparkline {
  position: absolute; bottom: 0; right: 0;
  width: 80px; height: 40px; opacity: .15;
}

/* ── TABLE ── */
.data-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}

.data-card-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 18px;
  border-bottom: 1px solid var(--border);
}
.data-card-title {
  font-size: 12px; font-weight: 600; letter-spacing: .07em;
  text-transform: uppercase; color: var(--text-3);
}

table { width: 100%; border-collapse: collapse; }
th {
  text-align: left; padding: 10px 16px;
  font-size: 11px; font-weight: 600; letter-spacing: .07em;
  text-transform: uppercase; color: var(--text-3);
  border-bottom: 1px solid var(--border);
  background: var(--bg);
}
td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-light);
  font-size: 13px; color: var(--text);
  vertical-align: middle;
}
tr:last-child td { border-bottom: none; }
tr:hover td { background: var(--bg); }

.event-num { font-family: var(--mono); color: var(--text-3); font-size: 12px; }
.event-ts { font-family: var(--mono); font-size: 12px; color: var(--text-2); }

.ip-tag {
  font-family: var(--mono); font-size: 12px;
  font-weight: 500;
}
.ip-tag.ext { color: var(--critical); }
.ip-tag.int { color: var(--info); }

.tag-badge {
  display: inline-flex; align-items: center;
  padding: 1px 5px; border-radius: 3px;
  font-family: var(--mono); font-size: 10px; font-weight: 500;
  margin-left: 4px;
}
.tag-badge.ext { background: var(--critical-dim); color: var(--critical); }
.tag-badge.int { background: #dbeafe; color: var(--info); }
.tag-badge.mitre { background: #f3f4f6; color: var(--text-2); }

.sev-badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 8px; border-radius: 4px;
  font-size: 11px; font-weight: 600;
}
.sev-badge::before {
  content: ''; width: 5px; height: 5px; border-radius: 50%;
}
.sev-badge.critical { background: var(--critical-dim); color: var(--critical); }
.sev-badge.critical::before { background: var(--critical); }
.sev-badge.high { background: var(--high-dim); color: var(--high); }
.sev-badge.high::before { background: var(--high); }
.sev-badge.medium { background: var(--medium-dim); color: #a16207; }
.sev-badge.medium::before { background: var(--medium); }
.sev-badge.low { background: var(--low-dim); color: var(--low); }
.sev-badge.low::before { background: var(--low); }

.status-badge {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 12px; font-weight: 500;
}
.status-badge::before {
  content: ''; width: 6px; height: 6px; border-radius: 50%;
}
.status-badge.blocked { color: var(--accent); }
.status-badge.blocked::before { background: var(--accent); }
.status-badge.investigating { color: var(--high); }
.status-badge.investigating::before { background: var(--high); }
.status-badge.resolved { color: var(--text-3); }
.status-badge.resolved::before { background: var(--text-3); }

/* ── COMPLIANCE ── */
.compliance-grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 16px; margin-bottom: 24px;
}
.compliance-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px 20px;
}
.compliance-title { font-size: 14px; font-weight: 600; color: var(--text); }
.compliance-sub { font-size: 11px; color: var(--text-3); margin-bottom: 12px; }
.compliance-score {
  font-size: 36px; font-weight: 700;
  font-family: var(--mono);
  float: right; margin-top: -4px;
}
.compliance-score.green { color: var(--accent); }
.compliance-score.orange { color: var(--high); }
.compliance-score.yellow { color: var(--medium); }
.compliance-bar {
  height: 6px; background: var(--border);
  border-radius: 3px; margin: 12px 0 8px; overflow: hidden;
}
.compliance-fill { height: 100%; border-radius: 3px; }
.compliance-fill.green { background: var(--accent); }
.compliance-fill.orange { background: var(--high); }
.compliance-fill.yellow { background: var(--medium); }
.compliance-stats { display: flex; gap: 12px; font-size: 12px; color: var(--text-2); }
.compliance-stats span { font-weight: 500; }
.compliance-stats .pass { color: var(--accent); }
.compliance-stats .fail { color: var(--critical); }
.compliance-stats .warn { color: var(--medium); }

/* ── LIVE STREAM ── */
.live-stream-header {
  display: flex; align-items: center; gap: 8px;
  font-size: 12px; font-weight: 600; letter-spacing: .07em;
  text-transform: uppercase; color: var(--text-3);
}
.events-count-badge {
  background: var(--accent-dim);
  border: 1px solid var(--accent);
  color: var(--accent);
  font-size: 11px; font-weight: 600; font-family: var(--mono);
  padding: 2px 8px; border-radius: 12px;
  display: flex; align-items: center; gap: 5px;
}
.events-count-badge::before {
  content: ''; width: 5px; height: 5px; border-radius: 50%;
  background: var(--accent); animation: pulse 2s infinite;
}

/* ── POSTURE SIDEBAR ── */
.dashboard-layout {
  display: grid; grid-template-columns: 1fr 280px; gap: 20px;
}
.posture-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px 20px;
}
.posture-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 16px;
}
.posture-title {
  font-size: 11px; font-weight: 600; letter-spacing: .07em;
  text-transform: uppercase; color: var(--text-3);
}
.posture-link { font-size: 12px; color: var(--accent); text-decoration: none; }
.posture-link:hover { text-decoration: underline; }

.score-ring {
  display: flex; align-items: center; gap: 14px;
  margin-bottom: 16px;
}
.score-ring svg { width: 72px; height: 72px; flex-shrink: 0; }
.score-strong { font-size: 14px; font-weight: 600; color: var(--text); }
.score-tip { font-size: 12px; color: var(--text-2); margin-top: 3px; }

.posture-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 0;
  border-top: 1px solid var(--border-light);
  font-size: 13px;
}
.posture-row-key { color: var(--text-2); }
.posture-row-val { font-weight: 500; color: var(--text); }
.posture-row-val.green { color: var(--accent); }
.posture-row-val.link { color: var(--accent); text-decoration: none; }

/* ── FILTERS BAR ── */
.filters-bar {
  display: flex; align-items: center; gap: 8px;
  padding: 16px 0 12px; flex-wrap: wrap;
}
.filter-input {
  padding: 7px 12px; border-radius: 7px;
  border: 1px solid var(--border); background: var(--surface);
  font-family: var(--sans); font-size: 13px; color: var(--text);
  outline: none; width: 260px;
}
.filter-input:focus { border-color: var(--accent); }
.filter-btn {
  padding: 6px 12px; border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface); cursor: pointer;
  font-size: 12px; font-weight: 500; color: var(--text-2);
  transition: all .15s;
}
.filter-btn:hover { background: var(--bg); }
.filter-btn.active-filter {
  background: var(--accent-dim); border-color: var(--accent);
  color: var(--accent);
}
.filter-btn.critical-f { background: var(--critical-dim); border-color: var(--critical); color: var(--critical); }
.filter-btn.high-f { background: var(--high-dim); border-color: var(--high); color: var(--high); }
.filter-btn.medium-f { background: var(--medium-dim); border-color: #ca8a04; color: #a16207; }
.filter-btn.low-f { background: var(--low-dim); border-color: var(--text-3); color: var(--low); }

/* ── ALERT TOAST ── */
.alert-toast {
  position: fixed; top: 68px; right: 20px;
  background: var(--surface);
  border: 1px solid var(--critical);
  border-radius: 10px;
  padding: 12px 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,.1);
  z-index: 200;
  display: flex; align-items: flex-start; gap: 10px;
  min-width: 280px; max-width: 340px;
  animation: slideIn .3s ease;
}
@keyframes slideIn {
  from { transform: translateX(30px); opacity: 0; }
  to   { transform: translateX(0);    opacity: 1; }
}
.toast-icon {
  width: 28px; height: 28px; border-radius: 6px;
  background: var(--critical-dim);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.toast-icon svg { width: 14px; height: 14px; color: var(--critical); }
.toast-title { font-size: 13px; font-weight: 600; color: var(--text); }
.toast-msg { font-size: 12px; color: var(--text-2); margin-top: 2px; }

/* ── PLAYBOOKS ── */
.playbooks-grid {
  display: grid; grid-template-columns: repeat(2, 1fr);
  gap: 16px; margin-bottom: 24px;
}
.playbook-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px 20px;
  display: flex; flex-direction: column; gap: 10px;
}
.playbook-card-top {
  display: flex; align-items: flex-start; gap: 12px;
}
.pb-icon {
  width: 36px; height: 36px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.pb-icon.destructive { background: var(--critical-dim); color: var(--critical); }
.pb-icon.safe { background: var(--accent-dim); color: var(--accent); }
.pb-icon svg { width: 18px; height: 18px; }
.pb-name { font-size: 14px; font-weight: 600; color: var(--text); }
.pb-desc { font-size: 12px; color: var(--text-2); }
.playbook-card-bottom {
  display: flex; align-items: center; justify-content: space-between;
  border-top: 1px solid var(--border-light);
  padding-top: 10px;
}
.pb-meta { font-size: 11px; color: var(--text-3); font-family: var(--mono); }
.pb-meta.destructive { color: var(--critical); }
.pb-meta.safe { color: var(--accent); }
.btn-execute {
  padding: 6px 14px; border-radius: 6px;
  font-size: 12px; font-weight: 600; cursor: pointer;
  border: 1px solid; transition: all .15s;
  display: flex; align-items: center; gap: 4px;
}
.btn-execute.destructive {
  background: var(--critical-dim); border-color: var(--critical);
  color: var(--critical);
}
.btn-execute.destructive:hover { background: var(--critical); color: #fff; }
.btn-execute.safe {
  background: var(--accent-dim); border-color: var(--accent);
  color: var(--accent);
}
.btn-execute.safe:hover { background: var(--accent); color: #fff; }

/* ── ROADMAP ── */
.roadmap-table td:last-child {
  font-weight: 500; color: var(--accent); font-size: 12px;
  text-align: right;
}
.roadmap-table td:last-child.inprog { color: var(--high); }

/* ── ALERT RULES ── */
.rule-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 18px;
  margin-bottom: 12px;
  display: flex; align-items: flex-start; gap: 14px;
}
.rule-toggle {
  width: 36px; height: 20px; border-radius: 10px;
  background: var(--border); cursor: pointer;
  position: relative; flex-shrink: 0; margin-top: 2px;
  border: none; transition: background .2s;
}
.rule-toggle.on { background: var(--accent); }
.rule-toggle::after {
  content: '';
  position: absolute; top: 2px; left: 2px;
  width: 16px; height: 16px; border-radius: 50%;
  background: #fff;
  transition: transform .2s;
}
.rule-toggle.on::after { transform: translateX(16px); }
.rule-name { font-size: 14px; font-weight: 600; color: var(--text); }
.rule-expr { font-size: 12px; color: var(--text-2); margin-top: 2px; font-family: var(--mono); }
.rule-expr .keyword { color: var(--info); }
.rule-expr .value { color: var(--accent); }
.rule-fires { font-size: 12px; color: var(--text-3); margin-left: auto; white-space: nowrap; }
.rule-fires strong { color: var(--critical); }

.code-block {
  background: #1e1e2e; color: #cdd6f4;
  border-radius: 8px; padding: 14px 16px;
  font-family: var(--mono); font-size: 12px;
  line-height: 1.7; overflow-x: auto;
}
.code-block .kw { color: #89b4fa; }
.code-block .str { color: #a6e3a1; }
.code-block .fn { color: #cba6f7; }
.code-block .comment { color: #6c7086; }

.available-fields {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 18px;
}
.fields-title {
  font-size: 11px; font-weight: 600; letter-spacing: .07em;
  text-transform: uppercase; color: var(--text-3); margin-bottom: 10px;
}
.field-row {
  display: flex; justify-content: space-between;
  align-items: center;
  padding: 6px 0; border-top: 1px solid var(--border-light);
  font-size: 13px;
}
.field-name { color: var(--text); font-family: var(--mono); }
.field-values { color: var(--text-3); font-size: 11px; }

/* ── INTEGRATIONS ── */
.integrations-grid {
  display: grid; grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}
.integration-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 18px;
  display: flex; align-items: center; gap: 14px;
}
.int-icon {
  width: 40px; height: 40px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; font-weight: 700; color: #fff;
  flex-shrink: 0;
}
.int-icon.slack { background: #4a154b; }
.int-icon.pd { background: #06ac38; }
.int-icon.gh { background: #24292e; }
.int-icon.jira { background: #0052cc; }
.int-icon.dd { background: #632ca6; }
.int-icon.sp { background: #ff5733; }
.int-name { font-size: 14px; font-weight: 600; color: var(--text); }
.int-desc { font-size: 12px; color: var(--text-2); }
.int-action { margin-left: auto; flex-shrink: 0; }
.btn-connect {
  padding: 6px 14px; border-radius: 6px;
  font-size: 12px; font-weight: 500; cursor: pointer;
  transition: all .15s; display: flex; align-items: center; gap: 5px;
  border: 1px solid var(--border);
  background: var(--surface); color: var(--text-2);
}
.btn-connect:hover { border-color: var(--text-3); color: var(--text); }
.btn-disconnect {
  padding: 6px 14px; border-radius: 6px;
  font-size: 12px; font-weight: 500; cursor: pointer;
  transition: all .15s;
  border: 1px solid var(--border);
  background: var(--surface); color: var(--text-2);
}
.btn-disconnect:hover { background: var(--critical-dim); border-color: var(--critical); color: var(--critical); }

/* ── USERS ── */
.role-badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 8px; border-radius: 4px;
  font-size: 11px; font-weight: 600;
}
.role-badge::before { content: '•'; }
.role-badge.admin { background: var(--critical-dim); color: var(--critical); }
.role-badge.responder { background: var(--medium-dim); color: #a16207; }
.role-badge.analyst { background: #dbeafe; color: var(--info); }
.role-badge.readonly { background: var(--low-dim); color: var(--low); }
.role-badge.automation { background: var(--accent-dim); color: var(--accent); }

.mfa-check { color: var(--accent); }
.mfa-dash { color: var(--text-3); }

/* ── API KEYS ── */
.scope-badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 8px; border-radius: 4px;
  font-size: 11px; font-weight: 600;
}
.scope-badge::before { content: '•'; }
.scope-badge.write { background: var(--high-dim); color: var(--high); }
.scope-badge.read { background: var(--accent-dim); color: var(--accent); }
.key-token { font-family: var(--mono); font-size: 12px; color: var(--text-2); }
.key-ts { font-family: var(--mono); font-size: 12px; color: var(--text-2); }

/* ── HEALTH ── */
.health-status-banner {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 14px; border-radius: 20px;
  background: var(--accent-dim); border: 1px solid var(--accent);
  color: var(--accent); font-size: 12px; font-weight: 600;
}
.health-status-banner::before {
  content: ''; width: 7px; height: 7px; border-radius: 50%;
  background: var(--accent); animation: pulse 2s infinite;
}

.health-grid {
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 16px; margin-bottom: 20px;
}
.health-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px; padding: 18px 20px;
}
.health-card-label {
  font-size: 11px; font-weight: 600; letter-spacing: .07em;
  text-transform: uppercase; color: var(--text-3); margin-bottom: 6px;
}
.health-card-value {
  font-size: 28px; font-weight: 700; font-family: var(--mono);
  color: var(--accent);
}
.health-card-value.ok { color: var(--text); }

.progress-bar {
  height: 5px; background: var(--border); border-radius: 3px;
  overflow: hidden; width: 70px;
}
.progress-fill { height: 100%; border-radius: 3px; background: var(--accent); }
.progress-fill.warn { background: var(--high); }

/* ── STATS ── */
.stats-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.sev-bar-row {
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 10px;
}
.sev-bar-label { font-size: 12px; font-weight: 600; text-transform: uppercase;
                  width: 70px; color: var(--text-2); }
.sev-bar-track { flex: 1; height: 10px; background: var(--border); border-radius: 5px; overflow: hidden; }
.sev-bar-fill { height: 100%; border-radius: 5px; }
.sev-bar-fill.critical { background: var(--critical); }
.sev-bar-fill.high { background: var(--high); }
.sev-bar-fill.medium { background: var(--medium); }
.sev-bar-fill.low { background: var(--low); }
.sev-bar-stat { font-family: var(--mono); font-size: 11px; color: var(--text-2); width: 55px; text-align: right; }

.infra-table td:first-child { color: var(--text-2); font-size: 13px; }
.infra-table td:last-child { text-align: right; font-weight: 500; font-size: 13px; }
.infra-table td:last-child.link { color: var(--accent); }

.region-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
}
.region-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px; padding: 14px 16px;
}
.region-name { font-family: var(--mono); font-size: 12px; color: var(--text-2); }
.region-count { font-size: 28px; font-weight: 700; font-family: var(--mono); color: var(--text); }
.region-label { font-size: 11px; color: var(--text-3); }

/* ── LAYOUT HELPERS ── */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.half { display: grid; grid-template-columns: 3fr 2fr; gap: 20px; }

.section-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 14px;
}
.section-title {
  font-size: 11px; font-weight: 600; letter-spacing: .07em;
  text-transform: uppercase; color: var(--text-3);
}

a.view-all {
  font-size: 12px; color: var(--accent); text-decoration: none;
}
a.view-all:hover { text-decoration: underline; }

.empty-state {
  padding: 30px; text-align: center;
  color: var(--text-3); font-size: 13px;
}

.page-header-row {
  display: flex; align-items: flex-start; justify-content: space-between;
  padding: 24px 28px 0;
}
"""

# ─── LAYOUT TEMPLATE ──────────────────────────────────────────────────────────
def layout(page, content, toast=None, badge_overrides=None):
    badges = {
        'dashboard': '6 D', 'events': None, 'statistics': '6 S',
        'playbooks': '6 P', 'alert_rules': '6 R', 'integrations': '6 I',
        'users': '6 U', 'api_keys': '6 K', 'health': '6 H'
    }
    if badge_overrides:
        badges.update(badge_overrides)

    def nav_badge(key, cls=''):
        b = badges.get(key)
        if not b: return ''
        c = 'green' if 'D' in b or 'S' in b or 'H' in b else ('orange' if 'P' in b or 'R' in b else 'gray')
        return f'<span class="nav-badge {c}">{b}</span>'

    def nav_item(key, label, href, icon_path, live=False):
        active = 'active' if page == key else ''
        live_badge = f'<span class="nav-badge green" style="font-size:9px;padding:1px 4px;">LIVE</span>' if live else ''
        return f'''<li><a href="{href}" class="{active}">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="{icon_path}"/>
            </svg>
            {label}{live_badge}{nav_badge(key)}
        </a></li>'''

    toast_html = ''
    if toast:
        toast_html = f'''<div class="alert-toast" id="toast">
          <div class="toast-icon">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M8 2L2 13h12L8 2zm0 4v3m0 2.5v.5"/>
            </svg>
          </div>
          <div>
            <div class="toast-title">Critical threat detected</div>
            <div class="toast-msg">{toast}</div>
          </div>
        </div>
        <script>setTimeout(()=>document.getElementById('toast')?.remove(), 6000)</script>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GuardianOps — Cloud Security Console</title>
<style>{SHARED_CSS}</style>
</head>
<body>

<!-- SIDEBAR -->
<aside class="sidebar">
  <a class="sidebar-brand" href="/">
    <div class="brand-icon">
      <svg viewBox="0 0 20 20" fill="none" stroke="white" stroke-width="1.5">
        <path d="M10 2L3 6v5c0 4 3 7 7 8 4-1 7-4 7-8V6L10 2z"/>
        <path d="M7 10l2 2 4-4" stroke="#10b981" stroke-width="1.8"/>
      </svg>
    </div>
    <div class="brand-text">
      <div class="brand-name">Guardian<span>Ops</span></div>
      <div class="brand-sub">Cloud Security Console</div>
    </div>
  </a>

  <div class="sidebar-section">
    <div class="sidebar-label">Monitor</div>
    <ul class="sidebar-nav">
      {nav_item('dashboard','Dashboard','/',
        'M2 2h5v5H2zm7 0h5v5H9zm-7 7h5v5H2zm7 0h5v5H9z')}
      {nav_item('events','Events','/events',
        'M2 4h12M2 8h8M2 12h10', live=True)}
      {nav_item('statistics','Statistics','/statistics',
        'M2 12l3-4 3 2 3-6 3 5')}
    </ul>
  </div>

  <div class="sidebar-section">
    <div class="sidebar-label">Respond</div>
    <ul class="sidebar-nav">
      {nav_item('playbooks','Playbooks','/playbooks',
        'M4 2h8l2 2v12H2V2h2zm2 5h4m-4 3h4m-4 3h2')}
      {nav_item('alert_rules','Alert rules','/alert-rules',
        'M8 2a6 6 0 100 12A6 6 0 008 2zm0 3v4m0 2v.5')}
      {nav_item('integrations','Integrations','/integrations',
        'M10 3H6a2 2 0 00-2 2v6a2 2 0 002 2h4m2-8l3 3-3 3m-6 0V5')}
    </ul>
  </div>

  <div class="sidebar-section">
    <div class="sidebar-label">Administer</div>
    <ul class="sidebar-nav">
      {nav_item('users','Users &amp; roles','/users',
        'M8 8a3 3 0 100-6 3 3 0 000 6zm-5 6a5 5 0 0110 0H3z')}
      {nav_item('api_keys','API keys','/api-keys',
        'M7 11a3 3 0 100-6 3 3 0 000 6zm4-3h5m-2-2l2 2-2 2')}
      {nav_item('health','Health','/health',
        'M2 8h2l2-4 2 8 2-6 2 4h2')}
    </ul>
  </div>

  <div class="sidebar-footer">
    <div class="sidebar-user">
      <div class="user-avatar">BH</div>
      <div class="user-info">
        <div class="user-name">Baran Heidari</div>
        <div class="user-role">sec-ops-responder</div>
      </div>
      <svg class="user-logout" viewBox="0 0 16 16" fill="none" stroke="currentColor"
           stroke-width="1.5" width="16" height="16">
        <path d="M11 5l3 3-3 3M7 8h7M6 3H3v10h3"/>
      </svg>
    </div>
  </div>
</aside>

<!-- TOPBAR -->
<header class="topbar">
  <div class="search-wrap">
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
      <circle cx="7" cy="7" r="4"/><path d="m11 11 3 3"/>
    </svg>
    <input class="search-input" placeholder="Search events, IPs, playbooks… (⌘K or /)">
    <span class="search-kbd">⌘K</span>
  </div>
  <div class="topbar-spacer"></div>
  <span class="ingestion-badge">Ingestion &lt; 500 ms</span>
  <div class="topbar-actions">
    <button class="topbar-btn">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="8" cy="8" r="3"/><path d="M8 1v1m0 12v1M1 8h1m12 0h1m-2.05-5.95-.7.7M3.05 12.95l-.7.7m0-10.6.7.7m10.6 10.6-.7-.7"/>
      </svg>
    </button>
    <button class="topbar-btn">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
        <rect x="2" y="3" width="12" height="9" rx="1"/><path d="M5 15h6"/>
      </svg>
    </button>
    <button class="topbar-btn notif">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M8 2a4 4 0 00-4 4v3l-1 2h10l-1-2V6a4 4 0 00-4-4zm-1 10a1 1 0 002 0"/>
      </svg>
      <span class="notif-dot"></span>
    </button>
    <button class="topbar-btn">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M2 4h4v4H2zm6 0h4v4H8zm-6 6h4v4H2zm6 0h4v4H8z"/>
      </svg>
    </button>
    <button class="topbar-btn">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="8" cy="8" r="2"/><path d="M8 2v1m0 10v1M2 8h1m10 0h1"/>
      </svg>
    </button>
  </div>
</header>

<!-- CONTENT -->
<main class="main">
  {toast_html}
  {content}
</main>

</body>
</html>'''


# ─── DASHBOARD ────────────────────────────────────────────────────────────────
@app.route('/')
def dashboard():
    content = '''
<div class="page-header-row">
  <div>
    <h1 class="page-title">Security overview <span>/ us-east-1</span></h1>
    <p class="page-subtitle">Real-time threat posture across EKS cluster guardianops-cluster.
       Ingestion latency &lt; 500 ms. Press <kbd>?</kbd> for shortcuts.</p>
  </div>
  <div class="page-actions">
    <span style="display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:500;color:var(--accent);">
      <span style="width:7px;height:7px;border-radius:50%;background:var(--accent);animation:pulse 2s infinite;display:inline-block;"></span>
      Live
    </span>
    <button class="btn btn-outline" style="font-size:12px;padding:5px 10px;">EKS v1.30</button>
    <button class="btn btn-outline" style="font-size:12px;padding:5px 10px;">2 / 2 pods</button>
    <button class="btn btn-outline" style="font-size:12px;padding:5px 10px;">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" width="13" height="13">
        <path d="M3 8v5h10V8M8 2v8m-3-3l3 3 3-3"/>
      </svg> Export
    </button>
  </div>
</div>

<div class="page-content">
  <!-- Metric Cards -->
  <div class="metrics-grid">
    <div class="metric-card critical">
      <div class="metric-label">Critical Threats</div>
      <div class="metric-value">9</div>
      <div class="metric-delta up">▲ 2 vs last 24h</div>
      <svg class="metric-sparkline" viewBox="0 0 80 40">
        <polyline points="5,35 15,25 25,30 35,15 45,20 55,10 65,18 75,12" fill="none" stroke="#ef4444" stroke-width="2"/>
      </svg>
    </div>
    <div class="metric-card high">
      <div class="metric-label">High Severity</div>
      <div class="metric-value">10</div>
      <div class="metric-delta up">▲ 1 vs last 24h</div>
      <svg class="metric-sparkline" viewBox="0 0 80 40">
        <polyline points="5,30 15,20 25,25 35,18 45,22 55,15 65,20 75,14" fill="none" stroke="#f97316" stroke-width="2"/>
      </svg>
    </div>
    <div class="metric-card medium">
      <div class="metric-label">Medium Severity</div>
      <div class="metric-value">12</div>
      <div class="metric-delta down">▼ 3 vs last 24h</div>
      <svg class="metric-sparkline" viewBox="0 0 80 40">
        <polyline points="5,15 15,25 25,18 35,28 45,20 55,30 65,22 75,26" fill="none" stroke="#eab308" stroke-width="2"/>
      </svg>
    </div>
    <div class="metric-card success">
      <div class="metric-label">Auto-Blocked</div>
      <div class="metric-value">18</div>
      <div class="metric-delta up" style="color:var(--accent);">▲ 4 vs last 24h</div>
      <svg class="metric-sparkline" viewBox="0 0 80 40">
        <polyline points="5,35 15,28 25,32 35,20 45,25 55,15 65,10 75,8" fill="none" stroke="#10b981" stroke-width="2"/>
      </svg>
    </div>
  </div>

  <!-- Compliance Posture -->
  <div style="margin-bottom:20px;">
    <div class="section-header">
      <div class="section-title">Compliance Posture</div>
      <a class="view-all" href="#">View all controls →</a>
    </div>
    <div class="compliance-grid">
      <div class="compliance-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
          <div>
            <div class="compliance-title">CIS AWS Foundations</div>
            <div class="compliance-sub">v1.5.0</div>
          </div>
          <div class="compliance-score green">92</div>
        </div>
        <div class="compliance-bar"><div class="compliance-fill green" style="width:92%"></div></div>
        <div class="compliance-stats">
          <span><span class="pass">47 pass</span></span>
          <span><span class="fail">4 fail</span></span>
          <span><span class="warn">0 warn</span></span>
        </div>
      </div>
      <div class="compliance-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
          <div>
            <div class="compliance-title">SOC 2 Type II</div>
            <div class="compliance-sub">Trust Services</div>
          </div>
          <div class="compliance-score orange">88</div>
        </div>
        <div class="compliance-bar"><div class="compliance-fill orange" style="width:88%"></div></div>
        <div class="compliance-stats">
          <span><span class="pass">32 pass</span></span>
          <span><span class="fail">3 fail</span></span>
          <span><span class="warn">1 warn</span></span>
        </div>
      </div>
      <div class="compliance-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
          <div>
            <div class="compliance-title">NIST CSF</div>
            <div class="compliance-sub">v2.0</div>
          </div>
          <div class="compliance-score yellow">85</div>
        </div>
        <div class="compliance-bar"><div class="compliance-fill yellow" style="width:85%"></div></div>
        <div class="compliance-stats">
          <span><span class="pass">58 pass</span></span>
          <span><span class="fail">6 fail</span></span>
          <span><span class="warn">4 warn</span></span>
        </div>
      </div>
    </div>
  </div>

  <!-- Live Stream + Posture -->
  <div class="dashboard-layout">
    <div>
      <div class="section-header">
        <div class="live-stream-header">
          Live Event Stream
        </div>
        <span class="events-count-badge">35 events</span>
      </div>
      <div class="data-card">
        <table>
          <thead>
            <tr>
              <th>#</th><th>Timestamp</th><th>Source IP</th>
              <th>Event</th><th>Severity</th><th>Status</th><th>Region</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="event-num">78926</td>
              <td class="event-ts">2026-04-29 16:08:46</td>
              <td><span class="ip-tag ext">101.114.113.197</span><span class="tag-badge ext">EXT</span></td>
              <td>Egress Anomaly <span class="tag-badge mitre">T1078</span></td>
              <td><span class="sev-badge critical">CRITICAL</span></td>
              <td><span class="status-badge blocked">Auto-Blocked</span></td>
              <td style="font-family:var(--mono);font-size:11px;">us-east-1</td>
            </tr>
            <tr>
              <td class="event-num">78917</td>
              <td class="event-ts">2026-04-29 16:08:37</td>
              <td><span class="ip-tag ext">176.25.110.74</span><span class="tag-badge ext">EXT</span></td>
              <td>Malformed JWT <span class="tag-badge mitre">T1059</span></td>
              <td><span class="sev-badge medium">MEDIUM</span></td>
              <td><span class="status-badge investigating">Investigating</span></td>
              <td style="font-family:var(--mono);font-size:11px;">ap-south-1</td>
            </tr>
            <tr>
              <td class="event-num">78903</td>
              <td class="event-ts">2026-04-29 16:08:23</td>
              <td><span class="ip-tag ext">91.119.157.66</span><span class="tag-badge ext">EXT</span></td>
              <td>Egress Anomaly <span class="tag-badge mitre">T1078</span></td>
              <td><span class="sev-badge medium">MEDIUM</span></td>
              <td><span class="status-badge resolved">Resolved</span></td>
              <td style="font-family:var(--mono);font-size:11px;">us-west-2</td>
            </tr>
            <tr>
              <td class="event-num">78891</td>
              <td class="event-ts">2026-04-29 16:08:11</td>
              <td><span class="ip-tag int">10.0.1.145</span><span class="tag-badge int">INT</span></td>
              <td>Unusual S3 Access <span class="tag-badge mitre">T1059</span></td>
              <td><span class="sev-badge high">HIGH</span></td>
              <td><span class="status-badge blocked">Auto-Blocked</span></td>
              <td style="font-family:var(--mono);font-size:11px;">us-west-2</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Posture Card -->
    <div>
      <div class="posture-card">
        <div class="posture-header">
          <div class="posture-title">Posture</div>
          <a class="posture-link" href="#">Report →</a>
        </div>
        <div class="score-ring">
          <svg viewBox="0 0 72 72">
            <circle cx="36" cy="36" r="30" fill="none" stroke="#e5e7eb" stroke-width="7"/>
            <circle cx="36" cy="36" r="30" fill="none" stroke="#10b981" stroke-width="7"
              stroke-dasharray="168 188" stroke-linecap="round"
              transform="rotate(-90 36 36)"/>
            <text x="36" y="41" text-anchor="middle" font-size="14" font-weight="700"
                  font-family="IBM Plex Mono" fill="#111827">87</text>
          </svg>
          <div>
            <div class="score-strong">Strong posture</div>
            <div class="score-tip">3 controls need review. Enable MFA for svc-deploy to reach 92.</div>
          </div>
        </div>
        <div class="posture-row">
          <span class="posture-row-key">Cluster</span>
          <span class="posture-row-val">guardianops-cluster</span>
        </div>
        <div class="posture-row">
          <span class="posture-row-key">Nodes</span>
          <a class="posture-row-val green posture-row-val link" href="#">2 × t3.medium</a>
        </div>
        <div class="posture-row">
          <span class="posture-row-key">Load balancer</span>
          <a class="posture-row-val green posture-row-val link" href="#">ELB →</a>
        </div>
      </div>
    </div>
  </div>
</div>
'''
    return render_template_string(layout('dashboard', content))


# ─── EVENTS ───────────────────────────────────────────────────────────────────
@app.route('/events')
def events():
    content = '''
<div class="page-header-row">
  <div>
    <h1 class="page-title">Events <span>/ 39 shown</span></h1>
    <p class="page-subtitle">All events across regions. Source: CloudTrail + VPC flow logs + custom sensors.
       Click a row for incident details.</p>
  </div>
  <div class="page-actions">
    <span style="font-size:12px;color:var(--text-2);">22 EXT</span>
    <span style="font-size:12px;color:var(--text-2);">17 INT</span>
    <button class="btn btn-outline" style="font-size:12px;padding:5px 10px;">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" width="13" height="13">
        <path d="M3 8v5h10V8M8 2v8m-3-3l3 3 3-3"/>
      </svg> Export CSV
    </button>
  </div>
</div>

<div class="page-content">
  <div class="filters-bar">
    <input class="filter-input" placeholder="Filter by IP, type, user, MITRE tag, region…">
    <button class="filter-btn active-filter">All severities</button>
    <button class="filter-btn critical-f">Critical <strong>10</strong></button>
    <button class="filter-btn high-f">High <strong>10</strong></button>
    <button class="filter-btn medium-f">Medium <strong>14</strong></button>
    <button class="filter-btn low-f">Low <strong>5</strong></button>
    <button class="filter-btn active-filter" style="margin-left:8px;">Any status</button>
    <button class="filter-btn">Auto-Blocked</button>
    <button class="filter-btn">Investigating</button>
    <button class="filter-btn">Resolved</button>
  </div>

  <div class="data-card">
    <table>
      <thead>
        <tr>
          <th>#</th><th>Timestamp</th><th>Source IP</th>
          <th>Event</th><th>Severity</th><th>Status</th><th>Region</th>
        </tr>
      </thead>
      <tbody>
        <tr><td class="event-num">78975</td><td class="event-ts">2026-04-29 16:09:35</td>
          <td><span class="ip-tag int">10.0.0.124</span><span class="tag-badge int">INT</span></td>
          <td>Port Scan Detected <span class="tag-badge mitre">T1046</span></td>
          <td><span class="sev-badge critical">CRITICAL</span></td>
          <td><span class="status-badge blocked">Auto-Blocked</span></td>
          <td style="font-family:var(--mono);font-size:11px;">us-west-2</td></tr>
        <tr><td class="event-num">78962</td><td class="event-ts">2026-04-29 16:09:22</td>
          <td><span class="ip-tag ext">192.101.120.109</span><span class="tag-badge ext">EXT</span></td>
          <td>Unusual S3 Access <span class="tag-badge mitre">T1110</span></td>
          <td><span class="sev-badge medium">MEDIUM</span></td>
          <td><span class="status-badge investigating">Investigating</span></td>
          <td style="font-family:var(--mono);font-size:11px;">eu-west-1</td></tr>
        <tr><td class="event-num">78949</td><td class="event-ts">2026-04-29 16:09:09</td>
          <td><span class="ip-tag int">10.0.3.202</span><span class="tag-badge int">INT</span></td>
          <td>Rate Limit Breach <span class="tag-badge mitre">T1098</span></td>
          <td><span class="sev-badge medium">MEDIUM</span></td>
          <td><span class="status-badge resolved">Resolved</span></td>
          <td style="font-family:var(--mono);font-size:11px;">us-east-2</td></tr>
        <tr><td class="event-num">78940</td><td class="event-ts">2026-04-29 16:09:00</td>
          <td><span class="ip-tag ext">104.98.93.132</span><span class="tag-badge ext">EXT</span></td>
          <td>Suspicious DNS Query <span class="tag-badge mitre">T1078</span></td>
          <td><span class="sev-badge low">LOW</span></td>
          <td><span class="status-badge investigating">Investigating</span></td>
          <td style="font-family:var(--mono);font-size:11px;">ap-south-1</td></tr>
        <tr><td class="event-num">78926</td><td class="event-ts">2026-04-29 16:08:46</td>
          <td><span class="ip-tag ext">101.114.113.197</span><span class="tag-badge ext">EXT</span></td>
          <td>Egress Anomaly <span class="tag-badge mitre">T1078</span></td>
          <td><span class="sev-badge critical">CRITICAL</span></td>
          <td><span class="status-badge blocked">Auto-Blocked</span></td>
          <td style="font-family:var(--mono);font-size:11px;">us-east-1</td></tr>
        <tr><td class="event-num">78917</td><td class="event-ts">2026-04-29 16:08:37</td>
          <td><span class="ip-tag ext">176.25.110.74</span><span class="tag-badge ext">EXT</span></td>
          <td>Malformed JWT <span class="tag-badge mitre">T1059</span></td>
          <td><span class="sev-badge medium">MEDIUM</span></td>
          <td><span class="status-badge investigating">Investigating</span></td>
          <td style="font-family:var(--mono);font-size:11px;">ap-south-1</td></tr>
        <tr><td class="event-num">78903</td><td class="event-ts">2026-04-29 16:08:23</td>
          <td><span class="ip-tag ext">91.119.157.66</span><span class="tag-badge ext">EXT</span></td>
          <td>Egress Anomaly <span class="tag-badge mitre">T1078</span></td>
          <td><span class="sev-badge medium">MEDIUM</span></td>
          <td><span class="status-badge resolved">Resolved</span></td>
          <td style="font-family:var(--mono);font-size:11px;">us-west-2</td></tr>
        <tr><td class="event-num">78891</td><td class="event-ts">2026-04-29 16:08:11</td>
          <td><span class="ip-tag int">10.0.1.145</span><span class="tag-badge int">INT</span></td>
          <td>Unusual S3 Access <span class="tag-badge mitre">T1059</span></td>
          <td><span class="sev-badge high">HIGH</span></td>
          <td><span class="status-badge blocked">Auto-Blocked</span></td>
          <td style="font-family:var(--mono);font-size:11px;">us-east-2</td></tr>
        <tr><td class="event-num">78880</td><td class="event-ts">2026-04-29 16:08:00</td>
          <td><span class="ip-tag int">10.0.2.88</span><span class="tag-badge int">INT</span></td>
          <td>Unauthorized API Call <span class="tag-badge mitre">T1190</span></td>
          <td><span class="sev-badge medium">MEDIUM</span></td>
          <td><span class="status-badge investigating">Investigating</span></td>
          <td style="font-family:var(--mono);font-size:11px;">us-east-2</td></tr>
        <tr><td class="event-num">78869</td><td class="event-ts">2026-04-29 16:07:49</td>
          <td><span class="ip-tag ext">122.130.127.30</span><span class="tag-badge ext">EXT</span></td>
          <td>Unusual S3 Access <span class="tag-badge mitre">T1110</span></td>
          <td><span class="sev-badge medium">MEDIUM</span></td>
          <td><span class="status-badge investigating">Investigating</span></td>
          <td style="font-family:var(--mono);font-size:11px;">us-west-2</td></tr>
        <tr><td class="event-num">78859</td><td class="event-ts">2026-04-29 16:07:39</td>
          <td><span class="ip-tag int">10.0.2.86</span><span class="tag-badge int">INT</span></td>
          <td>Token Replay Attack <span class="tag-badge mitre">T1110</span></td>
          <td><span class="sev-badge critical">CRITICAL</span></td>
          <td><span class="status-badge blocked">Auto-Blocked</span></td>
          <td style="font-family:var(--mono);font-size:11px;">us-east-2</td></tr>
      </tbody>
    </table>
  </div>
</div>
'''
    return render_template_string(layout('events', content,
        toast='Port Scan Detected from 10.0.0.124'))


# ─── STATISTICS ───────────────────────────────────────────────────────────────
@app.route('/statistics')
def statistics():
    content = '''
<div class="page-header-row">
  <div>
    <h1 class="page-title">Statistics <span>/ aggregated</span></h1>
    <p class="page-subtitle">Last 24h telemetry from CloudTrail, VPC flow logs, EKS, and ingestion pipeline.</p>
  </div>
  <span class="ingestion-badge">Streaming</span>
</div>

<div class="page-content">
  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-label">Ingestion P95</div>
      <div class="metric-value" style="color:var(--text);">418 <span style="font-size:14px;font-weight:400;color:var(--text-2);">ms</span></div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Page Load P95</div>
      <div class="metric-value" style="color:var(--text);">0.9 <span style="font-size:14px;font-weight:400;color:var(--text-2);">s</span></div>
    </div>
    <div class="metric-card success">
      <div class="metric-label">Uptime / 30d</div>
      <div class="metric-value">100 <span style="font-size:14px;font-weight:400;color:var(--accent);">%</span></div>
    </div>
    <div class="metric-card">
      <div class="metric-label">MTTD Change</div>
      <div class="metric-value" style="color:var(--accent);">-30 <span style="font-size:14px;font-weight:400;">%</span></div>
    </div>
  </div>

  <div class="stats-grid">
    <div>
      <div class="data-card" style="padding:18px 20px;margin-bottom:20px;">
        <div class="section-title" style="margin-bottom:16px;">Severity Distribution</div>
        <div style="font-size:11px;color:var(--text-3);text-align:right;margin-bottom:10px;">40 total</div>
        <div class="sev-bar-row">
          <div class="sev-bar-label">Critical</div>
          <div class="sev-bar-track"><div class="sev-bar-fill critical" style="width:25%"></div></div>
          <div class="sev-bar-stat">10 · 25%</div>
        </div>
        <div class="sev-bar-row">
          <div class="sev-bar-label">High</div>
          <div class="sev-bar-track"><div class="sev-bar-fill high" style="width:25%"></div></div>
          <div class="sev-bar-stat">10 · 25%</div>
        </div>
        <div class="sev-bar-row">
          <div class="sev-bar-label">Medium</div>
          <div class="sev-bar-track"><div class="sev-bar-fill medium" style="width:38%"></div></div>
          <div class="sev-bar-stat">15 · 38%</div>
        </div>
        <div class="sev-bar-row">
          <div class="sev-bar-label">Low</div>
          <div class="sev-bar-track"><div class="sev-bar-fill low" style="width:13%"></div></div>
          <div class="sev-bar-stat">5 · 13%</div>
        </div>
      </div>

      <div class="data-card" style="padding:0;">
        <div class="section-title" style="padding:14px 18px 0;">Region Breakdown</div>
        <div class="region-grid" style="padding:14px 18px 18px;">
          <div class="region-card">
            <div class="region-name">us-east-1</div>
            <div class="region-count">13</div>
            <div class="region-label">events</div>
          </div>
          <div class="region-card">
            <div class="region-name">us-east-2</div>
            <div class="region-count">9</div>
            <div class="region-label">events</div>
          </div>
          <div class="region-card">
            <div class="region-name">us-west-2</div>
            <div class="region-count">7</div>
            <div class="region-label">events</div>
          </div>
          <div class="region-card">
            <div class="region-name">eu-west-1</div>
            <div class="region-count">5</div>
            <div class="region-label">events</div>
          </div>
        </div>
      </div>
    </div>

    <div class="data-card" style="padding:18px 20px;">
      <div class="section-title" style="margin-bottom:16px;">Infrastructure</div>
      <table class="infra-table">
        <tbody>
          <tr><td>Platform</td><td class="link">AWS EKS v1.30</td></tr>
          <tr><td>Pods running</td><td class="link">2 / 2</td></tr>
          <tr><td>Nodes</td><td>2 × t3.medium</td></tr>
          <tr><td>Region</td><td>us-east-1</td></tr>
          <tr><td>Load balancer</td><td class="link">Classic ELB</td></tr>
          <tr><td>Registry</td><td class="link">AWS ECR</td></tr>
          <tr><td>IaC</td><td>Terraform ≥ 1.0</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
'''
    return render_template_string(layout('statistics', content))


# ─── PLAYBOOKS ────────────────────────────────────────────────────────────────
@app.route('/playbooks')
def playbooks():
    content = '''
<div class="page-header-row">
  <div>
    <h1 class="page-title">Playbooks <span>/ response automation</span></h1>
    <p class="page-subtitle">Predefined remediations. RBAC approval required for destructive actions.
       Every run is audit-logged.</p>
  </div>
  <div style="display:flex;align-items:center;gap:8px;">
    <span style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-2);
                 padding:5px 10px;border:1px solid var(--border);border-radius:6px;">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"
           width="13" height="13">
        <circle cx="8" cy="8" r="5"/><path d="M8 5v4l2.5 2"/>
      </svg>
      RBAC enforced
    </span>
  </div>
</div>

<div class="page-content">
  <div class="playbooks-grid">
    <div class="playbook-card">
      <div class="playbook-card-top">
        <div class="pb-icon destructive">
          <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="2" y="5" width="14" height="11" rx="2"/>
            <path d="M6 5V4a3 3 0 016 0v1"/>
          </svg>
        </div>
        <div>
          <div class="pb-name">Quarantine IP</div>
          <div class="pb-desc">Block suspicious IP across all security groups and WAF. Audit logged.</div>
        </div>
      </div>
      <div class="playbook-card-bottom">
        <span class="pb-meta destructive">PB-001 · destructive</span>
        <button class="btn-execute destructive">Execute →</button>
      </div>
    </div>

    <div class="playbook-card">
      <div class="playbook-card-top">
        <div class="pb-icon destructive">
          <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 3l4 4-4 4m0-4H3m10-1v8"/>
          </svg>
        </div>
        <div>
          <div class="pb-name">Rotate access keys</div>
          <div class="pb-desc">Revoke and regenerate IAM access keys. Notifies owner with timestamp.</div>
        </div>
      </div>
      <div class="playbook-card-bottom">
        <span class="pb-meta destructive">PB-002 · destructive</span>
        <button class="btn-execute destructive">Execute →</button>
      </div>
    </div>

    <div class="playbook-card">
      <div class="playbook-card-top">
        <div class="pb-icon destructive">
          <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M3 9h12M9 3l6 6-6 6"/>
          </svg>
        </div>
        <div>
          <div class="pb-name">Revoke active sessions</div>
          <div class="pb-desc">Terminate all active sessions for a user or role immediately.</div>
        </div>
      </div>
      <div class="playbook-card-bottom">
        <span class="pb-meta destructive">PB-003 · destructive</span>
        <button class="btn-execute destructive">Execute →</button>
      </div>
    </div>

    <div class="playbook-card">
      <div class="playbook-card-top">
        <div class="pb-icon safe">
          <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 2L3 5v5c0 3.5 2.5 6 6 7 3.5-1 6-3.5 6-7V5L9 2z"/>
            <path d="M6 9l2 2 4-4"/>
          </svg>
        </div>
        <div>
          <div class="pb-name">Enforce MFA</div>
          <div class="pb-desc">Require MFA for all API calls from a specified role or user group.</div>
        </div>
      </div>
      <div class="playbook-card-bottom">
        <span class="pb-meta safe">PB-004 · safe</span>
        <button class="btn-execute safe">Execute →</button>
      </div>
    </div>

    <div class="playbook-card">
      <div class="playbook-card-top">
        <div class="pb-icon safe">
          <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="2" y="3" width="14" height="12" rx="2"/>
            <path d="M5 7h8M5 10h6M5 13h4"/>
          </svg>
        </div>
        <div>
          <div class="pb-name">Incident report</div>
          <div class="pb-desc">Auto-generate full incident report with timeline and remediation steps.</div>
        </div>
      </div>
      <div class="playbook-card-bottom">
        <span class="pb-meta safe">PB-005 · safe</span>
        <button class="btn-execute safe">Execute →</button>
      </div>
    </div>

    <div class="playbook-card">
      <div class="playbook-card-top">
        <div class="pb-icon safe">
          <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 3v3M3 9H6M12 9h3M9 15v-3m-4.2-8.2l2.1 2.1m5.8 0l2.1-2.1m-9.9 9.9l2.1-2.1m5.8 0l2.1 2.1"/>
          </svg>
        </div>
        <div>
          <div class="pb-name">Escalate to SOC</div>
          <div class="pb-desc">Escalate to Security Operations Center with full evidence package.</div>
        </div>
      </div>
      <div class="playbook-card-bottom">
        <span class="pb-meta safe">PB-006 · safe</span>
        <button class="btn-execute safe">Execute →</button>
      </div>
    </div>
  </div>

  <div class="two-col">
    <div class="data-card">
      <div class="data-card-header">
        <div class="data-card-title">Roadmap</div>
      </div>
      <table class="roadmap-table">
        <tbody>
          <tr><td>P0 · Auto-block hardening</td><td>Live</td></tr>
          <tr><td>P0 · Severity normalization</td><td>Live</td></tr>
          <tr><td>P0 · IP classification</td><td>Live</td></tr>
          <tr><td>P1 · Real-time SSE feed</td><td class="inprog">In progress</td></tr>
          <tr><td>P1 · Smart alert rules</td><td>Live</td></tr>
          <tr><td>P2 · Threat graph</td><td class="inprog">Planned</td></tr>
        </tbody>
      </table>
    </div>
    <div class="data-card" style="padding:18px 20px;">
      <div class="section-title" style="margin-bottom:12px;">Recent Audit Log</div>
      <div class="empty-state">No playbook runs yet. Execute one to see it here.</div>
    </div>
  </div>
</div>
'''
    return render_template_string(layout('playbooks', content))


# ─── ALERT RULES ──────────────────────────────────────────────────────────────
@app.route('/alert-rules')
def alert_rules():
    content = '''
<div class="page-header-row">
  <div>
    <h1 class="page-title">Alert rules <span>/ 4 active</span></h1>
    <p class="page-subtitle">Conditional rules that fire integrations or playbooks on matching events.</p>
  </div>
  <button class="btn btn-primary">
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" width="14" height="14">
      <path d="M8 3v10M3 8h10"/>
    </svg> New rule
  </button>
</div>

<div class="page-content">
  <div class="rule-card">
    <button class="rule-toggle on"></button>
    <div style="flex:1;">
      <div class="rule-name">Page on-call on CRITICAL from external IP</div>
      <div class="rule-expr">
        <span class="keyword">when</span> severity == <span class="value">CRITICAL</span>
        AND iptype == <span class="value">external</span> →
        PagerDuty → SOC-L1
      </div>
    </div>
    <div class="rule-fires"><strong>14</strong> fires · 24h</div>
  </div>

  <div class="rule-card">
    <button class="rule-toggle on"></button>
    <div style="flex:1;">
      <div class="rule-name">Slack #sec-alerts on brute force</div>
      <div class="rule-expr">
        <span class="keyword">when</span> type == <span class="value">'Brute Force Attempt'</span> →
        Slack → #sec-alerts
      </div>
    </div>
    <div class="rule-fires"><strong>8</strong> fires · 24h</div>
  </div>

  <div class="rule-card">
    <button class="rule-toggle on"></button>
    <div style="flex:1;">
      <div class="rule-name">Auto-quarantine port scanners</div>
      <div class="rule-expr">
        <span class="keyword">when</span> type == <span class="value">'Port Scan Detected'</span>
        AND iptype == <span class="value">external</span> →
        Playbook → Quarantine IP
      </div>
    </div>
    <div class="rule-fires"><strong>22</strong> fires · 24h</div>
  </div>

  <div class="rule-card">
    <button class="rule-toggle"></button>
    <div style="flex:1;">
      <div class="rule-name" style="color:var(--text-2);">Notify owner on IAM policy change</div>
      <div class="rule-expr">
        <span class="keyword">when</span> type == <span class="value">'IAM Policy Change'</span> →
        Email → policy-owner
      </div>
    </div>
    <div class="rule-fires"><strong>3</strong> fires · 24h</div>
  </div>

  <div class="rule-card">
    <button class="rule-toggle on"></button>
    <div style="flex:1;">
      <div class="rule-name">Escalate privilege escalation to SOC</div>
      <div class="rule-expr">
        <span class="keyword">when</span> type == <span class="value">'Privilege Escalation'</span> →
        Playbook → Escalate to SOC
      </div>
    </div>
    <div class="rule-fires"><strong>2</strong> fires · 24h</div>
  </div>

  <div class="two-col" style="margin-top:24px;">
    <div>
      <div class="section-title" style="margin-bottom:10px;">Rule Syntax</div>
      <div class="code-block">
<span class="kw">severity</span> == CRITICAL
  <span class="kw">AND</span> iptype == <span class="str">external</span>
  <span class="kw">AND</span> region <span class="kw">IN</span> (<span class="str">'us-east-1'</span>, <span class="str">'eu-west-1'</span>)
<span class="kw">THEN</span> <span class="fn">playbook</span>(<span class="str">'Quarantine IP'</span>)
     <span class="fn">notify</span>(<span class="str">'slack'</span>, <span class="str">'#sec-alerts'</span>)
      </div>
    </div>
    <div class="available-fields">
      <div class="fields-title">Available Fields</div>
      <div class="field-row">
        <span class="field-name">severity</span>
        <span class="field-values">CRITICAL · HIGH · MEDIUM · LOW</span>
      </div>
      <div class="field-row">
        <span class="field-name">iptype</span>
        <span class="field-values">external · internal</span>
      </div>
      <div class="field-row">
        <span class="field-name">type</span>
        <span class="field-values">string</span>
      </div>
      <div class="field-row">
        <span class="field-name">region</span>
        <span class="field-values">aws-region</span>
      </div>
      <div class="field-row">
        <span class="field-name">user</span>
        <span class="field-values">iam-principal</span>
      </div>
      <div class="field-row">
        <span class="field-name">mitre</span>
        <span class="field-values">T1xxx</span>
      </div>
    </div>
  </div>
</div>
'''
    return render_template_string(layout('alert_rules', content))


# ─── INTEGRATIONS ─────────────────────────────────────────────────────────────
@app.route('/integrations')
def integrations():
    content = '''
<div class="page-header-row">
  <div>
    <h1 class="page-title">Integrations <span>/ 3 connected</span></h1>
    <p class="page-subtitle">Route alerts, tickets, and metrics to your existing tools.</p>
  </div>
</div>

<div class="page-content">
  <div class="integrations-grid">
    <div class="integration-card">
      <div class="int-icon slack">S</div>
      <div>
        <div class="int-name">Slack</div>
        <div class="int-desc">Route alerts to #sec-alerts</div>
      </div>
      <div class="int-action">
        <button class="btn-disconnect">Disconnect</button>
      </div>
    </div>

    <div class="integration-card">
      <div class="int-icon pd">PD</div>
      <div>
        <div class="int-name">PagerDuty</div>
        <div class="int-desc">Page on-call for CRITICAL events</div>
      </div>
      <div class="int-action">
        <button class="btn-disconnect">Disconnect</button>
      </div>
    </div>

    <div class="integration-card" style="opacity:.7;">
      <div class="int-icon gh">GH</div>
      <div>
        <div class="int-name">GitHub</div>
        <div class="int-desc">Open issue on misconfig finding</div>
      </div>
      <div class="int-action">
        <button class="btn-connect">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"
               width="12" height="12"><path d="M8 3v10M3 8h10"/></svg>
          Connect
        </button>
      </div>
    </div>

    <div class="integration-card">
      <div class="int-icon jira">J</div>
      <div>
        <div class="int-name">Jira</div>
        <div class="int-desc">Create tickets from incidents</div>
      </div>
      <div class="int-action">
        <button class="btn-disconnect">Disconnect</button>
      </div>
    </div>

    <div class="integration-card" style="opacity:.7;">
      <div class="int-icon dd">DD</div>
      <div>
        <div class="int-name">Datadog</div>
        <div class="int-desc">Forward metrics to Datadog</div>
      </div>
      <div class="int-action">
        <button class="btn-connect">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"
               width="12" height="12"><path d="M8 3v10M3 8h10"/></svg>
          Connect
        </button>
      </div>
    </div>

    <div class="integration-card" style="opacity:.7;">
      <div class="int-icon sp">SP</div>
      <div>
        <div class="int-name">Splunk</div>
        <div class="int-desc">Stream events to Splunk SIEM</div>
      </div>
      <div class="int-action">
        <button class="btn-connect">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"
               width="12" height="12"><path d="M8 3v10M3 8h10"/></svg>
          Connect
        </button>
      </div>
    </div>
  </div>
</div>
'''
    return render_template_string(layout('integrations', content,
        toast='Rate Limit Breach from 10.0.3.140'))


# ─── USERS & ROLES ────────────────────────────────────────────────────────────
@app.route('/users')
def users():
    content = '''
<div class="page-header-row">
  <div>
    <h1 class="page-title">Users &amp; roles</h1>
    <p class="page-subtitle">Manage team access, RBAC assignments, and MFA enforcement.</p>
  </div>
  <button class="btn btn-primary">
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" width="14" height="14">
      <path d="M8 3v10M3 8h10"/>
    </svg> Invite user
  </button>
</div>

<div class="page-content">
  <div class="data-card">
    <table>
      <thead>
        <tr>
          <th>User</th><th>Email</th><th>Role</th><th>MFA</th><th>Status</th><th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="display:flex;align-items:center;gap:8px;">
            <div class="user-avatar" style="width:30px;height:30px;font-size:11px;">BH</div>
            Baran Heidari
          </td>
          <td style="color:var(--text-2);font-size:13px;">baran@guardianops.io</td>
          <td><span class="role-badge admin">Admin</span></td>
          <td><span class="mfa-check">✓</span></td>
          <td><span class="status-badge blocked">Auto-Blocked</span></td>
          <td><button class="btn btn-outline" style="font-size:12px;padding:4px 10px;">Edit</button></td>
        </tr>
        <tr>
          <td style="display:flex;align-items:center;gap:8px;">
            <div class="user-avatar" style="width:30px;height:30px;font-size:11px;background:#f97316;">AD</div>
            Ayo Daramola
          </td>
          <td style="color:var(--text-2);font-size:13px;">ayo@guardianops.io</td>
          <td><span class="role-badge responder">Responder</span></td>
          <td><span class="mfa-check">✓</span></td>
          <td><span class="status-badge blocked">Auto-Blocked</span></td>
          <td><button class="btn btn-outline" style="font-size:12px;padding:4px 10px;">Edit</button></td>
        </tr>
        <tr>
          <td style="display:flex;align-items:center;gap:8px;">
            <div class="user-avatar" style="width:30px;height:30px;font-size:11px;background:#3b82f6;">SY</div>
            Sana Yousef
          </td>
          <td style="color:var(--text-2);font-size:13px;">sana@guardianops.io</td>
          <td><span class="role-badge analyst">Analyst</span></td>
          <td><span class="mfa-check">✓</span></td>
          <td><span class="status-badge blocked">Auto-Blocked</span></td>
          <td><button class="btn btn-outline" style="font-size:12px;padding:4px 10px;">Edit</button></td>
        </tr>
        <tr>
          <td style="display:flex;align-items:center;gap:8px;">
            <div class="user-avatar" style="width:30px;height:30px;font-size:11px;background:#6b7280;">MK</div>
            Marco Kovacs
          </td>
          <td style="color:var(--text-2);font-size:13px;">marco@guardianops.io</td>
          <td><span class="role-badge readonly">Read-only</span></td>
          <td><span class="mfa-dash">—</span></td>
          <td><span class="status-badge blocked">Auto-Blocked</span></td>
          <td><button class="btn btn-outline" style="font-size:12px;padding:4px 10px;">Edit</button></td>
        </tr>
        <tr>
          <td style="display:flex;align-items:center;gap:8px;">
            <div class="user-avatar" style="width:30px;height:30px;font-size:11px;background:#8b5cf6;">SD</div>
            svc-deploy
          </td>
          <td style="color:var(--text-2);font-size:13px;">service-account</td>
          <td><span class="role-badge automation">Automation</span></td>
          <td><span class="mfa-dash">—</span></td>
          <td><span class="status-badge blocked">Auto-Blocked</span></td>
          <td><button class="btn btn-outline" style="font-size:12px;padding:4px 10px;">Edit</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
'''
    return render_template_string(layout('users', content))


# ─── API KEYS ─────────────────────────────────────────────────────────────────
@app.route('/api-keys')
def api_keys():
    content = '''
<div class="page-header-row">
  <div>
    <h1 class="page-title">API keys</h1>
    <p class="page-subtitle">Programmatic access tokens. Rotate regularly — every key is scoped and audit-logged.</p>
  </div>
  <button class="btn btn-primary">
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" width="14" height="14">
      <path d="M8 3v10M3 8h10"/>
    </svg> Generate key
  </button>
</div>

<div class="page-content">
  <div class="data-card">
    <table>
      <thead>
        <tr>
          <th>Name</th><th>Token</th><th>Scope</th><th>Created</th><th>Last Used</th><th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="font-weight:500;">CI/CD pipeline</td>
          <td><span class="key-token">gop_live_kJ3…82s</span></td>
          <td><span class="scope-badge write">Write</span></td>
          <td class="key-ts">2026-03-12</td>
          <td class="key-ts">2m ago</td>
          <td style="text-align:right;">
            <button class="btn btn-danger" style="font-size:12px;padding:4px 10px;">Revoke</button>
          </td>
        </tr>
        <tr>
          <td style="font-weight:500;">Datadog exporter</td>
          <td><span class="key-token">gop_live_qA8…m1x</span></td>
          <td><span class="scope-badge read">Read</span></td>
          <td class="key-ts">2026-02-01</td>
          <td class="key-ts">14m ago</td>
          <td style="text-align:right;">
            <button class="btn btn-danger" style="font-size:12px;padding:4px 10px;">Revoke</button>
          </td>
        </tr>
        <tr>
          <td style="font-weight:500;">SOC-L2 read</td>
          <td><span class="key-token">gop_live_rT9…pwz</span></td>
          <td><span class="scope-badge read">Read</span></td>
          <td class="key-ts">2025-12-20</td>
          <td class="key-ts">1h ago</td>
          <td style="text-align:right;">
            <button class="btn btn-danger" style="font-size:12px;padding:4px 10px;">Revoke</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
'''
    return render_template_string(layout('api_keys', content))


# ─── HEALTH ───────────────────────────────────────────────────────────────────
@app.route('/health')
def health():
    content = '''
<div class="page-header-row">
  <div>
    <h1 class="page-title">Health <span>/ system status</span></h1>
    <p class="page-subtitle">Live probes against /health and Kubernetes control plane.</p>
  </div>
  <span class="health-status-banner">All systems operational</span>
</div>

<div class="page-content">
  <div class="health-grid">
    <div class="health-card">
      <div class="health-card-label">Service</div>
      <div class="health-card-value" style="font-size:22px;margin-top:4px;">guardianops</div>
    </div>
    <div class="health-card">
      <div class="health-card-label">Version</div>
      <div class="health-card-value ok">6.0</div>
    </div>
    <div class="health-card">
      <div class="health-card-label">Uptime</div>
      <div class="health-card-value">42d 13h</div>
    </div>
  </div>

  <div class="two-col" style="margin-bottom:20px;">
    <div class="data-card" style="padding:18px 20px;">
      <div class="section-title" style="margin-bottom:14px;">Application</div>
      <table>
        <tbody>
          <tr>
            <td style="color:var(--text-2);">Service</td>
            <td style="text-align:right;color:var(--accent);font-weight:500;">guardianops</td>
          </tr>
          <tr>
            <td style="color:var(--text-2);">Health endpoint</td>
            <td style="text-align:right;font-family:var(--mono);font-size:12px;">GET /health</td>
          </tr>
          <tr>
            <td style="color:var(--text-2);">Status</td>
            <td style="text-align:right;color:var(--accent);font-weight:500;">Healthy</td>
          </tr>
          <tr>
            <td style="color:var(--text-2);">Events monitored</td>
            <td style="text-align:right;font-weight:600;">49</td>
          </tr>
          <tr>
            <td style="color:var(--text-2);">Last check</td>
            <td style="text-align:right;font-family:var(--mono);font-size:12px;">2026-04-29 16:11:28 UTC</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="data-card" style="padding:18px 20px;">
      <div class="section-title" style="margin-bottom:14px;">Kubernetes Control Plane</div>
      <table>
        <tbody>
          <tr>
            <td style="color:var(--text-2);">Cluster</td>
            <td style="text-align:right;font-weight:500;">guardianops-cluster</td>
          </tr>
          <tr>
            <td style="color:var(--text-2);">Version</td>
            <td style="text-align:right;color:var(--accent);font-weight:500;">EKS v1.30</td>
          </tr>
          <tr>
            <td style="color:var(--text-2);">Pods</td>
            <td style="text-align:right;color:var(--accent);font-weight:500;">2 Running</td>
          </tr>
          <tr>
            <td style="color:var(--text-2);">Replicas</td>
            <td style="text-align:right;color:var(--accent);font-weight:500;">2 / 2 Ready</td>
          </tr>
          <tr>
            <td style="color:var(--text-2);">Nodes</td>
            <td style="text-align:right;font-weight:500;">2 × t3.medium</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="data-card">
    <div class="data-card-header">
      <div class="data-card-title">Running Pods</div>
    </div>
    <table>
      <thead>
        <tr>
          <th>Pod</th><th>Node</th><th>CPU</th><th>Memory</th><th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="font-family:var(--mono);font-size:12px;">guardianops-7d4c9-xk2</td>
          <td style="font-family:var(--mono);font-size:12px;color:var(--text-2);">ip-10-0-1-12</td>
          <td>
            <div style="display:flex;align-items:center;gap:8px;">
              <div class="progress-bar"><div class="progress-fill" style="width:24%;"></div></div>
              <span style="font-size:12px;color:var(--text-2);">24%</span>
            </div>
          </td>
          <td>
            <div style="display:flex;align-items:center;gap:8px;">
              <div class="progress-bar"><div class="progress-fill warn" style="width:41%;"></div></div>
              <span style="font-size:12px;color:var(--text-2);">41%</span>
            </div>
          </td>
          <td><span class="status-badge blocked">Auto-Blocked</span></td>
        </tr>
        <tr>
          <td style="font-family:var(--mono);font-size:12px;">guardianops-7d4c9-p9m</td>
          <td style="font-family:var(--mono);font-size:12px;color:var(--text-2);">ip-10-0-2-88</td>
          <td>
            <div style="display:flex;align-items:center;gap:8px;">
              <div class="progress-bar"><div class="progress-fill" style="width:18%;"></div></div>
              <span style="font-size:12px;color:var(--text-2);">18%</span>
            </div>
          </td>
          <td>
            <div style="display:flex;align-items:center;gap:8px;">
              <div class="progress-bar"><div class="progress-fill warn" style="width:36%;"></div></div>
              <span style="font-size:12px;color:var(--text-2);">36%</span>
            </div>
          </td>
          <td><span class="status-badge blocked">Auto-Blocked</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
'''
    return render_template_string(layout('health', content))


# ─── HEALTH CHECK API ─────────────────────────────────────────────────────────
@app.route('/healthz')
def healthz():
    return jsonify({"status": "healthy", "version": "6.0",
                    "cluster": "guardianops-cluster"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)