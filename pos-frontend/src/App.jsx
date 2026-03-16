import { HashRouter, Routes, Route, Navigate } from "react-router-dom";
import { UserProvider, useUser } from "./context/UserContext";
import { CartProvider } from "./context/CartContext";
import { TaxProvider } from "./context/TaxContext";
import POSPage from "./pages/POSPage";
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
              <Route path="*" element={<Navigate to="/pos" replace />} />
            </Routes>
          </CartProvider>
        </TaxProvider>
      </UserProvider>
    </HashRouter>
  );
}
