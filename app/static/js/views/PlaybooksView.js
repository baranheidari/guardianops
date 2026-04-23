// static/js/views/PlaybooksView.js

export const PLAYBOOKS = [
  { id: "ip-quar", name: "Quarantine IP", desc: "Block malicious IP across all firewalls.", ico: "shield" },
  { id: "key-rot", name: "Rotate Keys", desc: "Force rotation of IAM access keys.", ico: "key" },
  { id: "sess-rev", name: "Revoke Sessions", desc: "Terminate active user sessions.", ico: "user" },
  { id: "mfa", name: "Enforce MFA", desc: "Require MFA for privileged roles.", ico: "lock" },
  { id: "report", name: "Generate Report", desc: "Compile incident summary for SOC.", ico: "doc" },
];

export const PlaybooksView = ({ openPlaybook, audit }) => {
  return (
    <>
      <div className="view-head">
        <div>
          <h1>Playbooks <span className="dim">Automation</span></h1>
          <p>Execute automated remediation workflows.</p>
        </div>
      </div>

      <div className="pb-grid">
        {PLAYBOOKS.map(pb => (
          <div className={`pb ${pb.id === "key-rot" ? "destructive" : ""}`} key={pb.id}>
            <div className="pb-top">
              <div className="pb-ico">{pb.ico}</div>
              <div>
                <h3>{pb.name}</h3>
                <p>{pb.desc}</p>
              </div>
            </div>

            <div className="pb-foot">
              <span className="pb-tag">Automation</span>
              <button className="btn" onClick={() => openPlaybook(pb)}>Run</button>
            </div>
          </div>
        ))}
      </div>

      <div className="card" style={{ marginTop: 20 }}>
        <div className="card-title">Recent Playbook Runs</div>
        {audit.length === 0 && <p style={{ marginTop: 10, color: "var(--mute)" }}>No recent executions.</p>}
        {audit.map((a, i) => (
          <div className="info-row" key={i}>
            <span className="k">{a.ts}</span>
            <span className="v">{a.name}</span>
          </div>
        ))}
      </div>
    </>
  );
};
