// static/js/components/Sparkline.js

export const Sparkline = ({ points = [] }) => {
  const path = points
    .map((p, i) => `${i === 0 ? "M" : "L"} ${i * 8} ${20 - p}`)
    .join(" ");

  return (
    <svg width="80" height="20" style={{ opacity: 0.8 }}>
      <path d={path} fill="none" stroke="var(--accent)" strokeWidth="2" />
    </svg>
  );
};
