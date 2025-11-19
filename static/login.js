// Login page JavaScript
let currentPhone = "";
let otpTimer = null;
let remainingSeconds = 0;

function showMessage(message, type = "info") {
  const messageEl = document.getElementById("message");
  messageEl.textContent = message;
  messageEl.className = `message ${type}`;
  messageEl.style.display = "block";

  // Auto-hide after 5 seconds for success messages
  if (type === "success") {
    setTimeout(() => {
      messageEl.style.display = "none";
    }, 5000);
  }
}

function hideMessage() {
  document.getElementById("message").style.display = "none";
}

function startTimer(seconds) {
  remainingSeconds = seconds;
  const timerEl = document.getElementById("timer");
  const resendBtn = document.getElementById("resend-btn");

  resendBtn.disabled = true;

  if (otpTimer) {
    clearInterval(otpTimer);
  }

  otpTimer = setInterval(() => {
    remainingSeconds--;

    const minutes = Math.floor(remainingSeconds / 60);
    const secs = remainingSeconds % 60;
    timerEl.textContent = `OTP expires in ${minutes}:${secs
      .toString()
      .padStart(2, "0")}`;

    if (remainingSeconds <= 0) {
      clearInterval(otpTimer);
      timerEl.textContent = "OTP expired";
      resendBtn.disabled = false;
    }
  }, 1000);
}

async function sendOTP() {
  hideMessage();

  const phone = document.getElementById("phone").value.trim();

  // Validate phone number
  if (!phone || phone.length !== 10 || !/^\d{10}$/.test(phone)) {
    showMessage("Please enter a valid 10-digit phone number", "error");
    return;
  }

  currentPhone = phone;

  const btn = document.getElementById("send-otp-btn");
  btn.disabled = true;
  btn.textContent = "Sending OTP...";

  try {
    const response = await fetch("/api/auth/send-otp", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ phone }),
    });

    const data = await response.json();

    if (data.success) {
      showMessage(data.message, "success");

      // Show dev OTP if in console mode
      if (data.dev_otp) {
        showMessage(`OTP: ${data.dev_otp} (Development Mode)`, "info");
      }

      // Switch to OTP step
      document.getElementById("phone-step").classList.add("hidden");
      document.getElementById("otp-step").classList.remove("hidden");

      // Start timer
      startTimer(data.expires_in_minutes * 60);

      // Focus on OTP input
      document.getElementById("otp").focus();
    } else {
      showMessage(data.message, "error");
      btn.disabled = false;
      btn.textContent = "Send OTP";
    }
  } catch (error) {
    console.error("Error sending OTP:", error);
    showMessage("Failed to send OTP. Please try again.", "error");
    btn.disabled = false;
    btn.textContent = "Send OTP";
  }
}

async function verifyOTP() {
  hideMessage();

  const otp = document.getElementById("otp").value.trim();
  const name = document.getElementById("name").value.trim();

  // Validate OTP (5 digits for hardcoded OTP)
  if (!otp || otp.length !== 5 || !/^\d{5}$/.test(otp)) {
    showMessage("Please enter a valid 5-digit OTP", "error");
    return;
  }

  const btn = document.getElementById("verify-otp-btn");
  btn.disabled = true;
  btn.textContent = "Verifying...";

  try {
    const response = await fetch("/api/auth/verify-otp", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        phone: currentPhone,
        otp,
        name: name || undefined,
      }),
    });

    const data = await response.json();

    if (data.success) {
      showMessage("Login successful! Redirecting...", "success");

      // Clear timer
      if (otpTimer) {
        clearInterval(otpTimer);
      }

      // Redirect to app
      setTimeout(() => {
        window.location.href = data.redirect_url || "/test";
      }, 1000);
    } else if (data.requires_name) {
      // Show name input for new users
      document.getElementById("name-group").classList.remove("hidden");
      showMessage(data.message, "info");
      btn.disabled = false;
      btn.textContent = "Verify & Login";
      document.getElementById("name").focus();
    } else {
      showMessage(data.message, "error");
      btn.disabled = false;
      btn.textContent = "Verify & Login";
    }
  } catch (error) {
    console.error("Error verifying OTP:", error);
    showMessage("Failed to verify OTP. Please try again.", "error");
    btn.disabled = false;
    btn.textContent = "Verify & Login";
  }
}

async function resendOTP() {
  await sendOTP();
}

// Enter key handlers
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("phone").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendOTP();
    }
  });

  document.getElementById("otp").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      verifyOTP();
    }
  });

  document.getElementById("name").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      verifyOTP();
    }
  });
});
