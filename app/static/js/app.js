// static/js/app.js

import { Icon } from './components/Icon.js';
import { Sparkline } from './components/Sparkline.js';
import { Pill } from './components/Pill.js';
import { Status } from './components/Status.js';
import { IPCell } from './components/IPCell.js';
import { EventsTable } from './components/EventsTable.js';

import { DashboardView } from './views/DashboardView.js';
import { EventsView } from './views/EventsView.js';
import { StatsView } from './views/StatsView.js';
import { PlaybooksView, PLAYBOOKS } from './views/PlaybooksView.js';
import { HealthView } from './views/HealthView.js';

import { PlaybookModal } from './modals/PlaybookModal.js';
import { CMDK } from './ui/CMDK.js';
import { Toasts } from './ui/Toasts.js';
import { TweaksPanel } from './ui/TweaksPanel.js';

const { useState, useEffect, useMemo } = React;

// ------------------------------------------------------------
// Seed data
// ------------------------------------------------------------
const SEED_EVENTS = [
  {id:1,ts:"2026-04-22 03:14:22",ip:"185.234.219.42",type:"Unauthorized API Call",severity:"HIGH",status:"Auto-Blocked",region:"us-east-1",iptype:"external",user:"anon"},
  {id:2,ts:"2026-04-22 07:55:10",ip:"10.0.0.45",     type:"Unusual S3 Access",   severity:"MEDIUM",status:"Investigating",region:"us-east-1",iptype:"internal",user:"data-eng"},
  {id:3,ts:"2026-04-22 11:02:47",ip:"203.0.113.99",  type:"Brute Force Attempt", severity:"CRITICAL",status:"Auto-Blocked",region:"us-west-2",iptype:"external",user:"anon"},
  {id:4,ts:"2026-04-22 13:30:01",ip:"10.0.1.12",     type:"IAM Policy Change",   severity:"LOW",status:"Resolved",region:"us-east-1",iptype:"internal",user:"devops-bot"},
  {id:5,ts:"2026-04-22 14:11:05",ip:"198.51.100.77", type:"Port Scan Detected",  severity:"HIGH",status:"Investigating",region:"us-east-2",iptype:"external",user:"anon"},
  {id:6,ts:"2026-04-22 15:44:33",ip:"10.0.2.88",     type:"Privilege Escalation",severity:"CRITICAL",status:"Auto-Blocked",region:"us-east-1",iptype:"internal",user:"svc-deploy"},
  {id:7,ts:"2026-04-22 16:02:19",ip:"172.16.4.103",  type:"Suspicious DNS Query",severity:"MEDIUM",status:"Investigating",region:"us-east-1",iptype:"internal",user:"web-fe"},
  {id:8,ts:"2026-04-22 16:38:55",ip:"45.141.84.10",  type:"Credential Stuffing", severity:"HIGH",status:"Auto-Blocked",region:"eu-west-1",iptype:"external",user:"anon"},
];

const SYNTH_TYPES   = ["Suspicious DNS Query","Port Scan Detected","Unusual S3 Access","Unauthorized API Call","Token Replay Attack","Egress Anomaly","Malformed JWT","Rate Limit Breach"];
const SYNTH_SEV     = ["CRITICAL","HIGH","HIGH","MEDIUM","MEDIUM","MEDIUM","LOW"];
const SYNTH_REGIONS = ["us-east-1","us-east-2","us-west-2","eu-west-1","ap-south-1"];

const randIP = (ext) => ext
  ? `${45+Math.floor(Math.random()*200)}.${Math.floor(Math.random()*240)}.${Math.floor(Math.random()*240)}.${Math.floor(Math.random()*240)}`
  : `10.0.${Math.floor(Math.random()*5)}.${Math.floor(Math.random()*250)}`;

const TWEAKS = {
  theme: "dim",
  accentHue: 207,
  density: "compact",
};

const NAV = [
  {id:"dashboard", name:"Dashboard",  ico:"dashboard"},
  {id:"events",    name:"Events",     ico:"bolt", badge:"LIVE"},
  {id:"stats",     name:"Statistics", ico:"chart"},
  {id:"playbooks", name:"Playbooks",  ico:"book"},
  {id:"health",    name:"Health",     ico:"heart"},
];

