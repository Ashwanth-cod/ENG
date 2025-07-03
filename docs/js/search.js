document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("searchInput");
  const resultsContainer = document.getElementById("resultsContainer");
  let examples = [];

  fetch("assets/code-examples.json")
    .then((res) => res.json())
    .then((data) => {
      examples = data;
      displayResults(examples.slice(0, 5));
    });

  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase();
    const filtered = examples.filter(ex =>
      ex.title.toLowerCase().includes(query) ||
      ex.description.toLowerCase().includes(query) ||
      ex.code.toLowerCase().includes(query)
    );
    displayResults(filtered.slice(0, 5));
  });

  function displayResults(results) {
    resultsContainer.innerHTML = "";

    if (results.length === 0) {
      resultsContainer.innerHTML = "<p>No matching examples found.</p>";
      return;
    }

    results.forEach(({ title, description, code }, index) => {
      const card = document.createElement("div");
      card.className = "example-card";
      const codeId = `code-${index}`;

      card.innerHTML = `
        <h3>${title}</h3>
        <p>${description}</p>
        <pre><code id="${codeId}">${code}</code></pre>
        <button class="copy-btn" data-code-id="${codeId}">📋 Copy</button>
      `;

      resultsContainer.appendChild(card);
    });

    // Attach copy event to all buttons
    document.querySelectorAll(".copy-btn").forEach(button => {
      button.addEventListener("click", () => {
        const codeId = button.getAttribute("data-code-id");
        const code = document.getElementById(codeId).innerText;
        navigator.clipboard.writeText(code).then(() => {
          button.textContent = "✅ Copied!";
          setTimeout(() => {
            button.textContent = "📋 Copy";
          }, 1500);
        });
      });
    });
  }
});
