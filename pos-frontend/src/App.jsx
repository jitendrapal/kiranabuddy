import { HashRouter, Routes, Route, Navigate } from "react-router-dom";
import { UserProvider, useUser } from "./context/UserContext";
import { CartProvider } from "./context/CartContext";
import { TaxProvider } from "./context/TaxContext";
import { CurrencyProvider } from "./context/CurrencyContext";
import POSPage from "./pages/POSPage";
import StockPage from "./pages/StockPage";
import TransactionsPage from "./pages/TransactionsPage";
import LoginPage from "./pages/LoginPage";

function ProtectedRoute({ children }) {
  const { user, loading } = useUser();
  if (loading) return <div className="loading-screen">⏳ Loading...</div>;
  return user ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <HashRouter>
      <UserProvider>
        <CurrencyProvider>
          <TaxProvider>
            <CartProvider>
              <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route
                  path="/pos"
                  element={
                    <ProtectedRoute>
                      <POSPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/stock"
                  element={
                    <ProtectedRoute>
                      <StockPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/transactions"
                  element={
                    <ProtectedRoute>
                      <TransactionsPage />
                    </ProtectedRoute>
                  }
                />
                <Route path="*" element={<Navigate to="/pos" replace />} />
              </Routes>
            </CartProvider>
          </TaxProvider>
        </CurrencyProvider>
      </UserProvider>
    </HashRouter>
  );
}