// ------------------------------------------------------------
// Main App Component
// ------------------------------------------------------------
const App = () => {
  const [view, setViewRaw] = useState(() => localStorage.getItem("go-view") || "dashboard");
  const setView = (v) => { setViewRaw(v); localStorage.setItem("go-view", v); };

  const [events, setEvents] = useState(SEED_EVENTS);
  const [cmdk, setCmdk] = useState(false);
  const [pbModal, setPbModal] = useState(null);
  const [audit, setAudit] = useState([]);
  const [toasts, setToasts] = useState([]);
  const [tweaksOpen, setTweaksOpen] = useState(false);
  const [tw, setTw] = useState(TWEAKS);

  // ------------------------------------------------------------
  // Theme + Accent
  // ------------------------------------------------------------
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", tw.theme);
    document.documentElement.style.setProperty("--accent",   `oklch(0.74 0.16 ${tw.accentHue})`);
    document.documentElement.style.setProperty("--accent-2", `oklch(0.82 0.12 ${tw.accentHue+5})`);
    document.documentElement.style.setProperty("--accent-soft", `oklch(0.74 0.16 ${tw.accentHue} / .14)`);
  }, [tw]);

  // ------------------------------------------------------------
  // Live event stream
  // ------------------------------------------------------------
  useEffect(() => {
    let cancel = false;
    const tick = () => {
      if(cancel) return;
      const ext = Math.random() > .45;
      const sev = SYNTH_SEV[Math.floor(Math.random()*SYNTH_SEV.length)];
      const nev = {
        id: Date.now()%100000,
        ts: new Date().toISOString().slice(0,19).replace('T',' '),
        ip: randIP(ext),
        type: SYNTH_TYPES[Math.floor(Math.random()*SYNTH_TYPES.length)],
        severity: sev,
        status: sev === "CRITICAL" || sev === "HIGH" ? "Auto-Blocked" : (Math.random()>.5?"Investigating":"Resolved"),
        region: SYNTH_REGIONS[Math.floor(Math.random()*SYNTH_REGIONS.length)],
        iptype: ext?"external":"internal",
        user: ext?"anon":"svc-app",
        _new: true
      };
      setEvents(ev => [nev, ...ev].slice(0, 60));
      if(sev === "CRITICAL") pushToast({title:"Critical threat detected", desc:`${nev.type} from ${nev.ip}`, ico:"bolt"});
      setTimeout(tick, 9000 + Math.random()*5000);
    };
    const t = setTimeout(tick, 6000);
    return () => { cancel = true; clearTimeout(t); };
  }, []);

  // ------------------------------------------------------------
  // Toasts
  // ------------------------------------------------------------
  const pushToast = (t) => {
    const id = Math.random().toString(36).slice(2);
    setToasts(list => [...list, {...t, id}]);
    setTimeout(()=> setToasts(list => list.map(x => x.id===id?{...x,out:true}:x)), 4000);
    setTimeout(()=> setToasts(list => list.filter(x => x.id!==id)), 4400);
  };

  // ------------------------------------------------------------
  // CMDK (Command Palette)
  // ------------------------------------------------------------
  useEffect(() => {
    const k = (e) => {
      if((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k"){ e.preventDefault(); setCmdk(c => !c); }
    };
    window.addEventListener("keydown", k);
    return () => window.removeEventListener("keydown", k);
  }, []);

  // ------------------------------------------------------------
  // Stats
  // ------------------------------------------------------------
  const stats = useMemo(() => ({
    total: events.length,
    critical: events.filter(e=>e.severity==="CRITICAL").length,
    high:     events.filter(e=>e.severity==="HIGH").length,
    medium:   events.filter(e=>e.severity==="MEDIUM").length,
    low:      events.filter(e=>e.severity==="LOW").length,
    blocked:  events.filter(e=>e.status==="Auto-Blocked").length,
  }), [events]);

  // ------------------------------------------------------------
  // Playbook modal
  // ------------------------------------------------------------
  const openPlaybook = (pb) => {
    const t = pb.id === "ip-quar" ? (events.find(e=>e.iptype==="external")?.ip || "—")
            : pb.id === "key-rot" ? "svc-deploy"
            : pb.id === "sess-rev" ? "user:anon-session"
            : pb.id === "mfa" ? "role/admin"
            : pb.id === "report" ? "INC-2026-0422" : "SOC-L2";
    setPbModal({pb, target: t});
  };

  const confirmPlaybook = (pb) => {
    setPbModal(null);
    const a = {name: pb.name, ts: new Date().toISOString().slice(0,19).replace('T',' '), target: "svc-deploy", ico: pb.ico};
    setAudit(x => [a, ...x].slice(0,8));
    pushToast({title:`${pb.name} executed`, desc:"Audit entry recorded · webhook fired to SOC.", ico:pb.ico});
  };

  // ------------------------------------------------------------
  // Render
  // ------------------------------------------------------------
  return (
    <div id="app">
      <aside className="side">
        <div className="brand">
          <div className="logo"><img src="/static/assets/G.png" alt=""/></div>
          <div>
            <div className="name">Guardian<span>Ops</span></div>
            <div className="sub">Cloud Security Console</div>
          </div>
        </div>

        <div className="nav-group">Workspace</div>
        <div className="nav">
          {NAV.map(n => (
            <a key={n.id} className={view===n.id?"active":""} onClick={()=>setView(n.id)}>
              <span className="ico"><Icon name={n.ico}/></span>
              <span>{n.name}</span>
              {n.badge && <span className="badge">{n.badge}</span>}
            </a>
          ))}
        </div>

        <div className="nav-group">Environment</div>
        <div className="nav">
          <a><span className="ico"><Icon name="pods"/></span><span>us-east-1</span><span className="badge" style={{background:"transparent",borderColor:"var(--line-2)",color:"var(--mute)"}}>PROD</span></a>
          <a><span className="ico"><Icon name="shield"/></span><span>Access rules</span></a>
          <a><span className="ico"><Icon name="settings"/></span><span>Settings</span></a>
        </div>

        <div className="side-foot">
          <div className="avatar">BH</div>
          <div className="who">Baran Heidari<small>sec-ops-responder</small></div>
        </div>
      </aside>

      <div className="main">
        <div className="topbar">
          <div className="search">
            <span className="si"><Icon name="search" size={14}/></span>
            <input placeholder="Search events, IPs, playbooks…" onFocus={()=>setCmdk(true)}/>
            <span className="kbd">⌘K</span>
          </div>
          <div className="spacer"></div>
          <span className="chip"><span className="dot"/>Ingestion &lt; 500 ms</span>
          <button className="icon-btn" title="Notifications"><Icon name="bell" size={15}/><span className="nd"/></button>
          <button className="icon-btn" title="Command palette" onClick={()=>setCmdk(true)}><Icon name="cmd" size={15}/></button>
          <button className="icon-btn" title="Settings" onClick={()=>setTweaksOpen(o=>!o)}><Icon name="settings" size={15}/></button>
        </div>

        <div className="view" key={view}>
          {view === "dashboard" && <DashboardView events={events} stats={stats} openPlaybook={openPlaybook}/>}
          {view === "events"    && <EventsView events={events}/>}
          {view === "stats"     && <StatsView stats={stats} events={events}/>}
          {view === "playbooks" && <PlaybooksView openPlaybook={openPlaybook} audit={audit}/>}
          {view === "health"    && <HealthView stats={stats} audit={audit}/>}
        </div>
      </div>

      <CMDK open={cmdk} onClose={()=>setCmdk(false)} setView={setView} events={events}/>
      {pbModal && <PlaybookModal pb={pbModal.pb} target={pbModal.target} onClose={()=>setPbModal(null)} onConfirm={confirmPlaybook}/>}
      <Toasts list={toasts}/>
      <TweaksPanel open={tweaksOpen} values={tw} onSet={setTw}/>
    </div>
  );
};

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
