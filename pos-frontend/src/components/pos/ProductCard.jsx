import { fmt } from "../../utils/currency";

const BG_COLORS = [
  "#fef9c3",
  "#eff6ff",
  "#f0fdf4",
  "#fdf4ff",
  "#fff7ed",
  "#ecfdf5",
  "#fef3c7",
  "#fef2f2",
  "#fefce8",
  "#fffbeb",
];

function StockBadge({ stock }) {
  if (stock === null || stock === undefined) return null;
  if (stock <= 0) return <span className="stock-badge out">Out</span>;
  if (stock <= 5) return <span className="stock-badge low">Low: {stock}</span>;
  return <span className="stock-badge ok">✓ {stock}</span>;
}

export default function ProductCard({ product, index, onClick }) {
  const { name, price, stock, emoji, isWeight } = product;
  const bg = product.color || BG_COLORS[index % BG_COLORS.length];
  const outOfStock = stock !== null && stock !== undefined && stock <= 0;

  return (
    <div
      className={`product-card${outOfStock ? " out-of-stock" : ""}`}
      onClick={() => !outOfStock && onClick(product)}
      title={
        outOfStock
          ? `${name} — Out of stock`
          : isWeight
            ? `${name} — ${fmt(price)}/kg · tap to enter weight`
            : `${name} — ${fmt(price)} · Stock: ${stock ?? "N/A"}`
      }
    >
      <StockBadge stock={stock} />
      <div className="product-card-img" style={{ background: bg }}>
        {emoji}
      </div>
      <div className="product-card-body">
        <div className="product-name">{name}</div>
        <div className="product-price">
          {fmt(price)}
          {isWeight ? "/kg" : ""}
        </div>
      </div>
      {isWeight && <div className="weight-badge">⚖️ per kg</div>}
    </div>
  );
}
