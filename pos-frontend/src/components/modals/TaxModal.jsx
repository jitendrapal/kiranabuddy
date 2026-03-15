import { useState } from 'react';
import { useTax } from '../../context/TaxContext';

const PRESETS = [0, 5, 10, 18, 20];

export default function TaxModal({ onClose }) {
  const { vatConfig, updateTax } = useTax();
  const [form, setForm] = useState({ ...vatConfig });

  const upd = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const sampleSub = 100;
  const r = form.rate / 100;
  const taxAmt = form.enabled && r
    ? form.type === 'inclusive' ? sampleSub - sampleSub / (1 + r) : sampleSub * r
    : 0;
  const previewTotal = form.type === 'inclusive' ? sampleSub : sampleSub + taxAmt;
  const previewSub   = form.type === 'inclusive' ? sampleSub - taxAmt : sampleSub;

  function save() {
    updateTax(form);
    onClose();
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="tax-modal" onClick={(e) => e.stopPropagation()}>
        <div className="tax-modal-header">
          <span>⚙️ Tax / VAT Configuration</span>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>
        <div className="tax-modal-body">
          <div className="tax-toggle-row">
            <div>
              <div className="tax-toggle-label">Enable Tax / VAT</div>
              <div className="tax-toggle-sub">Apply tax to all cart items</div>
            </div>
            <label className="toggle">
              <input type="checkbox" checked={form.enabled} onChange={(e) => upd('enabled', e.target.checked)} />
              <span className="toggle-slider" />
            </label>
          </div>

          <div className="tax-fields">
            <div className="tax-field">
              <label>Tax Name</label>
              <select value={form.name} onChange={(e) => upd('name', e.target.value)}>
                {['VAT','GST','Sales Tax','Service Tax','Custom'].map((n) => <option key={n}>{n}</option>)}
              </select>
            </div>
            <div className="tax-field">
              <label>Rate (%)</label>
              <input type="number" min="0" max="100" step="0.5" value={form.rate}
                onChange={(e) => upd('rate', parseFloat(e.target.value) || 0)} />
            </div>
          </div>

          <div className="tax-presets-label">Quick Presets</div>
          <div className="tax-presets">
            {PRESETS.map((v) => (
              <button key={v} className={`preset-btn${form.rate === v ? ' active' : ''}`}
                onClick={() => { upd('rate', v); if (v > 0) upd('enabled', true); }}>
                {v}%
              </button>
            ))}
          </div>

          <div className="tax-type-btns">
            <button className={`type-btn${form.type === 'exclusive' ? ' active' : ''}`}
              onClick={() => upd('type', 'exclusive')}>
              ➕ Exclusive<br /><small>Added on top</small>
            </button>
            <button className={`type-btn${form.type === 'inclusive' ? ' active' : ''}`}
              onClick={() => upd('type', 'inclusive')}>
              ✅ Inclusive<br /><small>Already in price</small>
            </button>
          </div>

          <div className="tax-preview">
            <div style={{ fontWeight: 700, marginBottom: 8 }}>📋 Preview (on €100 cart)</div>
            <div className="preview-row"><span>Subtotal</span><span>€ {previewSub.toFixed(2)}</span></div>
            <div className="preview-row"><span>{form.name} ({form.rate}%)</span><span>€ {taxAmt.toFixed(2)}</span></div>
            <div className="preview-row total"><span>Total</span><span>€ {previewTotal.toFixed(2)}</span></div>
          </div>

          <button className="tax-save-btn" onClick={save}>💾 Save Tax Settings</button>
        </div>
      </div>
    </div>
  );
}

