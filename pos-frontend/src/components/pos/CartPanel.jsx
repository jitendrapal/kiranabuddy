import { useCart } from "../../context/CartContext";
import CartItem from "./CartItem";
import CartSummary from "./CartSummary";

export default function CartPanel({ onCheckout }) {
  const { cart } = useCart();
  const items = cart.filter((i) => i.delta !== 0);

  return (
    <div className="pos-right">
      <div className="pos-cart-header">
        <div className="pos-cart-title">
          🛒 Order Summary
          <span className="cart-badge">
            {items.length} {items.length === 1 ? "item" : "items"}
          </span>
        </div>
        <div className="cart-col-header">
          <span></span>
          <span>ITEM</span>
          <span>PRICE</span>
          <span>QTY</span>
          <span>TOTAL</span>
        </div>
      </div>

      <div className="pos-cart-items">
        {items.length === 0 ? (
          <div className="cart-empty">
            <div>🛒</div>
            <div>Cart is empty</div>
            <small>Click a product or scan a barcode</small>
          </div>
        ) : (
          items.map((item) => <CartItem key={item.code} item={item} />)
        )}
      </div>

      {items.length > 0 && <CartSummary onCheckout={onCheckout} />}
    </div>
  );
}
