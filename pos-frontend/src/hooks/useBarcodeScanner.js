import { useEffect, useRef } from "react";

/**
 * Global barcode scanner listener.
 *
 * USB barcode scanners behave like keyboards: they type each character of the
 * barcode very quickly (< 50 ms apart) then send an Enter key.
 * A human typist has much longer gaps between keystrokes (> 100 ms).
 *
 * Strategy:
 *   - Accumulate characters in a buffer.
 *   - Reset the buffer if > TIMEOUT ms pass between keystrokes.
 *   - On Enter, if the buffer has at least MIN_LENGTH chars, call onScan().
 *   - Skip when the active element is an <input>, <textarea>, or contentEditable
 *     so normal typing is never intercepted.
 *
 * @param {(code: string) => void} onScan  - called with the scanned barcode string
 * @param {{ disabled?: boolean }}  opts   - set disabled=true when a modal is open
 */
export function useBarcodeScanner(onScan, { disabled = false } = {}) {
  const bufferRef    = useRef("");
  const lastKeyRef   = useRef(Date.now());
  const timerRef     = useRef(null);
  const onScanRef    = useRef(onScan);

  // Keep callback ref fresh without re-registering the listener
  useEffect(() => { onScanRef.current = onScan; }, [onScan]);

  useEffect(() => {
    const TIMEOUT    = 80;   // ms — gap longer than this = human typing
    const MIN_LENGTH = 3;    // ignore single-char or 2-char "scans"

    function handleKeyDown(e) {
      if (disabled) return;

      // Ignore when user is typing inside any focusable element
      const tag = document.activeElement?.tagName ?? "";
      if (
        tag === "INPUT" ||
        tag === "TEXTAREA" ||
        tag === "SELECT" ||
        document.activeElement?.isContentEditable
      ) return;

      // Modifier keys pressed alone — ignore
      if (e.ctrlKey || e.altKey || e.metaKey) return;

      const now = Date.now();
      const gap = now - lastKeyRef.current;
      lastKeyRef.current = now;

      // Long gap since last keystroke → this is a new, human-initiated sequence
      // Reset buffer so we don't accidentally merge two unrelated key presses
      if (gap > TIMEOUT && bufferRef.current.length > 0) {
        bufferRef.current = "";
      }

      if (e.key === "Enter") {
        clearTimeout(timerRef.current);
        const code = bufferRef.current.trim();
        bufferRef.current = "";
        if (code.length >= MIN_LENGTH) {
          e.preventDefault(); // don't submit any focused form
          onScanRef.current(code);
        }
        return;
      }

      // Only accumulate printable single characters
      if (e.key.length !== 1) return;

      bufferRef.current += e.key;

      // Safety timeout: clear buffer if Enter never comes (e.g. partial scan)
      clearTimeout(timerRef.current);
      timerRef.current = setTimeout(() => {
        bufferRef.current = "";
      }, 500);
    }

    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      clearTimeout(timerRef.current);
    };
  }, [disabled]); // only re-run when disabled changes
}

