import { useState, useRef, useEffect } from 'react';
import { sendChat } from '../../services/api';
import { useUser } from '../../context/UserContext';

export default function ChatPopup({ onClose }) {
  const { user } = useUser();
  const [messages, setMessages] = useState([
    { role: 'bot', text: '👋 Hi! I am your KiranaBuddy AI assistant. Ask me anything about your stock!' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  async function send() {
    const text = input.trim();
    if (!text) return;
    setMessages((m) => [...m, { role: 'user', text }]);
    setInput('');
    setLoading(true);
    try {
      const res = await sendChat(user?.phone || '', text);
      setMessages((m) => [...m, { role: 'bot', text: res.data?.reply || res.data?.message || '...' }]);
    } catch {
      setMessages((m) => [...m, { role: 'bot', text: '❌ Error connecting to AI.' }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="chat-popup" onClick={(e) => e.stopPropagation()}>
        <div className="chat-header">
          <span>💬 AI Assistant</span>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>
        <div className="chat-messages">
          {messages.map((m, i) => (
            <div key={i} className={`chat-msg ${m.role}`}>{m.text}</div>
          ))}
          {loading && <div className="chat-msg bot">⏳ Thinking...</div>}
          <div ref={bottomRef} />
        </div>
        <div className="chat-input-row">
          <input value={input} onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && send()}
            placeholder="Ask about stock, sales..." />
          <button onClick={send} disabled={loading}>Send</button>
        </div>
      </div>
    </div>
  );
}

