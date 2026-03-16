// Reads the symbol that CurrencyContext writes to localStorage.
// All components using fmt() automatically pick up the new symbol on next render.
export function getCurrencySymbol() {
  try {
    return localStorage.getItem("posCurrencySymbol") || "₹";
  } catch {
    return "₹";
  }
}

export const CURRENCY = "₹"; // kept for backward compat
export const fmt = (v) => `${getCurrencySymbol()} ${Number(v).toFixed(2)}`;

export function generateBillNumber() {
  const d = new Date();
  const dd = String(d.getDate()).padStart(2, "0");
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const seq = String(Math.floor(Math.random() * 900) + 100);
  return `KB-${dd}${mm}-${seq}`;
}
