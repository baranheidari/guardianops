// static/js/views/StatsView.js

export const StatsView = ({ stats, events }) => {
  const regions = [...new Set(events.map(e => e.region))];

  return (
    <>
      <div className="view-head">
        <div>
          <h1>Statistics <span className="dim">Analytics</span></h1>
          <p>Breakdown of threats, regions, and severity distribution.</p>
        </div>
      </div>

      <div className="grid-3">
        <div className="card">
          <div className="card-title">Severity Breakdown</div>
          <div className="info-row"><span className="k">Critical</span><span className="v acc">{stats.critical}</span></div>
          <div className="info-row"><span className="k">High</span><span className="v">{stats.high}</span></div>
          <div className="info-row"><span className="k">Medium</span><span className="v">{stats.medium}</span></div>
          <div className="info-row"><span className="k">Low</span><span className="v">{stats.low}</span></div>
        </div>

        <div className="card">
          <div className="card-title">Regions</div>
          {regions.map(r => (
            <div className="info-row" key={r}>
              <span className="k">{r}</span>
              <span className="v">{events.filter(e => e.region === r).length}</span>
            </div>
          ))}
        </div>

        <div className="card">
          <div className="card-title">Auto‑Blocked</div>
          <div className="info-row">
            <span className="k">Total</span>
            <span className="v acc">{stats.blocked}</span>
          </div>
        </div>
      </div>
    </>
  );
};
