import { useState, useEffect } from "react";
import { useUser } from "../../context/UserContext";
import { fetchEODReport } from "../../services/api";
import { fmt } from "../../utils/currency";

export default function EODReportModal({ onClose }) {
  const { user } = useUser();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const res = await fetchEODReport(user.phone);
        setReport(res.data);
      } catch (e) {
        setError(e.response?.data?.message || "Failed to load report");
      } finally {
        setLoading(false);
      }
    })();
  }, [user.phone]);

  const card = (label, value, color = "#f1f5f9", sub) => (
    <div
      style={{
        background: "#0f172a",
        border: "1px solid #334155",
        borderRadius: 12,
        padding: "16px 20px",
        flex: 1,
        minWidth: 120,
      }}
    >
      <div
        style={{
          fontSize: 11,
          color: "#64748b",
          fontWeight: 700,
          textTransform: "uppercase",
          letterSpacing: "0.05em",
          marginBottom: 6,
        }}
      >
        {label}
      </div>
      <div style={{ fontSize: 26, fontWeight: 900, color }}>{value}</div>
      {sub && (
        <div style={{ fontSize: 11, color: "#64748b", marginTop: 4 }}>
          {sub}
        </div>
      )}
    </div>
  );

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: "#1e293b",
          borderRadius: 16,
          width: 560,
          maxWidth: "95vw",
          maxHeight: "90vh",
          overflow: "auto",
          border: "1px solid #334155",
          boxShadow: "0 24px 80px rgba(0,0,0,0.5)",
          color: "#f1f5f9",
        }}
      >
        {/* Header */}
        <div
          style={{
            padding: "20px 24px 16px",
            borderBottom: "1px solid #334155",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div>
            <div style={{ fontSize: 20, fontWeight: 800 }}>
              📊 End of Day Report
            </div>
            {report && (
              <div style={{ fontSize: 13, color: "#64748b", marginTop: 2 }}>
                {report.date} · Generated at {report.generated_at}
              </div>
            )}
          </div>
          <div style={{ display: "flex", gap: 8 }}>
            <button
              onClick={() => window.print()}
              className="receipt-btn print"
              style={{ padding: "8px 16px" }}
            >
              🖨️ Print
            </button>
            <button
              onClick={onClose}
              className="receipt-btn close"
              style={{ padding: "8px 16px" }}
            >
              ✕
            </button>
          </div>
        </div>

        {/* Body */}
        <div style={{ padding: "20px 24px" }}>
          {loading && (
            <p
              style={{
                color: "#94a3b8",
                textAlign: "center",
                padding: "40px 0",
              }}
            >
              ⏳ Loading report...
            </p>
          )}
          {error && (
            <p
              style={{
                color: "#ef4444",
                textAlign: "center",
                padding: "40px 0",
              }}
            >
              ❌ {error}
            </p>
          )}

          {report && (
            <>
              {/* Summary cards */}
              <div
                style={{
                  display: "flex",
                  gap: 12,
                  flexWrap: "wrap",
                  marginBottom: 24,
                }}
              >
                {card("Revenue Today", fmt(report.total_revenue), "#10b981")}
                {card("Items Sold", report.total_items, "#f1f5f9")}
                {card("Transactions", report.total_txns, "#f1f5f9")}
                {report.total_profit > 0 &&
                  card(
                    "Est. Profit",
                    fmt(report.total_profit),
                    "#a78bfa",
                    `Cost: ${fmt(report.total_cost)}`,
                  )}
              </div>

              {/* Top products by revenue */}
              {report.top_by_revenue?.length > 0 && (
                <div style={{ marginBottom: 20 }}>
                  <div
                    style={{
                      fontSize: 13,
                      fontWeight: 700,
                      color: "#94a3b8",
                      textTransform: "uppercase",
                      letterSpacing: "0.05em",
                      marginBottom: 10,
                    }}
                  >
                    💰 Top Products by Revenue
                  </div>
                  {report.top_by_revenue.map((p, i) => (
                    <div
                      key={i}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 12,
                        padding: "10px 12px",
                        marginBottom: 6,
                        background: "#0f172a",
                        borderRadius: 8,
                      }}
                    >
                      <span
                        style={{
                          width: 24,
                          height: 24,
                          background: "#334155",
                          borderRadius: "50%",
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          fontSize: 12,
                          fontWeight: 800,
                          color: "#f1f5f9",
                          flexShrink: 0,
                        }}
                      >
                        {i + 1}
                      </span>
                      <span
                        style={{
                          flex: 1,
                          fontSize: 14,
                          fontWeight: 600,
                          color: "#f1f5f9",
                        }}
                      >
                        {p.name}
                      </span>
                      <span
                        style={{
                          fontWeight: 800,
                          color: "#10b981",
                          fontSize: 15,
                        }}
                      >
                        {fmt(p.revenue)}
                      </span>
                    </div>
                  ))}
                </div>
              )}

              {/* Top products by quantity */}
              {report.top_by_qty?.length > 0 && (
                <div>
                  <div
                    style={{
                      fontSize: 13,
                      fontWeight: 700,
                      color: "#94a3b8",
                      textTransform: "uppercase",
                      letterSpacing: "0.05em",
                      marginBottom: 10,
                    }}
                  >
                    📦 Top Products by Quantity
                  </div>
                  {report.top_by_qty.map((p, i) => (
                    <div
                      key={i}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 12,
                        padding: "10px 12px",
                        marginBottom: 6,
                        background: "#0f172a",
                        borderRadius: 8,
                      }}
                    >
                      <span
                        style={{
                          width: 24,
                          height: 24,
                          background: "#334155",
                          borderRadius: "50%",
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          fontSize: 12,
                          fontWeight: 800,
                          color: "#f1f5f9",
                          flexShrink: 0,
                        }}
                      >
                        {i + 1}
                      </span>
                      <span
                        style={{
                          flex: 1,
                          fontSize: 14,
                          fontWeight: 600,
                          color: "#f1f5f9",
                        }}
                      >
                        {p.name}
                      </span>
                      <span
                        style={{
                          fontWeight: 800,
                          color: "#60a5fa",
                          fontSize: 15,
                        }}
                      >
                        {p.qty} units
                      </span>
                    </div>
                  ))}
                </div>
              )}

              {report.total_revenue === 0 && (
                <div
                  style={{
                    textAlign: "center",
                    padding: "30px 0",
                    color: "#64748b",
                  }}
                >
                  <div style={{ fontSize: 40, marginBottom: 8 }}>📭</div>
                  <p>No sales recorded today yet.</p>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
