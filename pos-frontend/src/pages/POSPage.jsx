import { useState, useRef, useEffect } from "react";
import { useBarcodeScanner } from "../hooks/useBarcodeScanner";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext";
import { useCart } from "../context/CartContext";
import { useProducts } from "../hooks/useProducts";
import {
  fetchProductByBarcode,
  seedDemoProducts,
  logout as apiLogout,
  createDisplaySession,
  updateDisplaySession,
} from "../services/api";
import Header from "../components/layout/Header";
import StatusBar from "../components/layout/StatusBar";
import ProductGrid from "../components/pos/ProductGrid";
import CartPanel from "../components/pos/CartPanel";
import QuickSearch from "../components/pos/QuickSearch";
import WeightModal from "../components/modals/WeightModal";
import PaymentModal from "../components/modals/PaymentModal";
import ReceiptModal from "../components/modals/ReceiptModal";
import EODReportModal from "../components/modals/EODReportModal";
import ReturnModal from "../components/modals/ReturnModal";
import TaxModal from "../components/modals/TaxModal";
import ChatPopup from "../components/modals/ChatPopup";

export default function POSPage() {
  const { user, setUser } = useUser();
  const { cart, dispatch } = useCart();
  const navigate = useNavigate();
  const barcodeRef = useRef(null);

  const {
    products,
    allProducts,
    totalCount,
    loading,
    category,
    setCategory,
    search,
    setSearch,
    reload,
    applyStockReductions,
  } = useProducts(user?.phone);

  const [weightProduct, setWeightProduct] = useState(null);
  const [checkoutData, setCheckoutData] = useState(null);
  const [receipt, setReceipt] = useState(null);
  const [showTax, setShowTax] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [showEOD, setShowEOD] = useState(false);
  const [showReturn, setShowReturn] = useState(false);
  const [showQuickSearch, setShowQuickSearch] = useState(false);
  const [scanToast, setScanToast] = useState(null); // { name, barcode }
  const displaySessionId = useRef(null); // customer display session ID
  const toastTimer = useRef(null);

  const anyModalOpen =
    !!checkoutData ||
    !!weightProduct ||
    !!receipt ||
    showTax ||
    showChat ||
    showEOD ||
    showQuickSearch ||
    showReturn;

  // Open QuickSearch with "/" key when no input is focused and no modal open
  useEffect(() => {
    function onKey(e) {
      if (anyModalOpen) return;
      const tag = document.activeElement?.tagName ?? "";
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      if (e.key === "/") {
        e.preventDefault();
        setShowQuickSearch(true);
      }
    }
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [anyModalOpen]);

  // Push cart to customer display whenever cart changes
  useEffect(() => {
    if (!displaySessionId.current) return;
    // If name looks like a raw barcode (all digits, 6+ chars), show friendly label
    const friendlyName = (name) =>
      /^[0-9]{6,}$/.test(name) ? "Item (barcode: " + name + ")" : name;
    const items = cart
      .filter((i) => Math.abs(i.delta || 0) > 0)
      .map((i) => {
        const qty = Math.abs(i.delta || 0);
        const price = i.price ?? null;
        return {
          name: friendlyName(i.name),
          qty,
          unit: i.unit || "",
          unit_price: price,
          line_total: price != null ? price * qty : null,
        };
      });
    const grand_total = items.reduce((s, i) => s + (i.line_total || 0), 0);
    updateDisplaySession(displaySessionId.current, {
      items,
      grand_total,
      status: "active",
    }).catch(() => {});
  }, [cart]);

  // Global barcode scanner — fires when USB scanner sends barcode+Enter
  useBarcodeScanner(
    async (code) => {
      await handleBarcodeSubmit(code);
      // Show a brief toast so the cashier sees what was scanned
      clearTimeout(toastTimer.current);
      const matched = products.find(
        (p) => (p.barcode || "").toLowerCase() === code.toLowerCase(),
      );
      setScanToast({ name: matched?.name || code, barcode: code });
      toastTimer.current = setTimeout(() => setScanToast(null), 2000);
    },
    { disabled: anyModalOpen },
  );

  function handleProductClick(product) {
    if (
      product.stock !== null &&
      product.stock !== undefined &&
      product.stock <= 0
    )
      return; // block out-of-stock
    if (product.isWeight) {
      setWeightProduct(product);
      return;
    }
    dispatch({
      type: "ADD_REGULAR",
      code: product.barcode,
      name: product.name,
      price: product.price,
      stock: product.stock,
    });
    playScanBeep();
  }

  async function handleBarcodeSubmit(value) {
    const v = value.trim();
    if (!v) return;

    // ── Fast path: product already loaded in memory ──────────────────────────
    const local = allProducts.find(
      (p) => (p.barcode || "").toLowerCase() === v.toLowerCase(),
    );
    if (local) {
      if (local.isWeight) {
        setWeightProduct({ ...local, barcode: v });
      } else {
        dispatch({
          type: "ADD_REGULAR",
          code: v,
          name: local.name,
          price: local.price,
          stock: local.stock,
        });
        playScanBeep();
      }
      return; // done — no network call needed
    }

    // ── Slow path: not in local list, ask the server ──────────────────────────
    try {
      const res = await fetchProductByBarcode(v, user?.phone);
      const p = res.data?.product;
      if (p) {
        const isWeight = !!(p.per_kg || p.unit === "kg");
        const price = parseFloat(p.selling_price ?? p.price ?? 0);
        if (isWeight) {
          setWeightProduct({ ...p, price, barcode: v });
        } else {
          dispatch({ type: "ADD_REGULAR", code: v, name: p.name, price });
          playScanBeep();
        }
      } else {
        dispatch({ type: "ADD_REGULAR", code: v, name: v, price: 0 });
        playScanBeep();
      }
    } catch {
      dispatch({ type: "ADD_REGULAR", code: v, name: v, price: 0 });
      playScanBeep();
    }
  }

  function playScanBeep() {
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.connect(g);
      g.connect(ctx.destination);
      o.frequency.value = 880;
      g.gain.setValueAtTime(0.3, ctx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.15);
      o.start();
      o.stop(ctx.currentTime + 0.15);
    } catch {}
  }

  async function handleSeedProducts() {
    if (
      !confirm(
        "Import demo products to database? Existing products will be skipped.",
      )
    )
      return;
    try {
      const res = await seedDemoProducts(user?.phone);
      alert("✅ " + res.data.message);
      reload();
    } catch (e) {
      alert("Error: " + e.message);
    }
  }

  async function handleLogout() {
    await apiLogout().catch(() => {});
    setUser(null);
    navigate("/login");
  }

  return (
    <div className="pos-app">
      <Header
        onOpenChat={() => setShowChat(true)}
        onOpenTax={() => setShowTax(true)}
        onOpenCamera={() => alert("Camera scan coming soon")}
        onOpenDisplay={async () => {
          try {
            const res = await createDisplaySession(
              user?.shop_name || "KiranaBuddy",
            );
            if (res.data?.success) {
              displaySessionId.current = res.data.session_id;
              window.open(
                `/customer-display?session=${res.data.session_id}`,
                "CustomerDisplay",
                "width=1280,height=720",
              );
            }
          } catch (e) {
            console.error("Failed to open customer display", e);
          }
        }}
        onOpenStock={() => navigate("/stock")}
        onOpenTransactions={() => navigate("/transactions")}
        onOpenEOD={() => setShowEOD(true)}
        onOpenReturn={() => setShowReturn(true)}
        onSeedProducts={handleSeedProducts}
        onLogout={handleLogout}
      />
      <StatusBar />
      <div className="pos-content">
        <ProductGrid
          products={products}
          totalCount={totalCount}
          loading={loading}
          category={category}
          onCategoryChange={setCategory}
          search={search}
          onSearchChange={setSearch}
          barcodeRef={barcodeRef}
          onBarcodeSubmit={handleBarcodeSubmit}
          onProductClick={handleProductClick}
        />
        <CartPanel onCheckout={(data) => setCheckoutData(data)} />
      </div>

      {weightProduct && (
        <WeightModal
          product={weightProduct}
          onClose={() => setWeightProduct(null)}
        />
      )}
      {checkoutData !== null && (
        <PaymentModal
          checkoutData={checkoutData}
          onClose={() => setCheckoutData(null)}
          onSuccess={(receiptData) => {
            const soldItems = cart
              .filter((i) => i.delta !== 0)
              .map((i) => ({
                name: i.name,
                barcode: i.displayCode || i.code,
                quantity: Math.abs(i.delta || 0),
              }));
            applyStockReductions(soldItems);
            // Tell customer display: payment done → show "Thank You" screen
            if (displaySessionId.current) {
              updateDisplaySession(displaySessionId.current, {
                status: "checked_out",
                grand_total: receiptData?.total || 0,
              }).catch(() => {});
              // After 4 seconds reset display back to idle
              setTimeout(() => {
                if (displaySessionId.current) {
                  updateDisplaySession(displaySessionId.current, {
                    items: [],
                    grand_total: 0,
                    status: "active",
                  }).catch(() => {});
                }
              }, 4000);
            }
            dispatch({ type: "CLEAR" });
            setCheckoutData(null);
            setReceipt(receiptData);
            reload();
          }}
        />
      )}
      {receipt && (
        <ReceiptModal receipt={receipt} onClose={() => setReceipt(null)} />
      )}
      {showTax && <TaxModal onClose={() => setShowTax(false)} />}
      {showChat && <ChatPopup onClose={() => setShowChat(false)} />}
      {showEOD && <EODReportModal onClose={() => setShowEOD(false)} />}
      {showReturn && <ReturnModal onClose={() => setShowReturn(false)} />}

      {showQuickSearch && (
        <QuickSearch
          products={products}
          onAdd={(product) => {
            handleProductClick(product);
          }}
          onClose={() => setShowQuickSearch(false)}
        />
      )}

      {/* Scan toast — bottom-right notification when barcode is scanned */}
      {scanToast && (
        <div
          style={{
            position: "fixed",
            bottom: 24,
            right: 24,
            zIndex: 2000,
            background: "#0f172a",
            border: "2px solid #10b981",
            borderRadius: 12,
            padding: "12px 20px",
            display: "flex",
            alignItems: "center",
            gap: 12,
            boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
            animation: "slideInRight 0.2s ease",
          }}
        >
          <span style={{ fontSize: 22 }}>📷</span>
          <div>
            <div style={{ fontSize: 13, color: "#10b981", fontWeight: 700 }}>
              Barcode Scanned
            </div>
            <div style={{ fontSize: 15, color: "#f1f5f9", fontWeight: 600 }}>
              {scanToast.name}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
