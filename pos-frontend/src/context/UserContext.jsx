import { createContext, useContext, useState, useEffect } from "react";
import { getSession } from "../services/api";

const UserContext = createContext(null);

export function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSession()
      .then((r) => {
        // Flask returns { authenticated: true, user: {...} } or { authenticated: false }
        if (r.data?.authenticated && r.data?.user) {
          setUser(r.data.user);
        } else {
          setUser(null);
        }
      })
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  return (
    <UserContext.Provider value={{ user, setUser, loading }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const ctx = useContext(UserContext);
  if (!ctx) throw new Error("useUser must be inside UserProvider");
  return ctx;
}
