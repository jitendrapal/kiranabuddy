/** Add or increment a regular (non-weight) item in cart */
export function addRegularItem(cart, code, name, price) {
  const delta = -1; // always sale mode
  const idx = cart.findIndex((i) => i.code === code && !i.isWeight);
  if (idx >= 0) {
    const updated = [...cart];
    updated[idx] = { ...updated[idx], delta: updated[idx].delta + delta };
    if (updated[idx].delta === 0) updated.splice(idx, 1);
    return updated;
  }
  return [
    { code, name, price: parseFloat(price) || 0, delta, isWeight: false },
    ...cart,
  ];
}

/** Add a weight-based item to cart */
export function addWeightItem(
  cart,
  { code, name, pricePerKg, weightKg, emoji },
) {
  const delta = -1; // always sale mode
  const cartKey = `${code}_${Date.now()}`;
  const newItem = {
    code: cartKey,
    displayCode: code,
    name,
    price: parseFloat((pricePerKg * weightKg).toFixed(2)),
    delta,
    isWeight: true,
    weightKg,
    pricePerKg,
    emoji,
  };
  return [newItem, ...cart];
}

/** Adjust quantity of an item by direction (+1 or -1) */
export function adjustQty(cart, code, direction) {
  const idx = cart.findIndex((i) => i.code === code);
  if (idx < 0) return cart;
  const item = cart[idx];
  const sign = item.delta >= 0 ? 1 : -1;
  const newAbs = Math.abs(item.delta) + direction;
  if (newAbs <= 0) return cart.filter((_, i) => i !== idx);
  const updated = [...cart];
  updated[idx] = { ...item, delta: sign * newAbs };
  return updated;
}

/** Calculate subtotal from cart */
export function cartSubtotal(cart) {
  return cart.reduce((sum, item) => {
    const qty = Math.abs(item.delta || 0);
    const price = typeof item.price === "number" ? item.price : 0;
    return sum + price * qty;
  }, 0);
}
