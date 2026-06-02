(function () {
  function normalize(s) {
    return (s || "").toLowerCase();
  }

  window.aiMemorySearch = function aiMemorySearch(inputId, itemSelector) {
    const input = document.getElementById(inputId);
    if (!input) return;
    const items = Array.from(document.querySelectorAll(itemSelector));

    input.addEventListener("input", function () {
      const q = normalize(input.value);
      items.forEach(function (item) {
        const text = normalize(item.textContent);
        item.style.display = text.includes(q) ? "" : "none";
      });
    });
  };
})();
