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

      // Only use DB products if there are enough real ones (≥5).
      // Fewer than 5 means the shop is likely empty or has only ghost
      // products created by a buggy checkout — fall back to DEMO so
      // the grid is never confusingly empty.
      if (raw.length >= 5) {
        setAll(raw.map(normalise));
      } else {
        // Merge: real DB products first, then fill with DEMO for missing items
        const dbNames = new Set(raw.map((p) => (p.name || "").toLowerCase()));
        const extras = DEMO.filter(
          (d) => !dbNames.has((d.name || "").toLowerCase()),
        );
        setAll([...raw.map(normalise), ...extras.map(normalise)]);
      }
    } catch {
      setAll(DEMO.map(normalise));
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

  return {
    products: filtered,
    totalCount: all.length,
    loading,
    category,
    setCategory,
    search,
    setSearch,
    reload: load,
  };
}

const DEMO = [
  {
    name: "Onion",
    barcode: "VEG-001",
    selling_price: 30,
    current_stock: 50,
    unit: "kg",
  },
  {
    name: "Tomato",
    barcode: "VEG-002",
    selling_price: 25,
    current_stock: 40,
    unit: "kg",
  },
  {
    name: "Potato",
    barcode: "VEG-003",
    selling_price: 22,
    current_stock: 60,
    unit: "kg",
  },
  {
    name: "Garlic",
    barcode: "VEG-004",
    selling_price: 200,
    current_stock: 20,
    unit: "kg",
  },
  {
    name: "Carrot",
    barcode: "VEG-006",
    selling_price: 40,
    current_stock: 35,
    unit: "kg",
  },
  {
    name: "Capsicum",
    barcode: "VEG-007",
    selling_price: 60,
    current_stock: 30,
    unit: "kg",
  },
  {
    name: "Spinach",
    barcode: "VEG-009",
    selling_price: 20,
    current_stock: 15,
    unit: "kg",
  },
  {
    name: "Maggi Noodles",
    barcode: "8901058001329",
    selling_price: 14,
    current_stock: 120,
    unit: "pieces",
  },
  {
    name: "Amul Butter 500g",
    barcode: "8901063028481",
    selling_price: 55,
    current_stock: 60,
    unit: "pieces",
  },
  {
    name: "Tata Salt 1kg",
    barcode: "8901058852017",
    selling_price: 22,
    current_stock: 200,
    unit: "pieces",
  },
  {
    name: "Parle-G Biscuit",
    barcode: "8901820000059",
    selling_price: 10,
    current_stock: 300,
    unit: "pieces",
  },
  {
    name: "Aashirvaad Atta 5kg",
    barcode: "8901725133496",
    selling_price: 280,
    current_stock: 45,
    unit: "pieces",
  },
  {
    name: "Surf Excel 1kg",
    barcode: "8901030827372",
    selling_price: 190,
    current_stock: 80,
    unit: "pieces",
  },
  {
    name: "Amul Milk 1L",
    barcode: "8901063013739",
    selling_price: 60,
    current_stock: 150,
    unit: "pieces",
  },
  {
    name: "Lifebuoy Soap",
    barcode: "8901030728931",
    selling_price: 35,
    current_stock: 90,
    unit: "pieces",
  },
  {
    name: "Colgate 200g",
    barcode: "8901030038591",
    selling_price: 89,
    current_stock: 70,
    unit: "pieces",
  },
  {
    name: "Dettol Handwash",
    barcode: "6290255052136",
    selling_price: 115,
    current_stock: 55,
    unit: "pieces",
  },
  {
    name: "Bru Coffee 100g",
    barcode: "8901030784576",
    selling_price: 199,
    current_stock: 40,
    unit: "pieces",
  },
  {
    name: "Good Day Biscuit",
    barcode: "8901820007812",
    selling_price: 30,
    current_stock: 180,
    unit: "pieces",
  },
  {
    name: "Haldiram Mixture",
    barcode: "8906002960019",
    selling_price: 50,
    current_stock: 95,
    unit: "pieces",
  },
  {
    name: "Lays Chips",
    barcode: "8901491502606",
    selling_price: 20,
    current_stock: 200,
    unit: "pieces",
  },
  {
    name: "Dairy Milk 40g",
    barcode: "8901233051400",
    selling_price: 40,
    current_stock: 110,
    unit: "pieces",
  },
  {
    name: "Tata Tea Gold 250g",
    barcode: "8901058003279",
    selling_price: 165,
    current_stock: 60,
    unit: "pieces",
  },
  {
    name: "Frooti Mango 200ml",
    barcode: "8906022302888",
    selling_price: 15,
    current_stock: 250,
    unit: "pieces",
  },
];
