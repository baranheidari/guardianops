// static/js/components/Status.js

export const Status = ({ status }) => {
  return (
    <span className={`status s-${status.replace(" ", "-")}`}>
      <span className="sdot" />
      {status}
    </span>
  );
};
