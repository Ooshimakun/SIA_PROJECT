// --- 1. DYNAMICALLY LOAD CATALOG ON PAGE START ---
document.addEventListener("DOMContentLoaded", async () => {
  const catalogList = document.getElementById("catalogList");

  try {
    // Note: Ensure this matches your actual Catalog API URL
    const response = await fetch("https://catalog-api-rkul.onrender.com/books");

    if (!response.ok) throw new Error("Catalog offline");

    const books = await response.json();
    catalogList.innerHTML = ""; // Clear the loading text

    // Loop through live database records and inject them into the HTML
    books.forEach((book) => {
      // Note: If your Supabase columns are named differently (e.g., 'book_title'), update book.title below!
      catalogList.innerHTML += `
        <div class="catalog-item">
          <span class="id">${book.id}</span>
          <span class="title">${book.title}</span>
          <span style="margin-left: auto; font-size: 0.75rem; color: ${book.stock > 0 ? "var(--success-green)" : "var(--error-red)"}">
            Stock: ${book.stock}
          </span>
        </div>
      `;
    });
  } catch (error) {
    catalogList.innerHTML = `<div style="color: var(--error-red); font-size: 0.85rem;">✖ Error connecting to Catalog API.</div>`;
  }
});

// --- 2. EXECUTE REQUEST LOGIC ---
document.getElementById("borrowForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const studentId = document.getElementById("studentId").value;
  const bookId = document.getElementById("bookId").value;
  const responseContainer = document.getElementById("responseContainer");
  const outputLog = document.getElementById("outputLog");

  responseContainer.classList.remove("hidden");
  outputLog.innerHTML = `<span style="color: var(--text-muted);">[System] Authenticating and communicating with network...</span>`;

  try {
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

    outputLog.innerHTML = `
      <div style="color: var(--success-green); margin-bottom: 8px; font-weight: bold;">✔ Transaction Successful</div>
      <div><strong>Authorized User:</strong> ${studentId}</div>
      <div><strong>Asset ID:</strong> ${bookId}</div>
      <div style="margin-top: 12px; color: var(--text-muted); font-size: 0.85em; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 8px;">
        Status: Inventory synced and transaction logged securely.
      </div>
    `;

    // Optional: Refresh the catalog list after a successful borrow so stock drops!
    document.dispatchEvent(new Event("DOMContentLoaded"));
  } catch (error) {
    outputLog.innerHTML = `
      <div style="color: var(--error-red); margin-bottom: 8px; font-weight: bold;">✖ Transaction Failed</div>
      <div><strong>System Error:</strong> ${error.message}</div>
      <div style="margin-top: 12px; color: var(--text-muted); font-size: 0.85em; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 8px;">
        Please verify asset availability in the catalog before retrying.
      </div>
    `;
  }
});
