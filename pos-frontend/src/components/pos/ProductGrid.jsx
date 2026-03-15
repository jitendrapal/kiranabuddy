import ProductCard from './ProductCard';
import CategorySidebar from './CategorySidebar';
import { useRef } from 'react';

export default function ProductGrid({ products, loading, category, onCategoryChange, search, onSearchChange, totalCount, barcodeRef, onBarcodeSubmit, onProductClick }) {

  function handleBarcodeKey(e) {
    if (e.key === 'Enter') { onBarcodeSubmit(e.target.value); e.target.value = ''; }
  }

  return (
    <div className="pos-left">
      {/* Search bar */}
      <div className="pos-left-header">
        <div className="pos-search">
          <input
            type="text"
            placeholder="Search products by name or barcode..."
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
          />
        </div>
        <input
          ref={barcodeRef}
          type="text"
          className="barcode-input"
          placeholder="🔫 Barcode..."
          autoComplete="off"
          onKeyDown={handleBarcodeKey}
        />
        <span className="items-count">{products.length} / {totalCount} items</span>
      </div>

      <div className="pos-left-body">
        <CategorySidebar active={category} onSelect={onCategoryChange} />

        <div className="pos-products">
          {loading ? (
            <div className="grid-placeholder">
              <div>📦</div>
              <div>Loading products...</div>
            </div>
          ) : products.length === 0 ? (
            <div className="grid-placeholder">
              <div>📦</div>
              <div>No products found</div>
              <small>Try a different category or search term</small>
            </div>
          ) : (
            <div className="product-grid">
              {products.map((p, i) => (
                <ProductCard key={p.barcode || i} product={p} index={i} onClick={onProductClick} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

