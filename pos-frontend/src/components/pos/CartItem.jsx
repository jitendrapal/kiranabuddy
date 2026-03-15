import { fmt } from "../../utils/currency";
import { useCart } from "../../context/CartContext";

export default function CartItem({ item }) {
  const { dispatch } = useCart();
  const qty = Math.abs(item.delta || 0);
  const total = item.price * qty;
  return (
    <div className="cart-item">
      <div className="cart-item-info">
        <div className="cart-item-name">
          {item.isWeight ? `${item.emoji} ` : ""}
          {item.name}
        </div>
        {item.isWeight ? (
          <div className="cart-item-sub">
            ⚖️ {item.weightKg?.toFixed(3)} kg @ {fmt(item.pricePerKg)}/kg
          </div>
        ) : (
          <div className="cart-item-sub">
            Barcode: {item.displayCode || item.code}
          </div>
        )}
      </div>
      <div className="cart-item-unit">{fmt(item.price)}</div>
      <div className="cart-item-qty">
        {item.isWeight ? (
          <span className="weight-qty">{item.weightKg?.toFixed(2)} kg</span>
        ) : (
          <>
            <button
              onClick={() =>
                dispatch({ type: "ADJUST_QTY", code: item.code, direction: -1 })
              }
            >
              −
            </button>
            <span>{qty}</span>
            <button
              onClick={() =>
                dispatch({ type: "ADJUST_QTY", code: item.code, direction: 1 })
              }
            >
              +
            </button>
          </>
        )}
      </div>
      <div className="cart-item-total">{fmt(total)}</div>
    </div>
  );
}
