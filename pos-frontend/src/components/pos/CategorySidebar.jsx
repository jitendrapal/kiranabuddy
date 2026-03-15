const CATEGORIES = [
  { id: 'all',        icon: '🏪', label: 'All' },
  { id: 'vegetables', icon: '🥦', label: 'Vegetables' },
  { id: 'grocery',    icon: '🌾', label: 'Grocery' },
  { id: 'dairy',      icon: '🥛', label: 'Dairy' },
  { id: 'snacks',     icon: '🍟', label: 'Snacks' },
  { id: 'beverages',  icon: '🧃', label: 'Beverages' },
  { id: 'cleaning',   icon: '🧴', label: 'Cleaning' },
  { id: 'personal',   icon: '🪥', label: 'Personal' },
  { id: 'biscuits',   icon: '🍪', label: 'Biscuits' },
];

export default function CategorySidebar({ active, onSelect }) {
  return (
    <aside className="category-sidebar">
      {CATEGORIES.map((c) => (
        <button
          key={c.id}
          className={`category-item${active === c.id ? ' active' : ''}`}
          onClick={() => onSelect(c.id)}
        >
          <span className="cat-icon">{c.icon}</span>
          <span>{c.label}</span>
        </button>
      ))}
    </aside>
  );
}

