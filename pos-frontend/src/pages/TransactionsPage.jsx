import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext";
import { fetchTransactions } from "../services/api";
import { fmt } from "../utils/currency";

const FILTERS = [
  { key: "today", label: "Today" },
  { key: "week", label: "Last 7 Days" },
  { key: "all", label: "All Time" },
];

const TYPE_LABELS = {
  sale: { label: "Sale", color: "#10b981", bg: "#f0fdf4" },
  reduce_stock: { label: "Sale", color: "#10b981", bg: "#f0fdf4" },
  add_stock: { label: "Stock In", color: "#3b82f6", bg: "#eff6ff" },
  adjustment: { label: "Adjust", color: "#f59e0b", bg: "#fffbeb" },
};

function badge(type) {
  const t = TYPE_LABELS[type] || {
    label: type,
    color: "#94a3b8",
    bg: "#f1f5f9",
  };
  return (
    <span
      style={{
        background: t.bg,
        color: t.color,
        border: `1px solid ${t.color}`,
        borderRadius: 6,
        padding: "2px 8px",
        fontSize: 11,
        fontWeight: 700,
      }}
    >
      {t.label}
    </span>
  );
}

function formatTs(ts) {
  if (!ts) return "—";
  try {
    return new Date(ts).toLocaleString("en-GB", {
      day: "2-digit",
      month: "short",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return ts;
  }
}

export default function TransactionsPage() {
  const { user } = useUser();
  const navigate = useNavigate();

  const [filter, setFilter] = useState("today");
  const [txns, setTxns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetchTransactions(user.phone, filter);
      setTxns(res.data?.transactions || []);
    } catch {
      setTxns([]);
    } finally {
      setLoading(false);
    }
  }, [user.phone, filter]);

  useEffect(() => {
    load();
  }, [load]);

  // Only count sales for revenue summary
  const sales = txns.filter((t) =>
    ["sale", "reduce_stock"].includes(t.transaction_type),
  );
  const revenue = sales.reduce(
    (s, t) => s + (parseFloat(t.total_amount) || 0),
    0,
  );
  const itemsSold = sales.reduce(
    (s, t) => s + (parseFloat(t.quantity) || 0),
    0,
  );

  const filtered = txns.filter((t) =>
    (t.product_name || "").toLowerCase().includes(search.toLowerCase()),
  );

  const s = {
    /* shared inline style helpers */
    page: {
      height: "100vh",
      display: "flex",
      flexDirection: "column",
      background: "#0f172a",
      color: "#f1f5f9",
      fontFamily: "sans-serif",
      overflow: "hidden",
    },
    bar: {
      padding: "14px 24px",
      background: "#1e293b",
      display: "flex",
      alignItems: "center",
      gap: 14,
      borderBottom: "1px solid #334155",
    },
    btn: (c) => ({
      padding: "9px 18px",
      background: "transparent",
      border: `1.5px solid ${c}`,
      borderRadius: 8,
      color: c,
      cursor: "pointer",
      fontSize: 14,
      fontWeight: 600,
    }),
    tab: (active) => ({
      padding: "8px 18px",
      borderRadius: 20,
      border: "1.5px solid #334155",
      background: active ? "#3b82f6" : "transparent",
      color: active ? "#fff" : "#94a3b8",
      cursor: "pointer",
      fontSize: 13,
      fontWeight: 600,
    }),
    input: {
      padding: "9px 14px",
      background: "#1e293b",
      border: "1px solid #334155",
      borderRadius: 8,
      color: "#f1f5f9",
      fontSize: 13,
      width: 260,
    },
    card: {
      background: "#1e293b",
      border: "1px solid #334155",
      borderRadius: 12,
      padding: "16px 20px",
      minWidth: 140,
    },
    th: {
      padding: "10px 14px",
      color: "#64748b",
      fontSize: 11,
      fontWeight: 700,
      textAlign: "left",
      textTransform: "uppercase",
      borderBottom: "1px solid #334155",
      position: "sticky",
      top: 0,
      background: "#0f172a",
      zIndex: 1,
    },
    td: {
      padding: "10px 14px",
      fontSize: 13,
      borderBottom: "1px solid #1e293b",
    },
  };

  return (
    <div style={s.page}>
      {/* Top bar */}
      <div style={s.bar}>
        <button onClick={() => navigate("/pos")} style={s.btn("#64748b")}>
          ← Back to POS
        </button>
        <h1 style={{ margin: 0, fontSize: 20, flex: 1 }}>
          📋 Transaction History
        </h1>
        <button onClick={load} style={s.btn("#3b82f6")}>
          ↻ Refresh
        </button>
      </div>

      {/* Summary cards */}
      <div style={{ display: "flex", gap: 16, padding: "20px 24px 0" }}>
        <div style={s.card}>
          <div style={{ fontSize: 12, color: "#64748b", marginBottom: 4 }}>
            REVENUE
          </div>
          <div style={{ fontSize: 24, fontWeight: 900, color: "#10b981" }}>
            {fmt(revenue)}
          </div>
        </div>
        <div style={s.card}>
          <div style={{ fontSize: 12, color: "#64748b", marginBottom: 4 }}>
            ITEMS SOLD
          </div>
          <div style={{ fontSize: 24, fontWeight: 900, color: "#f1f5f9" }}>
            {itemsSold}
          </div>
        </div>
        <div style={s.card}>
          <div style={{ fontSize: 12, color: "#64748b", marginBottom: 4 }}>
            TRANSACTIONS
          </div>
          <div style={{ fontSize: 24, fontWeight: 900, color: "#f1f5f9" }}>
            {txns.length}
          </div>
        </div>
      </div>

      {/* Filter tabs + search */}
      <div
        style={{
          display: "flex",
          gap: 8,
          padding: "16px 24px",
          alignItems: "center",
          flexWrap: "wrap",
        }}
      >
        {FILTERS.map((f) => (
          <button
            key={f.key}
            style={s.tab(filter === f.key)}
            onClick={() => setFilter(f.key)}
          >
            {f.label}
          </button>
        ))}
        <input
          style={{ ...s.input, marginLeft: "auto" }}
          placeholder="🔎 Search product..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Table — scrollable, takes all remaining height */}
      <div style={{ flex: 1, overflow: "auto", padding: "0 24px 24px" }}>
        {loading ? (
          <p style={{ color: "#94a3b8", padding: "40px 0" }}>
            ⏳ Loading transactions...
          </p>
        ) : filtered.length === 0 ? (
          <div
            style={{ textAlign: "center", padding: "60px 0", color: "#64748b" }}
          >
            <div style={{ fontSize: 48, marginBottom: 12 }}>📭</div>
            <p>
              No transactions found{search ? ` for "${search}"` : ""} in this
              period.
            </p>
          </div>
        ) : (
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              background: "#1e293b",
              borderRadius: 12,
              overflow: "hidden",
            }}
          >
            <thead>
              <tr>
                {[
                  "Time",
                  "Product",
                  "Type",
                  "Qty",
                  "Unit Price",
                  "Amount",
                  "Notes",
                ].map((h) => (
                  <th key={h} style={s.th}>
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map((t, i) => {
                const isSale = ["sale", "reduce_stock"].includes(
                  t.transaction_type,
                );
                return (
                  <tr
                    key={t.transaction_id || i}
                    style={{ background: i % 2 === 0 ? "#1e293b" : "#172033" }}
                  >
                    <td
                      style={{
                        ...s.td,
                        color: "#64748b",
                        fontSize: 12,
                        whiteSpace: "nowrap",
                      }}
                    >
                      {formatTs(t.timestamp)}
                    </td>
                    <td style={{ ...s.td, fontWeight: 600 }}>
                      {t.product_name || "—"}
                    </td>
                    <td style={s.td}>{badge(t.transaction_type)}</td>
                    <td style={{ ...s.td, textAlign: "right" }}>
                      {parseFloat(t.quantity || 0)}
                    </td>
                    <td
                      style={{ ...s.td, textAlign: "right", color: "#94a3b8" }}
                    >
                      {t.unit_price != null ? fmt(t.unit_price) : "—"}
                    </td>
                    <td
                      style={{
                        ...s.td,
                        textAlign: "right",
                        fontWeight: 700,
                        color: isSale ? "#10b981" : "#3b82f6",
                      }}
                    >
                      {t.total_amount != null ? fmt(t.total_amount) : "—"}
                    </td>
                    <td style={{ ...s.td, color: "#64748b", fontSize: 12 }}>
                      {t.notes || "—"}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
