import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext";
import {
  fetchProducts,
  fetchProductByBarcode,
  createProduct,
  addStockBill,
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
  });

  const [msg, setMsg] = useState("");
  const [saving, setSaving] = useState(false);

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

  async function handleCreateProduct() {
    const {
      barcode: bc,
      name,
      quantity,
      unit,
      selling_price,
      cost_price,
      brand,
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
      });
      setNewModal(false);
      loadProducts();
    } catch (e) {
      setMsg(e.response?.data?.message || "Error creating product");
    } finally {
      setSaving(false);
    }
  }

  const filtered = products.filter(
    (p) =>
      (p.name || "").toLowerCase().includes(search.toLowerCase()) ||
      (p.barcode || "").toLowerCase().includes(search.toLowerCase()),
  );

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

      {/* Product table */}
      <div style={{ padding: "20px 24px" }}>
        <div
          style={{
            display: "flex",
            gap: 12,
            marginBottom: 16,
            alignItems: "center",
          }}
        >
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="🔎 Search by name or barcode..."
            style={{ ...inputStyle, marginBottom: 0, maxWidth: 320 }}
          />
          <span style={{ color: "#64748b", fontSize: 13 }}>
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
                    "Action",
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
                {filtered.map((p, i) => (
                  <tr
                    key={p.product_id || i}
                    style={{
                      background: i % 2 === 0 ? "#0f172a" : "#111827",
                      borderBottom: "1px solid #1e293b",
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
                    <td style={{ padding: "10px 14px" }}>
                      <button
                        onClick={() => {
                          setStockModal(p);
                          setStockQty("");
                          setStockCost("");
                          setMsg("");
                        }}
                        style={btn("#3b82f6", true)}
                      >
                        + Add Stock
                      </button>
                    </td>
                  </tr>
                ))}
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
    </div>
  );
}
