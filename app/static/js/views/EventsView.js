// static/js/views/EventsView.js

import { EventsTable } from "../components/EventsTable.js";

export const EventsView = ({ events }) => {
  return (
    <>
      <div className="view-head">
        <div>
          <h1>Events <span className="dim">Live Stream</span></h1>
          <p>Real‑time detections from your cloud workloads.</p>
        </div>
      </div>

      <EventsTable events={events} />
    </>
  );
};
