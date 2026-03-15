
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
