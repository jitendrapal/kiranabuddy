import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { sendOtp, verifyOtp } from "../services/api";
import { useUser } from "../context/UserContext";

// steps: 'phone' → 'otp' → 'name' (new users only)
export default function LoginPage() {
  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState("");
  const [name, setName] = useState("");
  const [step, setStep] = useState("phone");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const { setUser } = useUser();
  const navigate = useNavigate();

  function clearError() {
    setError("");
  }

  async function handleSendOtp() {
    if (!phone.trim()) {
      setError("Please enter your phone number");
      return;
    }
    setLoading(true);
    clearError();
    try {
      await sendOtp(phone.trim());
      setStep("otp");
    } catch (e) {
      setError(
        e.response?.data?.message || "Failed to send OTP. Is Flask running?",
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleVerifyOtp() {
    if (!otp.trim()) {
      setError("Please enter the OTP");
      return;
    }
    setLoading(true);
    clearError();
    try {
      const res = await verifyOtp(phone.trim(), otp.trim(), "");
      if (res.data?.success) {
        setUser(res.data.user);
        navigate("/pos");
      } else {
        setError(res.data?.message || "Invalid OTP");
      }
    } catch (e) {
      // Flask returns 400 for requires_name — handle it as a valid step, not an error
      if (e.response?.data?.requires_name) {
        setStep("name");
      } else {
        setError(e.response?.data?.message || "Invalid OTP");
      }
    } finally {
      setLoading(false);
    }
  }

  async function handleNameSubmit() {
    if (!name.trim()) {
      setError("Please enter your name");
      return;
    }
    setLoading(true);
    clearError();
    try {
      const res = await verifyOtp(phone.trim(), otp.trim(), name.trim());
      if (res.data?.success) {
        setUser(res.data.user);
        navigate("/pos");
      } else {
        setError(res.data?.message || "Registration failed");
      }
    } catch (e) {
      setError(e.response?.data?.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-logo">🛒</div>
        <h1 className="login-title">KiranaBuddy POS</h1>
        <p className="login-subtitle">Point of Sale System</p>

        {error && <div className="login-error">{error}</div>}

        {step === "phone" && (
          <>
            <div className="login-field">
              <label>Phone Number</label>
              <input
                type="tel"
                placeholder="+91 98765 43210"
                value={phone}
                onChange={(e) => {
                  setPhone(e.target.value);
                  clearError();
                }}
                onKeyDown={(e) => e.key === "Enter" && handleSendOtp()}
                autoFocus
              />
            </div>
            <button
              className="login-btn"
              onClick={handleSendOtp}
              disabled={loading}
            >
              {loading ? "⏳ Sending OTP..." : "📱 Send OTP"}
            </button>
          </>
        )}

        {step === "otp" && (
          <>
            <div className="login-field">
              <label>OTP sent to {phone}</label>
              <input
                type="text"
                inputMode="numeric"
                placeholder="Enter 6-digit OTP"
                value={otp}
                onChange={(e) => {
                  setOtp(e.target.value);
                  clearError();
                }}
                onKeyDown={(e) => e.key === "Enter" && handleVerifyOtp()}
                autoFocus
                maxLength={6}
              />
            </div>
            <button
              className="login-btn"
              onClick={handleVerifyOtp}
              disabled={loading}
            >
              {loading ? "⏳ Verifying..." : "✅ Verify OTP"}
            </button>
            <button
              className="login-back"
              onClick={() => {
                setStep("phone");
                setOtp("");
                clearError();
              }}
            >
              ← Change number
            </button>
          </>
        )}

        {step === "name" && (
          <>
            <p style={{ fontSize: 13, color: "#64748b", marginBottom: 16 }}>
              👋 Welcome! You're new here. Enter your name to set up your shop.
            </p>
            <div className="login-field">
              <label>Your Name</label>
              <input
                type="text"
                placeholder="e.g. Ramesh Kumar"
                value={name}
                onChange={(e) => {
                  setName(e.target.value);
                  clearError();
                }}
                onKeyDown={(e) => e.key === "Enter" && handleNameSubmit()}
                autoFocus
              />
            </div>
            <button
              className="login-btn"
              onClick={handleNameSubmit}
              disabled={loading}
            >
              {loading ? "⏳ Creating shop..." : "🚀 Create My Shop"}
            </button>
          </>
        )}
      </div>
    </div>
  );
}
