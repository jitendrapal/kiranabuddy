import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext";
import {
  fetchProducts,
  fetchProductByBarcode,
  createProduct,
  addStockBill,
  patchProduct,
} from "../services/api";
import { fmt } from "../utils/currency";

const inputStyle = {
  width: "100%",
  padding: "10px 12px",
  background: "#0f172a",
  border: "1px solid #334155",
  borderRadius: 8,
  color: "#f1f5f9",
  fontSize: 14,
  marginBottom: 12,
  boxSizing: "border-box",
};
const labelStyle = {
  display: "block",
  fontSize: 13,
  color: "#94a3b8",
  marginBottom: 4,
};
const btn = (color, sm) => ({
  padding: sm ? "6px 12px" : "10px 18px",
  background: "transparent",
  border: `1.5px solid ${color}`,
  borderRadius: 8,
  color,
  cursor: "pointer",
  fontSize: sm ? 13 : 14,
  fontWeight: 600,
  whiteSpace: "nowrap",
});

function Modal({ children, onClose }) {
  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.75)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: "#1e293b",
          borderRadius: 12,
          padding: 28,
          minWidth: 360,
          maxWidth: 480,
          width: "92%",
          border: "1px solid #334155",
        }}
      >
        {children}
      </div>
    </div>
  );
}

// Returns expiry status info for color-coding
function expiryStatus(dateStr) {
  if (!dateStr) return null;
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const exp = new Date(dateStr);
  const diffDays = Math.floor((exp - today) / (1000 * 60 * 60 * 24));
  if (diffDays < 0)
    return { label: "Expired", color: "#ef4444", bg: "#450a0a", icon: "⛔" };
  if (diffDays === 0)
    return {
      label: "Expires today",
      color: "#f97316",
      bg: "#431407",
      icon: "⚠️",
    };
  if (diffDays <= 30)
    return {
      label: `${diffDays}d left`,
      color: "#f59e0b",
      bg: "#451a03",
      icon: "⚠️",
    };
  return { label: dateStr, color: "#10b981", bg: "transparent", icon: null };
}

