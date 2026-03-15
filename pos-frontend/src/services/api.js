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

// Payment / Checkout
export const processPayment = (payload) =>
  api.post("/api/process-payment", payload);

// Customer display
export const pushCartToDisplay = (payload) =>
  api.post("/api/customer-display/update", payload);
export const clearDisplay = (phone) =>
  api.post("/api/customer-display/clear", { phone });

// Stock management
export const createProduct = (data) =>
  api.post("/api/stock/create-product", data);
export const updateProduct = (data) =>
  api.post("/api/stock/update-product", data);
export const deleteProduct = (data) =>
  api.post("/api/stock/delete-product", data);
