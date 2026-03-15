import { useState } from 'react';
import { fmt } from '../../utils/currency';
import { useCart } from '../../context/CartContext';

const PRESETS = [0.25, 0.5, 0.75, 1, 2];

export default function WeightModal({ product, onClose }) {
  const { dispatch } = useCart();
  const [input, setInput] = useState('');

  const kg = parseFloat(input) || 0;
  const amount = kg * (product?.price || 0);

  function numpad(key) {
    if (key === 'del') { setInput((p) => p.slice(0, -1)); return; }
    if (key === '.' && input.includes('.')) return;
    if (input.length >= 7) return;
    setInput((p) => p + key);
  }

  function confirm() {
    if (kg <= 0) { alert('Please enter a valid weight'); return; }
    dispatch({
      type: 'ADD_WEIGHT',
      payload: { code: product.barcode, name: product.name, price: product.price,
        pricePerKg: product.price, weightKg: kg, emoji: product.emoji },
    });
    onClose();
  }

  if (!product) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="weight-modal" onClick={(e) => e.stopPropagation()}>
        <div className="weight-modal-header">
          <div style={{ fontSize: 36 }}>{product.emoji}</div>
          <div>
            <div className="weight-modal-name">{product.name}</div>
            <div className="weight-modal-rate">{fmt(product.price)} per kg</div>
          </div>
        </div>
        <div className="weight-modal-body">
          <div className="weight-presets">
            {PRESETS.map((v) => (
              <button key={v} className={`preset-btn${input === String(v) ? ' selected' : ''}`}
                onClick={() => setInput(String(v))}>
                {v < 1 ? `${v * 1000}g` : `${v} kg`}
              </button>
            ))}
          </div>
          <div className="weight-display">
            <span className="weight-val">{kg.toFixed(3)}</span>
            <span className="weight-unit"> kg</span>
            <div className="weight-amt">= {fmt(amount)}</div>
          </div>
          <div className="numpad">
            {['1','2','3','4','5','6','7','8','9','.','0','del'].map((k) => (
              <button key={k} className={`numpad-btn${k === 'del' ? ' del' : ''}`} onClick={() => numpad(k)}>
                {k === 'del' ? '⌫' : k}
              </button>
            ))}
          </div>
          <div className="weight-modal-actions">
            <button className="wm-cancel" onClick={onClose}>Cancel</button>
            <button className="wm-confirm" onClick={confirm}>➕ Add to Cart</button>
          </div>
        </div>
      </div>
    </div>
  );
}

