import { createContext, useContext, useState } from "react";

export const CURRENCIES = [
  { symbol: "₹", code: "INR", name: "Indian Rupee",        flag: "🇮🇳" },
  { symbol: "$", code: "USD", name: "US Dollar",           flag: "🇺🇸" },
  { symbol: "€", code: "EUR", name: "Euro",                flag: "🇪🇺" },
  { symbol: "£", code: "GBP", name: "British Pound",       flag: "🇬🇧" },
  { symbol: "¥", code: "JPY", name: "Japanese Yen",        flag: "🇯🇵" },
  { symbol: "د.إ", code: "AED", name: "UAE Dirham",        flag: "🇦🇪" },
  { symbol: "﷼", code: "SAR", name: "Saudi Riyal",         flag: "🇸🇦" },
  { symbol: "৳", code: "BDT", name: "Bangladeshi Taka",    flag: "🇧🇩" },
  { symbol: "₨", code: "PKR", name: "Pakistani Rupee",     flag: "🇵🇰" },
  { symbol: "RM", code: "MYR", name: "Malaysian Ringgit",  flag: "🇲🇾" },
  { symbol: "₱", code: "PHP", name: "Philippine Peso",     flag: "🇵🇭" },
  { symbol: "₺", code: "TRY", name: "Turkish Lira",        flag: "🇹🇷" },
];

function load() {
  try {
    const sym = localStorage.getItem("posCurrencySymbol") || "₹";
    return CURRENCIES.find((c) => c.symbol === sym) || CURRENCIES[0];
  } catch {
    return CURRENCIES[0];
  }
}

const CurrencyContext = createContext(null);

export function CurrencyProvider({ children }) {
  const [currency, setCurrency] = useState(load);

  function updateCurrency(curr) {
    setCurrency(curr);
    try { localStorage.setItem("posCurrencySymbol", curr.symbol); } catch {}
  }

  return (
    <CurrencyContext.Provider value={{ currency, updateCurrency }}>
      {children}
    </CurrencyContext.Provider>
  );
}

export function useCurrency() {
  const ctx = useContext(CurrencyContext);
  if (!ctx) throw new Error("useCurrency must be inside CurrencyProvider");
  return ctx;
}

