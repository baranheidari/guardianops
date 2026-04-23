// static/js/ui/CMDK.js

import { Icon } from "../components/Icon.js";

export const CMDK = ({ open, onClose, setView, events }) => {
  if (!open) return null;

  const jump = (v) => { setView(v); onClose(); };

  const recentIPs = [...new Set(events.slice(0, 20).map(e => e.ip))].slice(0, 5);

  return (
    <div className="modal-bg" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <h2>Command Palette</h2>
        <p>Quick navigation and shortcuts.</p>

        <div className="mrow">
          <div className="k">Navigation</div>
          <div className="v">
            <button onClick={() => jump("dashboard")}>Go to Dashboard</button>
            <button onClick={() => jump("events")}>Go to Events</button>
            <button onClick={() => jump("stats")}>Go to Statistics</button>
            <button onClick={() => jump("playbooks")}>Go to Playbooks</button>
            <button onClick={() => jump("health")}>Go to Health</button>
          </div>
        </div>

        <div className="mrow">
          <div className="k">Recent IPs</div>
          {recentIPs.map(ip => (
            <div key={ip} className="info-row">
              <span className="k">{ip}</span>
              <span className="v">View in Events</span>
            </div>
          ))}
        </div>

        <div className="foot">
          <button onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
};
