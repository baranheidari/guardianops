// static/js/components/Pill.js

export const Pill = ({ severity }) => {
  return (
    <span className={`pill pill-${severity}`}>
      {severity}
    </span>
  );
};
