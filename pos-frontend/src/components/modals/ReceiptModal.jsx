import { fmt } from "../../utils/currency";
import { useTax } from "../../context/TaxContext";

export default function ReceiptModal({ receipt, onClose }) {
  const { vatConfig } = useTax();
  const {
    items = [],
    rawSubtotal = 0,
    discountAmt = 0,
    taxAmt = 0,
    total = 0,
    paymentMode,
    cashGiven,
    change,
    timestamp,
  } = receipt || {};

  const dateStr = timestamp
    ? new Date(timestamp).toLocaleString("en-GB", {
        day: "2-digit", month: "short", year: "numeric",
        hour: "2-digit", minute: "2-digit",
      })
    : "";

  function handlePrint() {
    window.print();
  }

  return (
    <>
      {/* Overlay — hidden on print */}
      <div className="modal-overlay receipt-overlay" onClick={onClose}>
        <div className="receipt-modal" onClick={(e) => e.stopPropagation()}>

          {/* Actions — hidden on print */}
          <div className="receipt-actions no-print">
            <button className="receipt-btn print" onClick={handlePrint}>🖨️ Print</button>
            <button className="receipt-btn close" onClick={onClose}>✕ Close</button>
          </div>

          {/* ---- PRINTABLE RECEIPT ---- */}
          <div className="receipt-body" id="receipt-print">

            {/* Header */}
            <div className="receipt-header">
              <div className="receipt-shop">🛒 KiranaBuddy</div>
              <div className="receipt-date">{dateStr}</div>
              <div className="receipt-divider">- - - - - - - - - - - - - - -</div>
            </div>

            {/* Items */}
            <table className="receipt-table">
              <thead>
                <tr>
                  <th>Item</th>
                  <th>Qty</th>
                  <th>Price</th>
                  <th>Total</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item, i) => (
                  <tr key={i}>
                    <td>{item.name}</td>
                    <td className="receipt-center">{item.quantity}</td>
                    <td className="receipt-right">{fmt(item.price)}</td>
                    <td className="receipt-right">{fmt(item.price * item.quantity)}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="receipt-divider">- - - - - - - - - - - - - - -</div>

            {/* Totals */}
            <div className="receipt-totals">
              <div className="receipt-row">
                <span>Subtotal</span>
                <span>{fmt(rawSubtotal)}</span>
              </div>
              {discountAmt > 0 && (
                <div className="receipt-row discount">
                  <span>Discount</span>
                  <span>− {fmt(discountAmt)}</span>
                </div>
              )}
              {taxAmt > 0 && (
                <div className="receipt-row">
                  <span>{vatConfig.name} ({vatConfig.rate}%)</span>
                  <span>{fmt(taxAmt)}</span>
                </div>
              )}
              <div className="receipt-row total">
                <span>TOTAL</span>
                <span>{fmt(total)}</span>
              </div>
            </div>

            <div className="receipt-divider">- - - - - - - - - - - - - - -</div>

            {/* Payment info */}
            <div className="receipt-payment">
              <div className="receipt-row">
                <span>Payment</span>
                <span>{paymentMode}</span>
              </div>
              {paymentMode === "Cash" && cashGiven != null && (
                <>
                  <div className="receipt-row">
                    <span>Cash Given</span>
                    <span>{fmt(cashGiven)}</span>
                  </div>
                  <div className="receipt-row change">
                    <span>Change Returned</span>
                    <span>{fmt(change ?? 0)}</span>
                  </div>
                </>
              )}
            </div>

            <div className="receipt-divider">- - - - - - - - - - - - - - -</div>
            <div className="receipt-footer">Thank you for shopping! 🙏</div>
          </div>
        </div>
      </div>
    </>
  );
}

