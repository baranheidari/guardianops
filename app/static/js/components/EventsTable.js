// static/js/components/EventsTable.js

import { Pill } from "./Pill.js";
import { Status } from "./Status.js";
import { IPCell } from "./IPCell.js";

export const EventsTable = ({ events }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>Time</th>
          <th>IP</th>
          <th>Type</th>
          <th>Severity</th>
          <th>Status</th>
          <th>Region</th>
        </tr>
      </thead>

      <tbody>
        {events.map(ev => (
          <tr key={ev.id} className={ev._new ? "new-row" : ""}>
            <td className="mono">{ev.ts}</td>
            <td><IPCell ip={ev.ip} iptype={ev.iptype} /></td>
            <td>{ev.type}</td>
            <td><Pill severity={ev.severity} /></td>
            <td><Status status={ev.status} /></td>
            <td className="mono">{ev.region}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};
