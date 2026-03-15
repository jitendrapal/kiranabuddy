import os

def w(p, c):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(c)

w('src/components/pos/CartItem.jsx', """
import { fmt } from '../../utils/currency';
import { useCart } from '../../context/CartContext';

export default function CartItem({ item }) {
  const { dispatch } = useCart();
  const qty = Math.abs(item.delta || 0);
  const total = item.price * qty;
  return (
    <div className='cart-item'>
      <div className='cart-item-info'>
        <div className='cart-item-name'>{item.isWeight ? item.emoji + ' ' : ''}{item.name}</div>
        {item.isWeight
          ? <div className='cart-item-sub'>⚖️ {item.weightKg?.toFixed(3)} kg @ {fmt(item.pricePerKg)}/kg</div>
          : <div className='cart-item-sub'>Barcode: {item.displayCode || item.code}</div>}
      </div>
      <div className='cart-item-unit'>{fmt(item.price)}</div>
      <div className='cart-item-qty'>
        {item.isWeight ? (
          <span className='weight-qty'>{item.weightKg?.toFixed(2)} kg</span>
        ) : (
          <>
            <button onClick={() => dispatch({ type: 'ADJUST_QTY', code: item.code, direction: -1 })}>-</button>
            <span>{qty}</span>
            <button onClick={() => dispatch({ type: 'ADJUST_QTY', code: item.code, direction: 1 })}>+</button>
          </>
        )}
      </div>
      <div className='cart-item-total'>{fmt(total)}</div>
    </div>
  );
}
""")

w('src/components/pos/CartSummary.jsx', """
import { fmt } from '../../utils/currency';
import { calcTax } from '../../utils/taxCalculator';
import { useTax } from '../../context/TaxContext';
import { cartSubtotal } from '../../utils/cartHelpers';
import { useCart } from '../../context/CartContext';

export default function CartSummary({ onCheckout }) {
  const { cart } = useCart();
  const { vatConfig } = useTax();
  const raw = cartSubtotal(cart);
  const { subtotal, taxAmt, total } = calcTax(raw, vatConfig);

  return (
    <div className='cart-summary'>
      <div className='summary-row'><span>Subtotal</span><span>{fmt(subtotal)}</span></div>
      <div className='summary-row tax' style={{ color: taxAmt > 0 ? '#f59e0b' : '#64748b' }}>
        <span>{vatConfig.name} ({vatConfig.rate}%)</span>
        <span>{fmt(taxAmt)}</span>
      </div>
      <div className='summary-row total-row'>
        <span>TOTAL</span>
        <span className='total-amount'>{fmt(total)}</span>
      </div>
      <div className='cart-actions'>
        <button className='cart-btn clear' onClick={() => {}}>🗑 Clear</button>
        <button className='cart-btn checkout' onClick={() => onCheckout(total)}>💰 Checkout</button>
      </div>
    </div>
  );
}
""")

w('src/components/pos/CartPanel.jsx', """
import { useCart } from '../../context/CartContext';
import CartItem from './CartItem';
import CartSummary from './CartSummary';

export default function CartPanel({ onCheckout }) {
  const { cart, mode, dispatch } = useCart();
  const items = cart.filter((i) => i.delta !== 0);

  return (
    <div className='pos-right'>
      <div className='pos-cart-header'>
        <div className='pos-cart-title'>
          🛒 Order Summary
          <span className='cart-badge'>{items.length} {items.length === 1 ? 'item' : 'items'}</span>
        </div>
        <div className='mode-btns'>
          <button
            className={'mode-btn' + (mode === 'sale' ? ' active-sale' : '')}
            onClick={() => dispatch({ type: 'SET_MODE', mode: 'sale' })}>
            🛒 Sale Mode
          </button>
          <button
            className={'mode-btn' + (mode === 'add' ? ' active-add' : '')}
            onClick={() => dispatch({ type: 'SET_MODE', mode: 'add' })}>
            📦 Add Stock
          </button>
        </div>
        <div className='cart-col-header'>
          <span>ITEM</span><span>PRICE</span><span>QTY</span><span>TOTAL</span>
        </div>
      </div>

      <div className='pos-cart-items'>
        {items.length === 0 ? (
          <div className='cart-empty'>
            <div>🛒</div>
            <div>Cart is empty</div>
            <small>Click a product or scan a barcode</small>
          </div>
        ) : (
          items.map((item) => <CartItem key={item.code} item={item} />)
        )}
      </div>

      {items.length > 0 && (
        <CartSummary onCheckout={onCheckout} />
      )}
    </div>
  );
}
""")

print('Part 1 done: CartItem, CartSummary, CartPanel')
