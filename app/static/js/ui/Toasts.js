// static/js/ui/Toasts.js

import { Icon } from "../components/Icon.js";

export const Toasts = ({ list }) => {
  return (
    <div style={{
      position: "fixed",
      top: 20,
      right: 20,
      zIndex: 200,
      display: "flex",
      flexDirection: "column",
      gap: "10px"
    }}>
      {list.map(t => (
        <div
          key={t.id}
          style={{
            padding: "12px 16px",
            borderRadius: "10px",
            background: "var(--panel)",
            border: "1px solid var(--line-2)",
            backdropFilter: "blur(10px)",
            color: "var(--ink)",
            minWidth: "220px",
            transform: t.out ? "translateX(120%)" : "translateX(0)",
            opacity: t.out ? 0 : 1,
            transition: "all .35s"
          }}
        >
          <div style={{ fontWeight: 600, marginBottom: 4 }}>
            <Icon name={t.ico} size={14} /> {t.title}
          </div>
          <div style={{ fontSize: 12, color: "var(--mute)" }}>{t.desc}</div>
        </div>
      ))}
    </div>
  );
};
