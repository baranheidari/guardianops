// static/js/views/DashboardView.js

import { Sparkline } from "../components/Sparkline.js";
import { EventsTable } from "../components/EventsTable.js";

export const DashboardView = ({ events, stats, openPlaybook }) => {
  const spark = [4, 8, 6, 10, 7, 12, 9, 14, 11, 15];

  return (
    <>
      <div className="view-head">
        <div>
          <h1>Dashboard <span className="dim">Overview</span></h1>
          <p>Live security posture across your cloud environment.</p>
        </div>
      </div>

      <div className="grid-4">
        <div className="card stat is-crit">
          <div className="lbl">Critical Alerts</div>
          <div className="val">{stats.critical}</div>
          <div className="delta"><span className="up">▲</span> +12% today</div>
          <div className="spark"><Sparkline points={spark} /></div>
        </div>

        <div className="card stat is-high">
          <div className="lbl">High Severity</div>
          <div className="val">{stats.high}</div>
          <div className="delta"><span className="up">▲</span> +5% today</div>
          <div className="spark"><Sparkline points={spark} /></div>
        </div>

        <div className="card stat is-med">
          <div className="lbl">Medium Severity</div>
          <div className="val">{stats.medium}</div>
          <div className="delta"><span className="down">▼</span> -3% today</div>
          <div className="spark"><Sparkline points={spark} /></div>
        </div>

        <div className="card stat is-acc">
          <div className="lbl">Auto‑Blocked</div>
          <div className="val">{stats.blocked}</div>
          <div className="delta"><span className="up">▲</span> +9% today</div>
          <div className="spark"><Sparkline points={spark} /></div>
        </div>
      </div>

      <div className="card" style={{ marginTop: 20 }}>
        <div className="card-head">
          <div className="card-title">Recent Events</div>
          <div className="card-act" onClick={() => openPlaybook({ id: "ip-quar", name: "Quarantine IP", ico: "shield" })}>
            Run Playbook →
          </div>
        </div>

        <EventsTable events={events.slice(0, 10)} />
      </div>
    </>
  );
};
