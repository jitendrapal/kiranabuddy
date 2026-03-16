import { useCurrency, CURRENCIES } from "../../context/CurrencyContext";
import { fmt } from "../../utils/currency";

export default function CurrencyModal({ onClose }) {
  const { currency, updateCurrency } = useCurrency();

  function select(curr) {
    updateCurrency(curr);
    onClose();
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: "#1e293b",
          borderRadius: 16,
          width: 480,
          maxWidth: "95vw",
          boxShadow: "0 24px 64px rgba(0,0,0,0.5)",
          overflow: "hidden",
          animation: "slideUp 0.2s ease",
        }}
      >
        {/* Header */}
        <div style={{
          background: "linear-gradient(135deg,#1e293b,#0f172a)",
          padding: "18px 24px",
          display: "flex", alignItems: "center", justifyContent: "space-between",
          borderBottom: "1px solid #334155",
        }}>
          <span style={{ fontWeight: 800, fontSize: 17, color: "#f1f5f9" }}>
            💱 Currency Settings
          </span>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>

        {/* Body */}
        <div style={{ padding: 24, display: "flex", flexDirection: "column", gap: 16 }}>
          <p style={{ color: "#94a3b8", fontSize: 13 }}>
            Choose the currency for prices, receipts, and the customer display.
          </p>

          {/* Currency grid */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
            {CURRENCIES.map((c) => {
              const active = c.code === currency.code;
              return (
                <button
                  key={c.code}
                  onClick={() => select(c)}
                  style={{
                    display: "flex", alignItems: "center", gap: 12,
                    padding: "12px 16px",
                    background: active ? "#0f172a" : "#0f172a",
                    border: `2px solid ${active ? "#3b82f6" : "#334155"}`,
                    borderRadius: 10, cursor: "pointer",
                    transition: "border-color 0.15s",
                    textAlign: "left",
                  }}
                >
                  <span style={{ fontSize: 22 }}>{c.flag}</span>
                  <div>
                    <div style={{ fontSize: 15, fontWeight: 800, color: active ? "#60a5fa" : "#f1f5f9" }}>
                      {c.symbol} &nbsp;
                      <span style={{ fontWeight: 600, color: "#64748b", fontSize: 12 }}>{c.code}</span>
                    </div>
                    <div style={{ fontSize: 11, color: "#64748b" }}>{c.name}</div>
                  </div>
                  {active && (
                    <span style={{ marginLeft: "auto", color: "#3b82f6", fontSize: 16 }}>✓</span>
                  )}
                </button>
              );
            })}
          </div>

          {/* Preview */}
          <div style={{
            background: "#0f172a", borderRadius: 10, padding: "14px 18px",
            border: "1px solid #334155",
          }}>
            <div style={{ fontSize: 12, color: "#64748b", marginBottom: 6, fontWeight: 700, textTransform: "uppercase" }}>
              Preview
            </div>
            <div style={{ fontSize: 13, color: "#94a3b8", display: "flex", flexDirection: "column", gap: 4 }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span>Subtotal</span><span style={{ color: "#f1f5f9" }}>{fmt(100)}</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span>Total</span>
                <span style={{ color: "#10b981", fontWeight: 800, fontSize: 16 }}>{fmt(118)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

