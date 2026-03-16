import { useState } from "react";
import { fmt } from "../../utils/currency";
import { calcTax } from "../../utils/taxCalculator";
import { useTax } from "../../context/TaxContext";
import { useCurrency } from "../../context/CurrencyContext";
import { cartSubtotal } from "../../utils/cartHelpers";
import { useCart } from "../../context/CartContext";

export default function CartSummary({ onCheckout }) {
  const { cart, dispatch } = useCart();
  const { vatConfig } = useTax();
  const { currency } = useCurrency();

  const [discountValue, setDiscountValue] = useState("");
  const [discountType, setDiscountType] = useState("flat"); // "flat" | "pct"

  const raw = cartSubtotal(cart);

  // Compute discount amount
  const discountInput = parseFloat(discountValue) || 0;
  const discountAmt =
    discountType === "pct"
      ? Math.min(raw, (raw * discountInput) / 100)
      : Math.min(raw, discountInput);

  const afterDiscount = raw - discountAmt;
  const { subtotal, taxAmt, total } = calcTax(afterDiscount, vatConfig);

  function handleClear() {
    dispatch({ type: "CLEAR" });
    setDiscountValue("");
  }

  return (
    <div className="cart-summary">
      {/* Subtotal */}
      <div className="summary-row">
        <span>Subtotal</span>
        <span>{fmt(raw)}</span>
      </div>

      {/* Discount row */}
      <div className="discount-row">
        <span className="discount-label">Discount</span>
        <div className="discount-controls">
          <button
            className={`disc-type-btn${discountType === "flat" ? " active" : ""}`}
            onClick={() => setDiscountType("flat")}
          >
            {currency.symbol}
          </button>
          <button
            className={`disc-type-btn${discountType === "pct" ? " active" : ""}`}
            onClick={() => setDiscountType("pct")}
          >
            %
          </button>
          <input
            type="number"
            min="0"
            placeholder="0"
            value={discountValue}
            onChange={(e) => setDiscountValue(e.target.value)}
            className="discount-input"
          />
        </div>
        {discountAmt > 0 && (
          <span className="discount-amt">− {fmt(discountAmt)}</span>
        )}
      </div>

      {/* Tax */}
      <div
        className="summary-row tax"
        style={{ color: taxAmt > 0 ? "#f59e0b" : "#64748b" }}
      >
        <span>
          {vatConfig.name} ({vatConfig.rate}%)
        </span>
        <span>{fmt(taxAmt)}</span>
      </div>

      {/* Total */}
      <div className="summary-row total-row">
        <span>TOTAL</span>
        <span className="total-amount">{fmt(total)}</span>
      </div>

      <div className="cart-actions">
        <button className="cart-btn clear" onClick={handleClear}>
          🗑 Clear
        </button>
        <button
          className="cart-btn hold"
          onClick={() => dispatch({ type: "HOLD_BILL", total })}
          title="Park this bill and start a new one"
        >
          ⏸ Hold
        </button>
        <button
          className="cart-btn checkout"
          onClick={() =>
            onCheckout({ total, rawSubtotal: raw, discountAmt, taxAmt })
          }
        >
          💰 Pay
        </button>
      </div>
    </div>
  );
}
