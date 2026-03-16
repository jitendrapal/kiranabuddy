import axios from "axios";

// Base URL — Flask backend (same host in production, proxy in dev)
const BASE = import.meta.env.VITE_API_BASE || "";

const api = axios.create({ baseURL: BASE });

// Products
export const fetchProducts = (phone) =>
  api.get(`/api/stock/products?phone=${encodeURIComponent(phone)}`);
export const fetchProductByBarcode = (barcode, phone) =>
  api.get(
    `/api/product-by-barcode?barcode=${barcode}&phone=${encodeURIComponent(phone)}`,
  );
export const seedDemoProducts = (phone) =>
  api.post("/api/seed-demo-products", { phone });

// Auth  — match actual Flask routes under /api/auth/
export const sendOtp = (phone) => api.post("/api/auth/send-otp", { phone });
export const verifyOtp = (phone, otp, name) =>
  api.post("/api/auth/verify-otp", { phone, otp, name });
export const logout = () => api.post("/api/auth/logout");
export const getSession = () => api.get("/api/auth/check");

// Chat / AI
export const sendChat = (phone, message) =>
  api.post("/api/chat", { phone, message });

// Product return — increases stock, records RETURN transaction
export const processReturn = (phone, items) =>
  api.post("/api/sales/return", { phone, items });

// End of day report
export const fetchEODReport = (phone) =>
  api.get(`/api/reports/eod?phone=${encodeURIComponent(phone)}`);

// Transaction history
export const fetchTransactions = (phone, filter = "all", limit = 200) =>
  api.get(
    `/api/transactions?phone=${encodeURIComponent(phone)}&filter=${filter}&limit=${limit}`,
  );

// Payment / Checkout — deducts stock for each sold item
export const processPayment = (payload) =>
  api.post("/api/sales/record", payload);

// Customer display
export const pushCartToDisplay = (payload) =>
  api.post("/api/customer-display/update", payload);
export const clearDisplay = (phone) =>
  api.post("/api/customer-display/clear", { phone });

// Stock management
export const createProduct = (data) =>
  api.post("/api/stock/create-product", data);

// Add stock to one or more existing products (quantity increase)
// items: [{ product_id, name, quantity, cost_price? }]
export const addStockBill = (phone, items) =>
  api.post("/api/stock/bill", { phone, items });

// Update arbitrary product fields (PATCH by product_id)
export const patchProduct = (product_id, phone, updates) =>
  api.patch(
    `/api/stock/products/${product_id}?phone=${encodeURIComponent(phone)}`,
    updates,
  );
