export function calcTax(subtotal, vatConfig) {
  const { enabled, rate, type } = vatConfig;
  if (!enabled || !rate) return { subtotal, taxAmt: 0, total: subtotal };
  const r = rate / 100;
  if (type === 'inclusive') {
    const taxAmt = subtotal - subtotal / (1 + r);
    return { subtotal: subtotal - taxAmt, taxAmt, total: subtotal };
  }
  const taxAmt = subtotal * r;
  return { subtotal, taxAmt, total: subtotal + taxAmt };
}

export const DEFAULT_TAX = { enabled: false, rate: 0, name: 'VAT', type: 'exclusive' };

export function loadTaxFromStorage() {
  try {
    const saved = localStorage.getItem('posVatConfig');
    return saved ? { ...DEFAULT_TAX, ...JSON.parse(saved) } : DEFAULT_TAX;
  } catch { return DEFAULT_TAX; }
}

export function saveTaxToStorage(cfg) {
  localStorage.setItem('posVatConfig', JSON.stringify(cfg));
}