export default function StockPage() {
  const { user } = useUser();
  const navigate = useNavigate();
  const barcodeRef = useRef(null);

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [barcode, setBarcode] = useState("");

  // Add stock modal state
  const [stockModal, setStockModal] = useState(null);
  const [stockQty, setStockQty] = useState("");
  const [stockCost, setStockCost] = useState("");

  // New product modal state
  const [newModal, setNewModal] = useState(false);
  const [newForm, setNewForm] = useState({
    barcode: "",
    name: "",
    brand: "",
    quantity: "",
    unit: "pieces",
    selling_price: "",
    cost_price: "",
    expiry_date: "",
  });

  // Edit product modal state
  const [editModal, setEditModal] = useState(null); // product object
  const [editForm, setEditForm] = useState({});

  const [msg, setMsg] = useState("");
  const [saving, setSaving] = useState(false);
  const [stockFilter, setStockFilter] = useState("all"); // "all" | "low" | "out"

  const LOW_STOCK_THRESHOLD = 5;

  useEffect(() => {
    loadProducts();
  }, []);

  async function loadProducts() {
    setLoading(true);
    try {
      const res = await fetchProducts(user.phone);
      setProducts(res.data?.products || []);
    } catch {
      setProducts([]);
    } finally {
      setLoading(false);
    }
  }

  async function handleBarcodeSubmit(e) {
    e.preventDefault();
    const v = barcode.trim();
    if (!v) return;
    setBarcode("");
    setMsg("");
    try {
      const res = await fetchProductByBarcode(v, user.phone);
      const p = res.data?.product;
      if (p) {
        const full = products.find(
          (pr) => pr.barcode === v || pr.name === p.name,
        ) || { ...p, current_stock: p.current_stock ?? 0 };
        setStockModal(full);
        setStockQty("");
        setStockCost("");
      } else {
        openNewForm(v);
      }
    } catch {
      openNewForm(v);
    }
  }

  function openNewForm(prefillBarcode = "") {
    setNewForm({
      barcode: prefillBarcode,
      name: "",
      brand: "",
      quantity: "",
      unit: "pieces",
      selling_price: "",
      cost_price: "",
    });
    setMsg("");
    setNewModal(true);
  }

  async function handleAddStock() {
    const qty = parseFloat(stockQty);
    if (!qty || qty <= 0) {
      setMsg("Enter a valid quantity");
      return;
    }
    setSaving(true);
    setMsg("");
    try {
      await addStockBill(user.phone, [
        {
          product_id: stockModal.product_id,
          name: stockModal.name,
          quantity: qty,
          cost_price: parseFloat(stockCost) || null,
        },
      ]);
      setStockModal(null);
      loadProducts();
    } catch (e) {
      setMsg(e.response?.data?.message || "Error adding stock");
    } finally {
      setSaving(false);
    }
  }

  function openEditForm(p) {
    setEditForm({
      name: p.name || "",
      barcode: p.barcode || "",
      selling_price: p.selling_price != null ? String(p.selling_price) : "",
      cost_price: p.cost_price != null ? String(p.cost_price) : "",
      unit: p.unit || "pieces",
      expiry_date: p.expiry_date || "",
    });
    setMsg("");
    setEditModal(p);
  }

  async function handleEditProduct() {
    if (!editForm.name.trim()) {
      setMsg("Product name is required");
      return;
    }
    setSaving(true);
    setMsg("");
    try {
      const updates = {
        name: editForm.name.trim(),
        barcode: editForm.barcode.trim() || null,
        selling_price: parseFloat(editForm.selling_price) || null,
        cost_price: parseFloat(editForm.cost_price) || null,
        unit: editForm.unit,
        expiry_date: editForm.expiry_date || null,
      };
      await patchProduct(editModal.product_id, user.phone, updates);
      setEditModal(null);
      loadProducts();
    } catch (e) {
      setMsg(e.response?.data?.message || "Error saving changes");
    } finally {
      setSaving(false);
    }
  }

  async function handleCreateProduct() {
    const {
      barcode: bc,
      name,
      quantity,
      unit,
      selling_price,
      cost_price,
      brand,
      expiry_date,
    } = newForm;
    if (!name.trim() || !quantity) {
      setMsg("Name and quantity are required");
      return;
    }
    setSaving(true);
    setMsg("");
    try {
      await createProduct({
        phone: user.phone,
        barcode: bc,
        name: name.trim(),
        brand: brand || null,
        quantity: parseFloat(quantity),
        unit,
        selling_price: parseFloat(selling_price) || null,
        cost_price: parseFloat(cost_price) || null,
        expiry_date: expiry_date || null,
      });
      setNewModal(false);
      loadProducts();
    } catch (e) {
      setMsg(e.response?.data?.message || "Error creating product");
    } finally {
      setSaving(false);
    }
  }

  const lowStockCount = products.filter(
    (p) =>
      (p.current_stock ?? 0) > 0 &&
      (p.current_stock ?? 0) <= LOW_STOCK_THRESHOLD,
  ).length;
  const outOfStockCount = products.filter(
    (p) => (p.current_stock ?? 0) <= 0,
  ).length;

  const filtered = products
    .filter(
      (p) =>
        (p.name || "").toLowerCase().includes(search.toLowerCase()) ||
        (p.barcode || "").toLowerCase().includes(search.toLowerCase()),
    )
    .filter((p) => {
      if (stockFilter === "low")
        return (
          (p.current_stock ?? 0) > 0 &&
          (p.current_stock ?? 0) <= LOW_STOCK_THRESHOLD
        );
      if (stockFilter === "out") return (p.current_stock ?? 0) <= 0;
      return true;
    });

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#0f172a",
        color: "#f1f5f9",
        fontFamily: "sans-serif",
      }}
    >
      {/* Top bar */}
      <div
        style={{
          padding: "14px 24px",
          background: "#1e293b",
          display: "flex",
          alignItems: "center",
          gap: 14,
          borderBottom: "1px solid #334155",
        }}
      >
        <button onClick={() => navigate("/pos")} style={btn("#64748b")}>
          ← Back to POS
        </button>
        <h1 style={{ margin: 0, fontSize: 20, flex: 1 }}>
          📦 Stock Management
        </h1>
        <button onClick={() => openNewForm()} style={btn("#10b981")}>
          + Add New Product
        </button>
      </div>

      {/* Barcode scan row */}
      <div
        style={{
          padding: "18px 24px",
          background: "#1e293b",
          borderBottom: "1px solid #334155",
        }}
      >
        <form
          onSubmit={handleBarcodeSubmit}
          style={{ display: "flex", gap: 10, maxWidth: 520 }}
        >
          <input
            ref={barcodeRef}
            autoFocus
            value={barcode}
            onChange={(e) => setBarcode(e.target.value)}
            placeholder="🔍 Scan barcode or type barcode and press Enter..."
            style={{ ...inputStyle, marginBottom: 0, flex: 1 }}
          />
          <button type="submit" style={btn("#3b82f6")}>
            Search
          </button>
        </form>
        <p style={{ margin: "8px 0 0", fontSize: 12, color: "#64748b" }}>
          Found → opens Add Stock. Not found → opens Add New Product form.
        </p>
      </div>

      {/* Low-stock alert banner */}
      {(lowStockCount > 0 || outOfStockCount > 0) && (
        <div
          style={{
            margin: "16px 24px 0",
            padding: "12px 18px",
            borderRadius: 10,
            background: outOfStockCount > 0 ? "#450a0a" : "#451a03",
            border: `1px solid ${outOfStockCount > 0 ? "#ef4444" : "#f59e0b"}`,
            display: "flex",
            gap: 24,
            alignItems: "center",
            flexWrap: "wrap",
          }}
        >
          <span style={{ fontWeight: 700, fontSize: 14, color: "#f1f5f9" }}>
            ⚠️ Stock Alerts
          </span>
          {outOfStockCount > 0 && (
            <span
              style={{ color: "#ef4444", fontSize: 13, cursor: "pointer" }}
              onClick={() => setStockFilter("out")}
            >
              ⛔ <strong>{outOfStockCount}</strong> out of stock
            </span>
          )}
          {lowStockCount > 0 && (
            <span
              style={{ color: "#f59e0b", fontSize: 13, cursor: "pointer" }}
              onClick={() => setStockFilter("low")}
            >
              ⚠️ <strong>{lowStockCount}</strong> low stock (≤
              {LOW_STOCK_THRESHOLD})
            </span>
          )}
          <span
            style={{
              marginLeft: "auto",
              color: "#64748b",
              fontSize: 12,
              cursor: "pointer",
            }}
            onClick={() => setStockFilter("all")}
          >
            Click to filter →
          </span>
        </div>
      )}

      {/* Product table */}
      <div style={{ padding: "20px 24px" }}>
        <div
          style={{
            display: "flex",
            gap: 12,
            marginBottom: 16,
            alignItems: "center",
            flexWrap: "wrap",
          }}
        >
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="🔎 Search by name or barcode..."
            style={{ ...inputStyle, marginBottom: 0, maxWidth: 280 }}
          />
          {/* Stock filter tabs */}
          {[
            { key: "all", label: "All", color: "#94a3b8" },
            {
              key: "low",
              label: `⚠️ Low Stock (${lowStockCount})`,
              color: "#f59e0b",
            },
            {
              key: "out",
              label: `⛔ Out of Stock (${outOfStockCount})`,
              color: "#ef4444",
            },
          ].map(({ key, label, color }) => (
            <button
              key={key}
              onClick={() => setStockFilter(key)}
              style={{
                padding: "6px 14px",
                borderRadius: 8,
                border: `1.5px solid ${stockFilter === key ? color : "#334155"}`,
                background: stockFilter === key ? color + "22" : "transparent",
                color: stockFilter === key ? color : "#64748b",
                cursor: "pointer",
                fontSize: 13,
                fontWeight: 600,
              }}
            >
              {label}
            </button>
          ))}
          <span style={{ color: "#64748b", fontSize: 13, marginLeft: "auto" }}>
            {filtered.length} products
          </span>
        </div>

        {loading ? (
          <p style={{ color: "#94a3b8" }}>⏳ Loading products...</p>
        ) : filtered.length === 0 ? (
          <div
            style={{ textAlign: "center", padding: "60px 0", color: "#64748b" }}
          >
            <div style={{ fontSize: 48, marginBottom: 12 }}>📭</div>
            <p>
              No products yet. Click{" "}
              <strong style={{ color: "#10b981" }}>+ Add New Product</strong> to
              get started.
            </p>
          </div>
        ) : (
          <div style={{ overflowX: "auto" }}>
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                fontSize: 14,
              }}
            >
              <thead>
                <tr style={{ background: "#1e293b" }}>
                  {[
                    "Product Name",
                    "Barcode",
                    "Stock",
                    "Unit",
                    "Sell Price",
                    "Cost Price",
                    "Expiry",
                    "Actions",
                  ].map((h) => (
                    <th
                      key={h}
                      style={{
                        padding: "10px 14px",
                        color: "#94a3b8",
                        fontWeight: 600,
                        textAlign: "left",
                        borderBottom: "1px solid #334155",
                      }}
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filtered.map((p, i) => {
                  const stock = p.current_stock ?? 0;
                  const isOut = stock <= 0;
                  const isLow = !isOut && stock <= LOW_STOCK_THRESHOLD;
                  const rowBg = isOut
                    ? "#2d0a0a"
                    : isLow
                      ? "#2d1a00"
                      : i % 2 === 0
                        ? "#0f172a"
                        : "#111827";
                  return (
                    <tr
                      key={p.product_id || i}
                      style={{
                        background: rowBg,
                        borderBottom: "1px solid #1e293b",
                        borderLeft: isOut
                          ? "3px solid #ef4444"
                          : isLow
                            ? "3px solid #f59e0b"
                            : "3px solid transparent",
                      }}
                    >
                      <td style={{ padding: "10px 14px", fontWeight: 500 }}>
                        {p.name}
                      </td>
                      <td
                        style={{
                          padding: "10px 14px",
                          color: "#64748b",
                          fontFamily: "monospace",
                          fontSize: 12,
                        }}
                      >
                        {p.barcode || "—"}
                      </td>
                      <td
                        style={{
                          padding: "10px 14px",
                          fontWeight: 700,
                          color:
                            (p.current_stock ?? 0) > 0 ? "#10b981" : "#ef4444",
                        }}
                      >
                        {p.current_stock ?? 0}
                      </td>
                      <td style={{ padding: "10px 14px", color: "#94a3b8" }}>
                        {p.unit || "—"}
                      </td>
                      <td style={{ padding: "10px 14px" }}>
                        {p.selling_price != null ? fmt(p.selling_price) : "—"}
                      </td>
                      <td style={{ padding: "10px 14px", color: "#64748b" }}>
                        {p.cost_price != null ? fmt(p.cost_price) : "—"}
                      </td>
                      <td style={{ padding: "10px 14px" }}>
                        {(() => {
                          const s = expiryStatus(p.expiry_date);
                          if (!s)
                            return (
                              <span style={{ color: "#475569", fontSize: 12 }}>
                                —
                              </span>
                            );
                          return (
                            <span
                              style={{
                                display: "inline-block",
                                padding: "2px 8px",
                                borderRadius: 6,
                                fontSize: 11,
                                fontWeight: 600,
                                background: s.bg,
                                color: s.color,
                                border: `1px solid ${s.color}40`,
                                whiteSpace: "nowrap",
                              }}
                            >
                              {s.icon ? s.icon + " " : ""}
                              {s.label}
                            </span>
                          );
                        })()}
                      </td>
                      <td style={{ padding: "10px 14px" }}>
                        <div style={{ display: "flex", gap: 6 }}>
                          <button
                            onClick={() => {
                              setStockModal(p);
                              setStockQty("");
                              setStockCost("");
                              setMsg("");
                            }}
                            style={btn("#3b82f6", true)}
                          >
                            + Stock
                          </button>
                          <button
                            onClick={() => openEditForm(p)}
                            style={btn("#a78bfa", true)}
                          >
                            ✏️ Edit
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Add Stock Modal */}
      {stockModal && (
        <Modal onClose={() => setStockModal(null)}>
          <h3 style={{ margin: "0 0 4px", fontSize: 18 }}>➕ Add Stock</h3>
          <p style={{ margin: "0 0 16px", color: "#94a3b8", fontSize: 14 }}>
            {stockModal.name}
          </p>
          <div
            style={{
              background: "#0f172a",
              borderRadius: 8,
              padding: "10px 14px",
              marginBottom: 16,
              fontSize: 13,
              color: "#94a3b8",
            }}
          >
            Current stock:{" "}
            <strong style={{ color: "#f1f5f9" }}>
              {stockModal.current_stock ?? 0} {stockModal.unit}
            </strong>
          </div>
          <label style={labelStyle}>Quantity to Add *</label>
          <input
            type="number"
            min="0.1"
            step="any"
            autoFocus
            value={stockQty}
            onChange={(e) => setStockQty(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAddStock()}
            placeholder="e.g. 24"
            style={inputStyle}
          />
          <label style={labelStyle}>Cost Price per Unit (optional)</label>
          <input
            type="number"
            min="0"
            step="any"
            value={stockCost}
            onChange={(e) => setStockCost(e.target.value)}
            placeholder="e.g. 10.50"
            style={inputStyle}
          />
          {msg && (
            <p style={{ color: "#ef4444", margin: "0 0 12px", fontSize: 13 }}>
              {msg}
            </p>
          )}
          <div style={{ display: "flex", gap: 10 }}>
            <button
              onClick={handleAddStock}
              disabled={saving}
              style={btn("#10b981")}
            >
              {saving ? "Saving…" : "✅ Add Stock"}
            </button>
            <button onClick={() => setStockModal(null)} style={btn("#64748b")}>
              Cancel
            </button>
          </div>
        </Modal>
      )}

      {/* New Product Modal */}
      {newModal && (
        <Modal onClose={() => setNewModal(false)}>
          <h3 style={{ margin: "0 0 16px", fontSize: 18 }}>
            + Add New Product
          </h3>
          {[
            ["Barcode", "barcode", "text", "e.g. 8901234567890"],
            ["Product Name *", "name", "text", "e.g. Maggi Noodles 70g"],
            ["Brand", "brand", "text", "e.g. Nestle"],
            ["Initial Quantity *", "quantity", "number", "e.g. 50"],
            ["Selling Price *", "selling_price", "number", "e.g. 12.00"],
            ["Cost Price", "cost_price", "number", "e.g. 10.00"],
          ].map(([label, field, type, placeholder]) => (
            <div key={field}>
              <label style={labelStyle}>{label}</label>
              <input
                type={type}
                value={newForm[field]}
                onChange={(e) =>
                  setNewForm((f) => ({ ...f, [field]: e.target.value }))
                }
                placeholder={placeholder}
                style={inputStyle}
              />
            </div>
          ))}
          <label style={labelStyle}>Unit</label>
          <select
            value={newForm.unit}
            onChange={(e) =>
              setNewForm((f) => ({ ...f, unit: e.target.value }))
            }
            style={inputStyle}
          >
            {["pieces", "kg", "gram", "litre", "packet", "box"].map((u) => (
              <option key={u} value={u}>
                {u}
              </option>
            ))}
          </select>
          <label style={labelStyle}>Expiry Date (optional)</label>
          <input
            type="date"
            value={newForm.expiry_date}
            onChange={(e) =>
              setNewForm((f) => ({ ...f, expiry_date: e.target.value }))
            }
            style={inputStyle}
          />
          {msg && (
            <p style={{ color: "#ef4444", margin: "0 0 12px", fontSize: 13 }}>
              {msg}
            </p>
          )}
          <div style={{ display: "flex", gap: 10 }}>
            <button
              onClick={handleCreateProduct}
              disabled={saving}
              style={btn("#10b981")}
            >
              {saving ? "Saving…" : "✅ Create Product"}
            </button>
            <button onClick={() => setNewModal(false)} style={btn("#64748b")}>
              Cancel
            </button>
          </div>
        </Modal>
      )}

      {/* Edit Product Modal */}
      {editModal && (
        <Modal onClose={() => setEditModal(null)}>
          <h3 style={{ margin: "0 0 16px", fontSize: 18 }}>✏️ Edit Product</h3>
          {[
            ["Product Name *", "name", "text", "e.g. Maggi Noodles 70g"],
            ["Barcode", "barcode", "text", "e.g. 8901234567890"],
            ["Selling Price", "selling_price", "number", "e.g. 14.00"],
            ["Cost Price", "cost_price", "number", "e.g. 10.50"],
          ].map(([label, field, type, placeholder]) => (
            <div key={field}>
              <label style={labelStyle}>{label}</label>
              <input
                type={type}
                value={editForm[field]}
                onChange={(e) =>
                  setEditForm((f) => ({ ...f, [field]: e.target.value }))
                }
                placeholder={placeholder}
                style={inputStyle}
              />
            </div>
          ))}
          <label style={labelStyle}>Unit</label>
          <select
            value={editForm.unit}
            onChange={(e) =>
              setEditForm((f) => ({ ...f, unit: e.target.value }))
            }
            style={inputStyle}
          >
            {["pieces", "kg", "gram", "litre", "packet", "box"].map((u) => (
              <option key={u} value={u}>
                {u}
              </option>
            ))}
          </select>
          <label style={labelStyle}>Expiry Date (optional)</label>
          <input
            type="date"
            value={editForm.expiry_date || ""}
            onChange={(e) =>
              setEditForm((f) => ({ ...f, expiry_date: e.target.value }))
            }
            style={inputStyle}
          />
          {msg && (
            <p style={{ color: "#ef4444", margin: "0 0 12px", fontSize: 13 }}>
              {msg}
            </p>
          )}
          <div style={{ display: "flex", gap: 10 }}>
            <button
              onClick={handleEditProduct}
              disabled={saving}
              style={btn("#a78bfa")}
            >
              {saving ? "Saving…" : "💾 Save Changes"}
            </button>
            <button onClick={() => setEditModal(null)} style={btn("#64748b")}>
              Cancel
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
}
