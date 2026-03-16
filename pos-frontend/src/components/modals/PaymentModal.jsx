import { useState } from "react";
import { fmt } from "../../utils/currency";
import { useCart } from "../../context/CartContext";
import { processPayment } from "../../services/api";
import { useUser } from "../../context/UserContext";

const MODES = ["Cash", "UPI", "Card", "Credit"];

export default function PaymentModal({ checkoutData, onClose, onSuccess }) {
  const {
    total = 0,
    rawSubtotal = 0,
    discountAmt = 0,
    taxAmt = 0,
  } = checkoutData || {};
  const { cart, dispatch } = useCart();
  const { user } = useUser();
  const [mode, setMode] = useState("Cash");
  const [cash, setCash] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const cashGiven = parseFloat(cash) || 0;
  const isCash = mode === "Cash";
  const change = isCash ? cashGiven - total : 0;

  // Confirm is blocked for Cash if no amount entered or not enough
  const canConfirm = !isCash || (cashGiven >= total && cashGiven > 0);

  function handleModeChange(m) {
    setMode(m);
    setError("");
  }

  async function handleCheckout() {
    // Validation
    if (isCash) {
      if (!cash || cashGiven <= 0) {
        setError("Please enter the cash amount received from customer.");
        return;
      }
      if (cashGiven < total) {
        setError(`Cash is ${fmt(total - cashGiven)} short. Ask for more.`);
        return;
      }
    }
    setError("");
    setLoading(true);
    try {
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
      onSuccess?.({
        items,
        rawSubtotal,
        discountAmt,
        taxAmt,
        total,
        paymentMode: mode,
        cashGiven: isCash ? cashGiven : null,
        change: isCash ? Math.max(0, change) : null,
        timestamp: new Date(),
      });
      onClose();
    } catch (e) {
      const msg = e.response?.data?.message || e.message || "Unknown error";
      setError("Payment failed: " + msg);
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
          {/* Total */}
          <div className="payment-total">
            <div className="payment-total-label">TOTAL AMOUNT</div>
            <div className="payment-total-amount">{fmt(total)}</div>
          </div>

          {/* Payment mode selector */}
          <div className="payment-modes">
            {MODES.map((m) => (
              <button
                key={m}
                className={`payment-mode-btn${mode === m ? " active" : ""}`}
                onClick={() => handleModeChange(m)}
              >
                {m}
              </button>
            ))}
          </div>

          {/* Cash section */}
          {isCash && (
            <div className="cash-section">
              <label>Cash Received from Customer *</label>
              <input
                type="number"
                placeholder={`Enter amount (min ${fmt(total)})`}
                value={cash}
                onChange={(e) => {
                  setCash(e.target.value);
                  setError("");
                }}
                onKeyDown={(e) => e.key === "Enter" && handleCheckout()}
                autoFocus
                min={0}
                style={{
                  borderColor:
                    error && cashGiven < total && cashGiven > 0
                      ? "#ef4444"
                      : undefined,
                }}
              />

              {/* Change to return — shown prominently when cash is enough */}
              {cashGiven >= total && cashGiven > 0 && (
                <div
                  style={{
                    background: "#f0fdf4",
                    border: "2px solid #86efac",
                    borderRadius: 10,
                    padding: "14px 18px",
                    textAlign: "center",
                    marginTop: 4,
                  }}
                >
                  <div
                    style={{
                      fontSize: 12,
                      fontWeight: 700,
                      color: "#15803d",
                      textTransform: "uppercase",
                      letterSpacing: "0.05em",
                      marginBottom: 4,
                    }}
                  >
                    💵 Return to Customer
                  </div>
                  <div
                    style={{ fontSize: 32, fontWeight: 900, color: "#16a34a" }}
                  >
                    {fmt(change)}
                  </div>
                </div>
              )}

              {/* Shortfall warning */}
              {cashGiven > 0 && cashGiven < total && (
                <div
                  style={{
                    background: "#fef2f2",
                    border: "2px solid #fca5a5",
                    borderRadius: 10,
                    padding: "12px 16px",
                    textAlign: "center",
                    marginTop: 4,
                  }}
                >
                  <div
                    style={{ fontSize: 13, fontWeight: 700, color: "#dc2626" }}
                  >
                    ⚠️ Short by {fmt(total - cashGiven)} — need more cash
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Error message */}
          {error && (
            <div
              style={{
                background: "#fef2f2",
                border: "1.5px solid #fca5a5",
                borderRadius: 8,
                padding: "10px 14px",
                color: "#dc2626",
                fontSize: 13,
                fontWeight: 600,
              }}
            >
              ⚠️ {error}
            </div>
          )}

          {/* Confirm button */}
          <button
            className="payment-confirm-btn"
            onClick={handleCheckout}
            disabled={loading || !canConfirm}
            style={{
              opacity: canConfirm ? 1 : 0.45,
              cursor: canConfirm ? "pointer" : "not-allowed",
            }}
          >
            {loading ? "⏳ Processing..." : `✅ Confirm ${mode} Payment`}
          </button>

          {/* Hint when button is disabled */}
          {isCash && !canConfirm && (
            <p
              style={{
                textAlign: "center",
                fontSize: 12,
                color: "#94a3b8",
                margin: "6px 0 0",
              }}
            >
              Enter cash amount of at least {fmt(total)} to continue
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
