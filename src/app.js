// Small helper to wire up lazy preview modals for cards

(function () {
  const modal = document.getElementById("previewModal");
  const frame = document.getElementById("previewFrame");
  if (!modal || !frame) {
    return;
  }

  const openModal = (src) => {
    // Set src lazily to avoid loading heavy pages until requested
    if (frame.getAttribute("src") !== src) {
      frame.setAttribute("src", src);
    }
    modal.classList.add("show");
    modal.setAttribute("aria-hidden", "false");
    // Focus management: move focus to close button for accessibility
    const closeBtn = modal.querySelector("[data-close]");
    closeBtn && closeBtn.focus();
  };

  const closeModal = () => {
    modal.classList.remove("show");
    modal.setAttribute("aria-hidden", "true");
    // Keep iframe loaded to allow quick reopen; clear if you prefer
    // frame.removeAttribute('src');
  };

  // Wire preview buttons
  document.querySelectorAll(".preview-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const src = btn.getAttribute("data-preview-src");
      if (src) {
        openModal(src);
      }
    });
  });

  // Close handlers
  modal.querySelectorAll("[data-close]").forEach((el) => {
    el.addEventListener("click", closeModal);
  });

  // Escape to close
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("show")) {
      closeModal();
    }
  });
})();
