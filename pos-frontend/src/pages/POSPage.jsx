import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext";
import { useCart } from "../context/CartContext";
import { useProducts } from "../hooks/useProducts";
import {
  fetchProductByBarcode,
  seedDemoProducts,
  logout as apiLogout,
} from "../services/api";
import Header from "../components/layout/Header";
import StatusBar from "../components/layout/StatusBar";
import ProductGrid from "../components/pos/ProductGrid";
import CartPanel from "../components/pos/CartPanel";
import WeightModal from "../components/modals/WeightModal";
import PaymentModal from "../components/modals/PaymentModal";
import ReceiptModal from "../components/modals/ReceiptModal";
import TaxModal from "../components/modals/TaxModal";
import ChatPopup from "../components/modals/ChatPopup";

export default function POSPage() {
  const { user, setUser } = useUser();
  const { cart, dispatch } = useCart();
  const navigate = useNavigate();
  const barcodeRef = useRef(null);

  const {
    products,
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
        onOpenDisplay={() => window.open("/customer-display", "_blank")}
        onOpenStock={() => navigate("/stock")}
        onOpenTransactions={() => navigate("/transactions")}
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
    </div>
  );
}
