import { useState } from "react";
import { fmt } from "../../utils/currency";
import { useCart } from "../../context/CartContext";
import { processPayment } from "../../services/api";
import { useUser } from "../../context/UserContext";

const MODES = ["Cash", "UPI", "Card", "Credit"];

export default function PaymentModal({ total, onClose, onSuccess }) {
  const { cart, dispatch } = useCart();
  const { user } = useUser();
  const [mode, setMode] = useState("Cash");
  const [cash, setCash] = useState("");
  const [loading, setLoading] = useState(false);

  const cashGiven = parseFloat(cash) || 0;
  const change = mode === "Cash" ? Math.max(0, cashGiven - total) : 0;

  async function handleCheckout() {
    setLoading(true);
    try {
      // Map cart items → Flask /api/sales/record format
      const items = cart
        .filter((i) => i.delta !== 0)
        .map((i) => ({
          name: i.name,
          barcode: i.displayCode || i.code,
          quantity: Math.abs(i.delta || 0),
          price: i.price,
        }));

      await processPayment({
        phone: user?.phone,
        items,
        total,
        payment_mode: mode,
        cash_given: cashGiven,
      });

      dispatch({ type: "CLEAR" });
      onSuccess?.();
      onClose();
    } catch (e) {
      const msg = e.response?.data?.message || e.message || "Unknown error";
      alert("Payment failed: " + msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="payment-modal" onClick={(e) => e.stopPropagation()}>
        <div className="payment-modal-header">
          <h2>💰 Checkout</h2>
          <button className="modal-close" onClick={onClose}>
            ✕
          </button>
        </div>
        <div className="payment-modal-body">
          <div className="payment-total">
            <div className="payment-total-label">TOTAL AMOUNT</div>
            <div className="payment-total-amount">{fmt(total)}</div>
          </div>

          <div className="payment-modes">
            {MODES.map((m) => (
              <button
                key={m}
                className={`payment-mode-btn${mode === m ? " active" : ""}`}
                onClick={() => setMode(m)}
              >
                {m}
              </button>
            ))}
          </div>

          {mode === "Cash" && (
            <div className="cash-section">
              <label>Cash Given</label>
              <input
                type="number"
                placeholder="Enter cash amount"
                value={cash}
                onChange={(e) => setCash(e.target.value)}
                autoFocus
              />
              {cashGiven > 0 && (
                <div className="change-display">
                  Change: <strong>{fmt(change)}</strong>
                </div>
              )}
            </div>
          )}

          <button
            className="payment-confirm-btn"
            onClick={handleCheckout}
            disabled={loading}
          >
            {loading ? "⏳ Processing..." : `✅ Confirm ${mode} Payment`}
          </button>
        </div>
      </div>
    </div>
  );
}
