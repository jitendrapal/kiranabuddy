import { createContext, useContext, useReducer } from "react";
import { addRegularItem, addWeightItem, adjustQty } from "../utils/cartHelpers";

const CartContext = createContext(null);

const initialState = { cart: [], heldBills: [] };

function cartReducer(state, action) {
  switch (action.type) {
    case "ADD_REGULAR":
      return {
        ...state,
        cart: addRegularItem(
          state.cart,
          action.code,
          action.name,
          action.price,
          action.stock,
        ),
      };
    case "ADD_WEIGHT":
      return { ...state, cart: addWeightItem(state.cart, action.payload) };
    case "ADJUST_QTY":
      return {
        ...state,
        cart: adjustQty(state.cart, action.code, action.direction),
      };
    case "REMOVE_ITEM":
      return {
        ...state,
        cart: state.cart.filter((i) => i.code !== action.code),
      };
    case "CLEAR":
      return { ...state, cart: [] };
    case "HOLD_BILL": {
      if (state.cart.length === 0) return state;
      const held = {
        id: Date.now().toString(),
        items: state.cart,
        heldAt: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
        itemCount: state.cart.filter((i) => i.delta !== 0).length,
        total: action.total,
      };
      return { cart: [], heldBills: [held, ...state.heldBills] };
    }
    case "RECALL_BILL": {
      const bill = state.heldBills.find((b) => b.id === action.id);
      if (!bill) return state;
      // If current cart has items, push it back to held first
      const remaining = state.heldBills.filter((b) => b.id !== action.id);
      if (state.cart.length > 0) {
        const reHeld = {
          id: Date.now().toString(),
          items: state.cart,
          heldAt: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
          itemCount: state.cart.filter((i) => i.delta !== 0).length,
          total: action.currentTotal,
        };
        return { cart: bill.items, heldBills: [reHeld, ...remaining] };
      }
      return { cart: bill.items, heldBills: remaining };
    }
    case "DISCARD_HELD": {
      return {
        ...state,
        heldBills: state.heldBills.filter((b) => b.id !== action.id),
      };
    }
    default:
      return state;
  }
}

export function CartProvider({ children }) {
  const [state, dispatch] = useReducer(cartReducer, initialState);
  return (
    <CartContext.Provider value={{ ...state, dispatch }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error("useCart must be used inside CartProvider");
  return ctx;
}
