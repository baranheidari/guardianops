// static/js/components/IPCell.js

export const IPCell = ({ ip, iptype }) => {
  return (
    <span className="mono">
      {ip}
      <span className={`iptag ${iptype === "external" ? "ext" : "int"}`}>
        {iptype}
      </span>
    </span>
  );
};
