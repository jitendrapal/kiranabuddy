import { useUser } from '../../context/UserContext';
import { useTax } from '../../context/TaxContext';

export default function StatusBar() {
  const { user } = useUser();
  const { vatConfig } = useTax();

  return (
    <div className="pos-statusbar">
      <div className="statusbar-item"><span className="dot green" /> System Online</div>
      <div className="statusbar-item">🏪 {user?.shop_name || 'Demo Store'}</div>
      <div className="statusbar-item">👤 Cashier: {user?.name || 'Admin'}</div>
      <div className="statusbar-item">
        <span className={`dot ${vatConfig.enabled ? 'amber' : 'green'}`} />
        {vatConfig.enabled ? `${vatConfig.name}: ${vatConfig.rate}% (${vatConfig.type})` : 'Tax: Off'}
      </div>
      <div className="statusbar-item" style={{ marginLeft: 'auto' }}>
        Press <kbd>Enter</kbd> to scan
      </div>
    </div>
  );
}

