// static/js/ui/TweaksPanel.js

export const TweaksPanel = ({ open, values, onSet }) => {
  if (!open) return null;

  const set = (k, v) => onSet({ ...values, [k]: v });

  return (
    <div className="modal-bg" onClick={() => onSet({ ...values })}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <h2>UI Tweaks</h2>
        <p>Customize theme, accent color, and density.</p>

        <div className="mrow">
          <div className="k">Theme</div>
          <div className="v">
            <button onClick={() => set("theme", "dim")}>Dim</button>
            <button onClick={() => set("theme", "bright")}>Bright</button>
          </div>
        </div>

        <div className="mrow">
          <div className="k">Accent Hue</div>
          <input
            type="range"
            min="0"
            max="360"
            value={values.accentHue}
            onChange={e => set("accentHue", Number(e.target.value))}
            style={{ width: "100%" }}
          />
        </div>

        <div className="mrow">
          <div className="k">Density</div>
          <div className="v">
            <button onClick={() => set("density", "compact")}>Compact</button>
            <button onClick={() => set("density", "cozy")}>Cozy</button>
          </div>
        </div>

        <div className="foot">
          <button onClick={() => onSet(values)}>Close</button>
        </div>
      </div>
    </div>
  );
};
