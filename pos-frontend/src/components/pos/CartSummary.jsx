import { fmt } from "../../utils/currency";
import { calcTax } from "../../utils/taxCalculator";
import { useTax } from "../../context/TaxContext";
import { cartSubtotal } from "../../utils/cartHelpers";
import { useCart } from "../../context/CartContext";

export default function CartSummary({ onCheckout }) {
  const { cart, dispatch } = useCart();
  const { vatConfig } = useTax();
  const raw = cartSubtotal(cart);
  const { subtotal, taxAmt, total } = calcTax(raw, vatConfig);

  return (
    <div className="cart-summary">
      <div className="summary-row">
        <span>Subtotal</span>
        <span>{fmt(subtotal)}</span>
      </div>
      <div
        className="summary-row tax"
        style={{ color: taxAmt > 0 ? "#f59e0b" : "#64748b" }}
      >
        <span>
          {vatConfig.name} ({vatConfig.rate}%)
        </span>
        <span>{fmt(taxAmt)}</span>
      </div>
      <div className="summary-row total-row">
        <span>TOTAL</span>
        <span className="total-amount">{fmt(total)}</span>
      </div>
      <div className="cart-actions">
        <button
          className="cart-btn clear"
          onClick={() => dispatch({ type: "CLEAR" })}
        >
          🗑 Clear
        </button>
        <button className="cart-btn checkout" onClick={() => onCheckout(total)}>
          💰 Checkout
        </button>
      </div>
    </div>
  );
}
