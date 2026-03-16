import { useState, useEffect, useCallback } from "react";
import { fetchProducts } from "../services/api";
import { getProductEmoji } from "../utils/emojiMap";

const CATEGORY_MAP = {
  vegetables: [
    "onion",
    "tomato",
    "potato",
    "garlic",
    "ginger",
    "carrot",
    "capsicum",
    "spinach",
    "palak",
    "cauliflower",
    "gobi",
    "brinjal",
    "baingan",
    "okra",
    "ladyfinger",
    "bhindi",
    "peas",
    "matar",
    "cucumber",
    "kakdi",
    "radish",
    "mooli",
    "coriander",
    "dhania",
    "lemon",
    "nimbu",
    "chilli",
    "mirch",
    "pumpkin",
  ],
  grocery: [
    "maggi",
    "atta",
    "salt",
    "oil",
    "rice",
    "tata",
    "aashirvaad",
    "saffola",
    "rin",
    "detergent",
    "wheat",
    "dal",
  ],
  dairy: ["milk", "amul", "butter", "ghee", "paneer", "curd", "dahi"],
  snacks: ["lays", "chips", "haldiram", "mixture", "namkeen", "kurkure"],
  beverages: ["frooti", "juice", "bru", "coffee", "tea", "drink", "mango"],
  cleaning: ["surf", "vim", "dettol", "handwash", "phenyl", "harpic", "lizol"],
  personal: [
    "colgate",
    "toothpaste",
    "lifebuoy",
    "soap",
    "vaseline",
    "lotion",
    "shampoo",
  ],
  biscuits: [
    "parle",
    "good day",
    "oreo",
    "marie",
    "britannia",
    "sunfeast",
    "bourbon",
  ],
};

function normalise(p) {
  return {
    ...p,
    price: parseFloat(p.selling_price ?? p.price ?? p.mrp ?? 0),
    stock: p.current_stock ?? p.stock ?? p.quantity ?? null,
    barcode: p.barcode || p.code || p.product_id || p.name,
    emoji: p.emoji || getProductEmoji(p.name, p.unit),
    isWeight: !!(p.per_kg || p.is_weight || p.unit === "kg"),
  };
}

export function useProducts(phone) {
  const [all, setAll] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [category, setCategory] = useState("all");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    if (!phone) return;
    setLoading(true);
    try {
      const res = await fetchProducts(phone);
      const raw = res.data?.products || res.data || [];
      setAll(raw.map(normalise));
    } catch {
      setAll([]);
    } finally {
      setLoading(false);
    }
  }, [phone]);

  useEffect(() => {
    load();
  }, [load]);

  useEffect(() => {
    const q = search.toLowerCase();
    let result = all;
    if (category !== "all") {
      const kws = CATEGORY_MAP[category] || [];
      result = result.filter((p) =>
        kws.some((k) => p.name?.toLowerCase().includes(k)),
      );
    }
    if (q)
      result = result.filter(
        (p) =>
          p.name?.toLowerCase().includes(q) ||
          p.barcode?.toLowerCase().includes(q),
      );
    setFiltered(result);
  }, [all, category, search]);

  // Immediately reduce stock in local state for sold items.
  // Called right after a successful payment so the UI updates instantly,
  // even for DEMO products that aren't stored in Firestore.
  function applyStockReductions(soldItems) {
    setAll((prev) =>
      prev.map((p) => {
        const sold = soldItems.find(
          (s) =>
            (s.name || "").toLowerCase() === (p.name || "").toLowerCase() ||
            (s.barcode && s.barcode === p.barcode),
        );
        if (!sold) return p;
        const qty = parseFloat(sold.quantity) || 0;
        const currentStock = parseFloat(p.stock ?? p.current_stock ?? 0);
        return { ...p, stock: Math.max(0, currentStock - qty) };
      }),
    );
  }

  return {
    products: filtered,
    totalCount: all.length,
    loading,
    category,
    setCategory,
    search,
    setSearch,
    reload: load,
    applyStockReductions,
  };
}
