import { createContext, useContext, useReducer } from 'react';
import { addRegularItem, addWeightItem, adjustQty } from '../utils/cartHelpers';

const CartContext = createContext(null);

const initialState = { cart: [], mode: 'sale' }; // mode: 'sale' | 'add'

function cartReducer(state, action) {
  switch (action.type) {
    case 'ADD_REGULAR':
      return { ...state, cart: addRegularItem(state.cart, action.code, action.name, action.price, state.mode) };
    case 'ADD_WEIGHT':
      return { ...state, cart: addWeightItem(state.cart, { ...action.payload, mode: state.mode }) };
    case 'ADJUST_QTY':
      return { ...state, cart: adjustQty(state.cart, action.code, action.direction) };
    case 'CLEAR':
      return { ...state, cart: [] };
    case 'SET_MODE':
      return { ...state, mode: action.mode };
    default:
      return state;
  }
}

export function CartProvider({ children }) {
  const [state, dispatch] = useReducer(cartReducer, initialState);
  return <CartContext.Provider value={{ ...state, dispatch }}>{children}</CartContext.Provider>;
}

export function useCart() {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error('useCart must be used inside CartProvider');
  return ctx;
}

