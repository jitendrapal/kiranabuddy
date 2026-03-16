import { useState } from "react";
import { useCart } from "../../context/CartContext";
import { cartSubtotal } from "../../utils/cartHelpers";
import { fmt } from "../../utils/currency";
import CartItem from "./CartItem";
import CartSummary from "./CartSummary";

export default function CartPanel({ onCheckout }) {
  const { cart, heldBills, dispatch } = useCart();
  const items = cart.filter((i) => i.delta !== 0);
  const [showHeld, setShowHeld] = useState(false);
  const currentTotal = cartSubtotal(cart);

  return (
    <div className="pos-right">
      <div className="pos-cart-header">
        <div className="pos-cart-title">
          🛒 Order Summary
          <span className="cart-badge">
            {items.length} {items.length === 1 ? "item" : "items"}
          </span>
          {heldBills.length > 0 && (
            <button
              className="held-badge"
              onClick={() => setShowHeld((v) => !v)}
              title="View held bills"
            >
              ⏸ {heldBills.length} on hold
            </button>
          )}
        </div>
        <div className="cart-col-header">
          <span></span>
          <span>ITEM</span>
          <span>PRICE</span>
          <span>QTY</span>
          <span>TOTAL</span>
        </div>
      </div>

      {/* Held bills panel */}
      {showHeld && heldBills.length > 0 && (
        <div className="held-bills-panel">
          <div className="held-bills-title">⏸ Held Bills</div>
          {heldBills.map((bill) => (
            <div key={bill.id} className="held-bill-row">
              <div className="held-bill-info">
                <span className="held-bill-time">{bill.heldAt}</span>
                <span className="held-bill-items">
                  {bill.itemCount} item{bill.itemCount !== 1 ? "s" : ""}
                </span>
                <span className="held-bill-total">{fmt(bill.total)}</span>
              </div>
              <div className="held-bill-actions">
                <button
                  className="held-btn recall"
                  onClick={() => {
                    dispatch({
                      type: "RECALL_BILL",
                      id: bill.id,
                      currentTotal,
                    });
                    setShowHeld(false);
                  }}
                >
                  ↩ Recall
                </button>
                <button
                  className="held-btn discard"
                  onClick={() =>
                    dispatch({ type: "DISCARD_HELD", id: bill.id })
                  }
                  title="Discard this held bill"
                >
                  ×
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="pos-cart-items">
        {items.length === 0 ? (
          <div className="cart-empty">
            <div>🛒</div>
            <div>Cart is empty</div>
            <small>
              {heldBills.length > 0
                ? `${heldBills.length} bill${heldBills.length > 1 ? "s" : ""} on hold — click ⏸ above to recall`
                : "Click a product or scan a barcode"}
            </small>
          </div>
        ) : (
          items.map((item) => <CartItem key={item.code} item={item} />)
        )}
      </div>

      {items.length > 0 && <CartSummary onCheckout={onCheckout} />}
    </div>
  );
}
