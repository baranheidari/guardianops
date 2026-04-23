// static/js/modals/PlaybookModal.js

export const PlaybookModal = ({ pb, target, onClose, onConfirm }) => {
  if (!pb) return null;

  return (
    <div className="modal-bg" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <h2>{pb.name}</h2>
        <p>{pb.desc}</p>

        <div className="mrow">
          <div className="k">Target</div>
          <div className="v">{target}</div>
        </div>

        <div className="mrow">
          <div className="k">Preview</div>
          <div className="evidence-box">
            <div className="ev-line-ok">✓ Validating conditions…</div>
            <div className="ev-line-ok">✓ Checking IAM permissions…</div>
            <div className="ev-line-warn">! External webhook queued…</div>
            <div className="ev-line-ok">✓ SOC automation pipeline ready</div>
          </div>
        </div>

        <div className="foot">
          <button onClick={onClose}>Cancel</button>
          <button className="primary" onClick={() => onConfirm(pb)}>Execute</button>
        </div>
      </div>
    </div>
  );
};
