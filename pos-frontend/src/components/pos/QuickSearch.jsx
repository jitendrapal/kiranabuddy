import { useState, useEffect, useRef } from "react";
import { fmt } from "../../utils/currency";

/**
 * QuickSearch — floating command-palette style product search.
 * Type a product name → arrow keys to navigate → Enter to add to cart.
 */
export default function QuickSearch({ products, onAdd, onClose }) {
  const [query, setQuery] = useState("");
  const [idx, setIdx]     = useState(0);
  const inputRef          = useRef(null);
  const listRef           = useRef(null);

  const results = products
    .filter((p) => (p.name || "").toLowerCase().includes(query.toLowerCase()))
    .slice(0, 8);

  // Auto-focus input on open
  useEffect(() => { inputRef.current?.focus(); }, []);

  // Reset selection when results change
  useEffect(() => { setIdx(0); }, [query]);

  // Scroll selected item into view
  useEffect(() => {
    const el = listRef.current?.children[idx];
    el?.scrollIntoView({ block: "nearest" });
  }, [idx]);

  function handleKeyDown(e) {
    if (e.key === "Escape") { onClose(); return; }
    if (e.key === "ArrowDown") { e.preventDefault(); setIdx((i) => Math.min(i + 1, results.length - 1)); return; }
    if (e.key === "ArrowUp")   { e.preventDefault(); setIdx((i) => Math.max(i - 1, 0)); return; }
    if (e.key === "Enter" && results[idx]) { handleSelect(results[idx]); return; }
  }

  function handleSelect(product) {
    if (product.stock !== null && product.stock !== undefined && product.stock <= 0) return;
    onAdd(product);
    setQuery("");
    setIdx(0);
    inputRef.current?.focus();
  }

  const outOfStock = (p) => p.stock !== null && p.stock !== undefined && p.stock <= 0;

  return (
    <>
      {/* Backdrop */}
      <div
        onClick={onClose}
        style={{
          position: "fixed", inset: 0, background: "rgba(0,0,0,0.55)",
          zIndex: 3000, backdropFilter: "blur(2px)",
        }}
      />

      {/* Panel */}
      <div style={{
        position: "fixed", top: "12%", left: "50%", transform: "translateX(-50%)",
        width: 520, maxWidth: "95vw", zIndex: 3001,
        background: "#1e293b", borderRadius: 14, border: "1px solid #334155",
        boxShadow: "0 24px 80px rgba(0,0,0,0.6)", overflow: "hidden",
      }}>
        {/* Search input */}
        <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "14px 16px", borderBottom: "1px solid #334155" }}>
          <span style={{ fontSize: 18 }}>🔍</span>
          <input
            ref={inputRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type product name to add to cart..."
            style={{
              flex: 1, background: "transparent", border: "none", outline: "none",
              color: "#f1f5f9", fontSize: 16, fontWeight: 500,
            }}
          />
          <kbd style={{ fontSize: 11, color: "#64748b", background: "#0f172a", border: "1px solid #334155", borderRadius: 4, padding: "2px 6px" }}>Esc</kbd>
        </div>

        {/* Results */}
        <div ref={listRef} style={{ maxHeight: 360, overflowY: "auto" }}>
          {results.length === 0 ? (
            <div style={{ padding: "28px 0", textAlign: "center", color: "#64748b", fontSize: 14 }}>
              {query ? `No products matching "${query}"` : "Start typing to search…"}
            </div>
          ) : (
            results.map((p, i) => {
              const oos      = outOfStock(p);
              const selected = i === idx;
              return (
                <div
                  key={p.barcode || i}
                  onClick={() => !oos && handleSelect(p)}
                  style={{
                    display: "flex", alignItems: "center", gap: 12,
                    padding: "11px 16px", cursor: oos ? "not-allowed" : "pointer",
                    background: selected ? "#334155" : "transparent",
                    opacity: oos ? 0.45 : 1,
                    borderBottom: "1px solid #0f172a",
                    transition: "background 0.1s",
                  }}
                  onMouseEnter={() => setIdx(i)}
                >
                  {/* Rank / Enter hint */}
                  <div style={{
                    width: 26, height: 26, borderRadius: 6, flexShrink: 0,
                    background: selected ? "#3b82f6" : "#0f172a",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: 11, fontWeight: 800, color: selected ? "#fff" : "#475569",
                  }}>
                    {selected ? "↵" : i + 1}
                  </div>

                  {/* Name */}
                  <span style={{ flex: 1, fontSize: 14, fontWeight: 600, color: "#f1f5f9" }}>{p.name}</span>

                  {/* Stock badge */}
                  {p.stock != null && (
                    <span style={{
                      fontSize: 11, fontWeight: 700, padding: "2px 8px", borderRadius: 20,
                      background: oos ? "#450a0a" : p.stock <= 5 ? "#451a03" : "#0f2918",
                      color: oos ? "#ef4444" : p.stock <= 5 ? "#f97316" : "#10b981",
                    }}>
                      {oos ? "Out" : `${p.stock} ${p.unit || ""}`}
                    </span>
                  )}

                  {/* Price */}
                  <span style={{ fontSize: 14, fontWeight: 700, color: "#10b981", minWidth: 52, textAlign: "right" }}>
                    {p.price ? fmt(p.price) : "—"}
                  </span>
                </div>
              );
            })
          )}
        </div>

        {/* Footer hint */}
        <div style={{ padding: "8px 16px", borderTop: "1px solid #334155", display: "flex", gap: 16, fontSize: 11, color: "#475569" }}>
          <span>↑↓ navigate</span>
          <span>↵ add to cart</span>
          <span>Esc close</span>
          <span style={{ marginLeft: "auto" }}>press <kbd style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 3, padding: "1px 5px" }}>/</kbd> to open</span>
        </div>
      </div>
    </>
  );
}

