import { createContext, useContext, useState } from 'react';
import { loadTaxFromStorage, saveTaxToStorage, DEFAULT_TAX } from '../utils/taxCalculator';

const TaxContext = createContext(null);

export function TaxProvider({ children }) {
  const [vatConfig, setVatConfig] = useState(() => loadTaxFromStorage());

  function updateTax(cfg) {
    const next = { ...vatConfig, ...cfg };
    setVatConfig(next);
    saveTaxToStorage(next);
  }

  return (
    <TaxContext.Provider value={{ vatConfig, updateTax }}>
      {children}
    </TaxContext.Provider>
  );
}

export function useTax() {
  const ctx = useContext(TaxContext);
  if (!ctx) throw new Error('useTax must be inside TaxProvider');
  return ctx;
}

