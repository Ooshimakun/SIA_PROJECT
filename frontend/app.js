document.getElementById("borrowForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const studentId = document.getElementById("studentId").value;
  const bookId = document.getElementById("bookId").value;
  const responseContainer = document.getElementById("responseContainer");
  const outputLog = document.getElementById("outputLog");

  // Reveal container and set loading state
  responseContainer.classList.remove("hidden");
  outputLog.innerHTML = `<span style="color: var(--text-muted);">[System] Authenticating and communicating with network...</span>`;

  try {
    // Send JSON data to the Borrowing System API
    const response = await fetch("https://borrowing-api.onrender.com/borrow", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        student_id: studentId,
        book_id: bookId,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Network connection failed");
    }

    // --- USER FRIENDLY SUCCESS OUTPUT ---
    // This replaces the raw JSON {} with a clean text readout
    outputLog.innerHTML = `
      <div style="color: var(--success-green); margin-bottom: 8px; font-weight: bold;">✔ Transaction Successful</div>
      <div><strong>Authorized User:</strong> ${studentId}</div>
      <div><strong>Asset ID:</strong> ${bookId}</div>
      <div style="margin-top: 12px; color: var(--text-muted); font-size: 0.85em; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 8px;">
        Status: Inventory synced and transaction logged securely.
      </div>
    `;
  } catch (error) {
    // --- USER FRIENDLY ERROR OUTPUT ---
    outputLog.innerHTML = `
      <div style="color: var(--error-red); margin-bottom: 8px; font-weight: bold;">✖ Transaction Failed</div>
      <div><strong>System Error:</strong> ${error.message}</div>
      <div style="margin-top: 12px; color: var(--text-muted); font-size: 0.85em; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 8px;">
        Please verify asset availability in the catalog before retrying.
      </div>
    `;
  }
});
