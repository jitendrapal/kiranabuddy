export const CURRENCY = "₹";
export const fmt = (v) => `${CURRENCY} ${Number(v).toFixed(2)}`;

export function generateBillNumber() {
  const d = new Date();
  const dd = String(d.getDate()).padStart(2, "0");
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const seq = String(Math.floor(Math.random() * 900) + 100);
  return `KB-${dd}${mm}-${seq}`;
}
