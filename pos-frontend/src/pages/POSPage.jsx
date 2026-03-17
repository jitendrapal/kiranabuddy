import { useState, useRef, useEffect } from "react";
import { useBarcodeScanner } from "../hooks/useBarcodeScanner";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext";
import { useCart } from "../context/CartContext";
import { useTax } from "../context/TaxContext";
import { useCurrency } from "../context/CurrencyContext";
import { calcTax } from "../utils/taxCalculator";
import { cartSubtotal } from "../utils/cartHelpers";
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
import CurrencyModal from "../components/modals/CurrencyModal";
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
    lowStockCount,
  } = useProducts(user?.phone);
  const { vatConfig } = useTax();
  const { currency } = useCurrency();

  const [weightProduct, setWeightProduct] = useState(null);
  const [checkoutData, setCheckoutData] = useState(null);
  const [receipt, setReceipt] = useState(null);
  const [showTax, setShowTax] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [showEOD, setShowEOD] = useState(false);
  const [showReturn, setShowReturn] = useState(false);
  const [showCurrency, setShowCurrency] = useState(false);
  const [showQuickSearch, setShowQuickSearch] = useState(false);
  const [scanToast, setScanToast] = useState(null); // { name, barcode }
  const displaySessionId = useRef(null); // customer display session ID
  const displayBroadcast = useRef(null); // BroadcastChannel for same-device instant push
  const toastTimer = useRef(null);
  const checkingOut = useRef(false); // true while Thank You screen is showing — suppresses empty-cart broadcast
  const displayResetTimer = useRef(null); // holds the 4-s post-checkout reset timer so we can cancel it
  const weightKeepAlive = useRef(null); // interval that keeps broadcasting while WeightModal is open

  // Open BroadcastChannel once on mount, close on unmount
  useEffect(() => {
    try {
      displayBroadcast.current = new BroadcastChannel("kirana-display");
    } catch {
      displayBroadcast.current = null; // not supported in older browsers
    }
    return () => displayBroadcast.current?.close();
  }, []);

  const anyModalOpen =
    !!checkoutData ||
    !!weightProduct ||
    !!receipt ||
    showTax ||
    showChat ||
    showEOD ||
    showCurrency ||
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

  // Stores the last correctly-built payload so the weight keepalive can rebroadcast
  // it without a stale closure (setInterval cannot see re-rendered state values).
  const lastPayloadRef = useRef(null);

  // Push cart to customer display whenever cart or tax config changes.
  // Payload is built INLINE so it always uses the current render's values —
  // no stale-closure risk that a shared helper function could introduce.
  useEffect(() => {
    const friendlyName = (name) =>
      /^[0-9]{6,}$/.test(name) ? "Item (barcode: " + name + ")" : name;

    const items = cart
      .filter((i) => Math.abs(i.delta || 0) > 0)
      .map((i) => {
        if (i.isWeight) {
          // Weight items: show actual kg and per-kg price for clarity
          return {
            name: friendlyName(i.name),
            qty: i.weightKg,
            unit: "kg",
            unit_price: i.pricePerKg ?? null,
            line_total: i.price ?? null,
          };
        }
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

    if (items.length > 0 && checkingOut.current) {
      // New customer started scanning before the post-checkout 4s window expired.
      // Unlock immediately so their items broadcast right away.
      checkingOut.current = false;
      if (displayResetTimer.current) {
        clearTimeout(displayResetTimer.current);
        displayResetTimer.current = null;
      }
    }

    // Still suppress if locked AND cart is empty — that's the CLEAR dispatch
    // fired right after checkout; we don't want it to overwrite "Thank You".
    if (checkingOut.current) return;

    const raw = cartSubtotal(cart);
    const { taxAmt, total } = calcTax(raw, vatConfig);
    const payload = {
      items,
      subtotal: raw,
      tax_amt: taxAmt,
      tax_name: vatConfig.enabled ? vatConfig.name : null,
      tax_rate: vatConfig.enabled ? vatConfig.rate : 0,
      grand_total: total,
      currency: currency.symbol,
      status: "active",
    };

    lastPayloadRef.current = payload; // cache for keepalive reuse
    displayBroadcast.current?.postMessage(payload);
    if (displaySessionId.current) {
      updateDisplaySession(displaySessionId.current, payload).catch(() => {});
    }
  }, [cart, vatConfig, currency]);

  // Open the WeightModal and keep the customer display alive during weight entry.
  // Problem: dispatch(ADD_WEIGHT) only fires AFTER user confirms weight, which
  // can take 5-15 seconds. During that window the poll suppression timer expires
  // and the poll fetches stale server data, clearing the display.
  // Fix: rebroadcast the last known payload immediately (resets lastBroadcastAt)
  // and repeat every 2.5 s so the display is always suppressed while modal is open.
  function openWeightModal(product) {
    setWeightProduct(product);
    const sendKeepAlive = () => {
      if (lastPayloadRef.current) {
        displayBroadcast.current?.postMessage(lastPayloadRef.current);
      }
    };
    sendKeepAlive(); // immediate reset of poll-suppression timer
    weightKeepAlive.current = setInterval(sendKeepAlive, 2500);
  }

  // Close the WeightModal and stop the keepalive interval.
  function closeWeightModal() {
    if (weightKeepAlive.current) {
      clearInterval(weightKeepAlive.current);
      weightKeepAlive.current = null;
    }
    setWeightProduct(null);
  }

  // Global barcode scanner — fires when USB scanner sends barcode+Enter
  useBarcodeScanner(
    async (code) => {
      await handleBarcodeSubmit(code);
      // Show a brief toast — use allProducts (full list, ignores active filters)
      clearTimeout(toastTimer.current);
      const matched = allProducts.find(
        (p) => (p.barcode || "").toLowerCase() === code.toLowerCase(),
      );
      setScanToast({
        name: matched?.name || null, // null = not registered
        barcode: code,
        notRegistered: !matched,
      });
      toastTimer.current = setTimeout(() => setScanToast(null), 3000);
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
      openWeightModal(product);
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
        openWeightModal({ ...local, barcode: v });
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
          openWeightModal({ ...p, price, barcode: v });
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
        onOpenCurrency={() => setShowCurrency(true)}
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
        lowStockCount={lowStockCount}
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
        <WeightModal product={weightProduct} onClose={closeWeightModal} />
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
            const checkoutPayload = {
              status: "checked_out",
              grand_total: receiptData?.total || 0,
              items: [],
            };

            // Lock broadcasting BEFORE clearing the cart so the empty-cart
            // useEffect doesn't overwrite the "Thank You" message.
            checkingOut.current = true;
            displayBroadcast.current?.postMessage(checkoutPayload);
            if (displaySessionId.current) {
              updateDisplaySession(
                displaySessionId.current,
                checkoutPayload,
              ).catch(() => {});
            }

            // After 4 s reset display to idle and re-enable broadcasting.
            // Store the timer ID so it can be cancelled if a new customer
            // starts scanning before the 4 s window expires.
            displayResetTimer.current = setTimeout(() => {
              checkingOut.current = false;
              displayResetTimer.current = null;
              const idlePayload = {
                items: [],
                grand_total: 0,
                status: "active",
              };
              displayBroadcast.current?.postMessage(idlePayload);
              if (displaySessionId.current) {
                updateDisplaySession(
                  displaySessionId.current,
                  idlePayload,
                ).catch(() => {});
              }
            }, 4000);
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
      {showCurrency && <CurrencyModal onClose={() => setShowCurrency(false)} />}
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
            border: `2px solid ${scanToast.notRegistered ? "#f59e0b" : "#10b981"}`,
            borderRadius: 12,
            padding: "12px 20px",
            display: "flex",
            alignItems: "center",
            gap: 12,
            boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
            animation: "slideInRight 0.2s ease",
            maxWidth: 300,
          }}
        >
          <span style={{ fontSize: 22 }}>
            {scanToast.notRegistered ? "⚠️" : "📷"}
          </span>
          <div>
            <div
              style={{
                fontSize: 13,
                fontWeight: 700,
                color: scanToast.notRegistered ? "#f59e0b" : "#10b981",
              }}
            >
              {scanToast.notRegistered
                ? "Barcode not registered"
                : "Barcode Scanned"}
            </div>
            <div style={{ fontSize: 14, color: "#f1f5f9", fontWeight: 600 }}>
              {scanToast.notRegistered
                ? `${scanToast.barcode} — Go to Stock → Edit product → Add barcode`
                : scanToast.name}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
