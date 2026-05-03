document.getElementById("borrowForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const studentId = document.getElementById("studentId").value;
  const bookId = document.getElementById("bookId").value;
  const responseContainer = document.getElementById("responseContainer");
  const outputLog = document.getElementById("outputLog");

  // Reveal container and set loading state
  responseContainer.classList.remove("hidden");
  outputLog.textContent = "Authenticating and communicating with systems...";
  outputLog.style.color = "#4a5568";

  try {
    // Send JSON data to the Borrowing System API
    const response = await fetch("https://borrowing-api.onrender.com", {
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
      throw new Error(data.error || "Enterprise workflow failed.");
    }

    // On success, print the JSON output
    outputLog.textContent = JSON.stringify(data, null, 2);
    outputLog.style.color = "#2f855a"; // Green for success
  } catch (error) {
    // On failure (e.g., out of stock), print the error
    outputLog.textContent = `Integration Error: ${error.message}`;
    outputLog.style.color = "#c53030"; // Red for error
  }
});
