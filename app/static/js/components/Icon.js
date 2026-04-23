// static/js/components/Icon.js

export const Icon = ({ name, size = 16 }) => {
  const icons = {
    dashboard: "📊",
    bolt: "⚡",
    chart: "📈",
    book: "📘",
    heart: "❤️",
    pods: "📦",
    shield: "🛡️",
    settings: "⚙️",
    search: "🔍",
    bell: "🔔",
    cmd: "⌘",
  };

  return (
    <span style={{ fontSize: size, lineHeight: 1 }}>
      {icons[name] || "❓"}
    </span>
  );
};
