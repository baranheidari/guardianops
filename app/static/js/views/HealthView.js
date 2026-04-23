// static/js/views/HealthView.js

export const HealthView = ({ stats, audit }) => {
  return (
    <>
      <div className="view-head">
        <div>
          <h1>Health <span className="dim">System Status</span></h1>
          <p>Operational status of ingestion, automation, and SOC pipelines.</p>
        </div>
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="card-title">Ingestion Pipeline</div>
          <div className="info-row"><span className="k">Status</span><span className="v acc">Healthy</span></div>
          <div className="info-row"><span className="k">Latency</span><span className="v">420 ms</span></div>
          <div className="info-row"><span className="k">Throughput</span><span className="v">12.4k events/min</span></div>
        </div>

        <div className="card">
          <div className="card-title">Automation</div>
          <div className="info-row"><span className="k">Playbooks Run</span><span className="v">{audit.length}</span></div>
          <div className="info-row"><span className="k">Last Run</span><span className="v">{audit[0]?.ts || "—"}</span></div>
        </div>
      </div>
    </>
  );
};
