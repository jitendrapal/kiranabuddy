import { useState, useRef } from "react";
import { useUser } from "../../context/UserContext";
import { fetchProductByBarcode, processReturn } from "../../services/api";
import { fmt } from "../../utils/currency";

const inp = {
  width: "100%", padding: "10px 14px", background: "#0f172a",
  border: "1.5px solid #334155", borderRadius: 8, color: "#f1f5f9",
  fontSize: 14, outline: "none", boxSizing: "border-box",
};
const btn = (color) => ({
  flex: 1, padding: "10px 0", border: `1.5px solid ${color}`,
  borderRadius: 8, background: "transparent", color,
  fontSize: 14, fontWeight: 700, cursor: "pointer",
});

export default function ReturnModal({ onClose }) {
  const { user } = useUser();

  const [query, setQuery]       = useState("");
  const [product, setProduct]   = useState(null);
  const [qty, setQty]           = useState("1");
  const [searching, setSearching] = useState(false);
  const [saving, setSaving]     = useState(false);
  const [error, setError]       = useState("");
  const [success, setSuccess]   = useState(null); // { name, qty, refund }
  const qtyRef = useRef(null);

  async function handleSearch(e) {
    e.preventDefault();
    const q = query.trim();
    if (!q) return;
    setError(""); setProduct(null); setSuccess(null);
    setSearching(true);
    try {
      const res = await fetchProductByBarcode(q, user.phone);
      const p = res.data?.product;
      if (p) {
        setProduct(p);
        setTimeout(() => qtyRef.current?.focus(), 50);
      } else {
        setError(`No product found for "${q}". Try a different barcode or name.`);
      }
    } catch {
      setError("Error looking up product. Check connection.");
    } finally { setSearching(false); }
  }

  async function handleConfirm() {
    const q = parseFloat(qty);
    if (!product || !q || q <= 0) { setError("Enter a valid quantity."); return; }
    setSaving(true); setError("");
    try {
      await processReturn(user.phone, [{
        name: product.name,
        barcode: product.barcode || "",
        quantity: q,
      }]);
      const refund = product.selling_price ? product.selling_price * q : null;
      setSuccess({ name: product.name, qty: q, refund });
      setProduct(null); setQuery(""); setQty("1");
    } catch (e) {
      setError(e.response?.data?.message || "Return failed.");
    } finally { setSaving(false); }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div onClick={e => e.stopPropagation()} style={{
        background: "#1e293b", borderRadius: 14, width: 440, maxWidth: "95vw",
        border: "1px solid #334155", boxShadow: "0 24px 60px rgba(0,0,0,0.5)",
        color: "#f1f5f9", overflow: "hidden",
      }}>
        {/* Header */}
        <div style={{ padding: "18px 22px", background: "#0f172a", borderBottom: "1px solid #334155", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div style={{ fontWeight: 800, fontSize: 18 }}>↩ Process Return</div>
          <button onClick={onClose} style={{ background: "none", border: "none", color: "#94a3b8", fontSize: 20, cursor: "pointer" }}>✕</button>
        </div>

        <div style={{ padding: "20px 22px", display: "flex", flexDirection: "column", gap: 16 }}>

          {/* Step 1 — Search */}
          <form onSubmit={handleSearch}>
            <label style={{ fontSize: 12, color: "#64748b", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.05em", display: "block", marginBottom: 6 }}>
              Scan barcode or enter product name
            </label>
            <div style={{ display: "flex", gap: 8 }}>
              <input
                style={inp} autoFocus value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="e.g. 8901234567890 or Maggi"
              />
              <button type="submit" disabled={searching} style={{ ...btn("#3b82f6"), flex: "none", padding: "10px 16px", whiteSpace: "nowrap" }}>
                {searching ? "…" : "Find"}
              </button>
            </div>
          </form>

          {/* Error */}
          {error && (
            <div style={{ background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 8, padding: "10px 14px", color: "#dc2626", fontSize: 13 }}>
              ⚠️ {error}
            </div>
          )}

          {/* Success */}
          {success && (
            <div style={{ background: "#f0fdf4", border: "2px solid #86efac", borderRadius: 10, padding: "14px 18px", color: "#166534" }}>
              <div style={{ fontWeight: 800, fontSize: 15, marginBottom: 4 }}>✅ Return Processed</div>
              <div style={{ fontSize: 13 }}><strong>{success.name}</strong> — {success.qty} unit{success.qty !== 1 ? "s" : ""} returned</div>
              {success.refund != null && (
                <div style={{ fontSize: 22, fontWeight: 900, color: "#16a34a", marginTop: 6 }}>
                  Refund: {fmt(success.refund)}
                </div>
              )}
            </div>
          )}

          {/* Step 2 — Product found */}
          {product && (
            <>
              <div style={{ background: "#0f172a", borderRadius: 10, padding: "14px 16px", border: "1px solid #334155" }}>
                <div style={{ fontSize: 16, fontWeight: 700, marginBottom: 4 }}>{product.name}</div>
                <div style={{ display: "flex", gap: 16, fontSize: 13, color: "#94a3b8" }}>
                  <span>Stock: <strong style={{ color: "#f1f5f9" }}>{product.current_stock ?? "—"}</strong></span>
                  {product.selling_price && <span>Price: <strong style={{ color: "#10b981" }}>{fmt(product.selling_price)}</strong></span>}
                  {product.barcode && <span>Barcode: <code style={{ color: "#64748b" }}>{product.barcode}</code></span>}
                </div>
              </div>

              <div>
                <label style={{ fontSize: 12, color: "#64748b", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.05em", display: "block", marginBottom: 6 }}>
                  Quantity to Return
                </label>
                <input
                  ref={qtyRef} type="number" min="0.1" step="any"
                  value={qty} onChange={e => setQty(e.target.value)}
                  onKeyDown={e => e.key === "Enter" && handleConfirm()}
                  style={inp}
                />
                {product.selling_price && parseFloat(qty) > 0 && (
                  <div style={{ marginTop: 8, fontSize: 13, color: "#94a3b8" }}>
                    Refund to customer: <strong style={{ color: "#10b981", fontSize: 16 }}>{fmt(product.selling_price * parseFloat(qty))}</strong>
                  </div>
                )}
              </div>

              <div style={{ display: "flex", gap: 10 }}>
                <button onClick={handleConfirm} disabled={saving} style={btn("#10b981")}>
                  {saving ? "Processing…" : "✅ Confirm Return"}
                </button>
                <button onClick={() => { setProduct(null); setQuery(""); }} style={btn("#64748b")}>
                  Cancel
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

