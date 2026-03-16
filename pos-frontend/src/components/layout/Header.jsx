import { useClock } from "../../hooks/useClock";
import { useTax } from "../../context/TaxContext";
import { useCurrency } from "../../context/CurrencyContext";
import { useUser } from "../../context/UserContext";
import { generateBillNumber } from "../../utils/currency";
import { useState } from "react";

const billNum = generateBillNumber();

export default function Header({
  onOpenChat,
  onOpenTax,
  onOpenCurrency,
  onOpenCamera,
  onOpenDisplay,
  onOpenStock,
  onOpenTransactions,
  onOpenEOD,
  onOpenReturn,
  onSeedProducts,
  onLogout,
}) {
  const { time, date } = useClock();
  const { vatConfig } = useTax();
  const { currency } = useCurrency();
  const { user } = useUser();

  return (
    <header className="pos-header">
      <div className="header-left">
        <div className="header-logo">🛒</div>
        <div className="header-title">
          <h1>{user?.shop_name || "KiranaBuddy POS"}</h1>
          <p>
            {user ? `👤 ${user.name}` : "Point of Sale System"}
            {user?.phone && (
              <span style={{ marginLeft: 8, opacity: 0.6, fontWeight: 400 }}>
                📞 {user.phone}
              </span>
            )}
          </p>
        </div>
      </div>

      <div className="header-clock">
        <div className="clock-time">{time}</div>
        <div className="clock-date">{date}</div>
      </div>

      <div className="header-bill">
        <div className="bill-label">Bill No.</div>
        <div className="bill-num">#{billNum}</div>
      </div>

      <div className="header-right">
        <button className="header-btn" onClick={onOpenDisplay}>
          📺 Display
        </button>
        <button
          className="header-btn"
          onClick={onOpenStock}
          style={{ borderColor: "#10b981", color: "#10b981" }}
        >
          📦 Stock
        </button>
        <button
          className="header-btn"
          onClick={onOpenTransactions}
          style={{ borderColor: "#a78bfa", color: "#a78bfa" }}
        >
          📋 History
        </button>
        <button
          className="header-btn"
          onClick={onOpenEOD}
          style={{ borderColor: "#f59e0b", color: "#f59e0b" }}
        >
          📊 EOD
        </button>
        <button
          className="header-btn"
          onClick={onOpenReturn}
          style={{ borderColor: "#f87171", color: "#f87171" }}
        >
          ↩ Return
        </button>
        <button className="header-btn" onClick={onOpenCamera}>
          📷 Scan
        </button>
        <button className="header-btn chat-btn" onClick={onOpenChat}>
          💬 AI Chat
        </button>
        <button
          className="header-btn"
          onClick={onOpenCurrency}
          style={{ borderColor: "#38bdf8", color: "#38bdf8" }}
        >
          💱 {currency.symbol} {currency.code}
        </button>
        <button
          className="header-btn tax-btn"
          onClick={onOpenTax}
          style={{
            borderColor: vatConfig.enabled ? "#10b981" : "#a855f7",
            color: vatConfig.enabled ? "#10b981" : "#a855f7",
          }}
        >
          ⚙️ Tax: {vatConfig.enabled ? `${vatConfig.rate}%` : "Off"}
        </button>
        <button
          className="header-btn"
          onClick={onSeedProducts}
          style={{ borderColor: "#f59e0b", color: "#f59e0b" }}
        >
          📥 Import Products
        </button>
        <button className="header-btn danger" onClick={onLogout}>
          🚪 Logout
        </button>
      </div>
    </header>
  );
}
