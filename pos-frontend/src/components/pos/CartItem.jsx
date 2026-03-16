import { fmt } from "../../utils/currency";
import { useCart } from "../../context/CartContext";

export default function CartItem({ item }) {
  const { dispatch } = useCart();
  const qty = Math.abs(item.delta || 0);
  const total = item.price * qty;
  const hasStock = item.stock !== null && item.stock !== undefined;
  const atLimit = hasStock && qty >= item.stock;

  return (
    <div className={`cart-item${atLimit ? " cart-item-warn" : ""}`}>
      <button
        className="cart-item-remove"
        onClick={() => dispatch({ type: "REMOVE_ITEM", code: item.code })}
        title="Remove item"
      >
        ×
      </button>
      <div className="cart-item-info">
        <div className="cart-item-name">
          {item.isWeight ? `${item.emoji} ` : ""}
          {item.name}
        </div>
        {item.isWeight ? (
          <div className="cart-item-sub">
            ⚖️ {item.weightKg?.toFixed(3)} kg @ {fmt(item.pricePerKg)}/kg
          </div>
        ) : atLimit ? (
          <div className="cart-item-sub stock-warn">
            ⚠️ Only {item.stock} in stock
          </div>
        ) : (
          <div className="cart-item-sub">{item.displayCode || item.code}</div>
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
              disabled={atLimit}
              title={atLimit ? `Max stock: ${item.stock}` : undefined}
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
