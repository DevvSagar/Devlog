// Error message extraction from API responses
export function getErrorMessage(error) {
  if (typeof error.detail === "string") {
    return error.detail;
  } else if (Array.isArray(error.detail)) {
    return error.detail.map((err) => err.msg).join(". ");
  }
  return "An error occurred. Please try again.";
}

// Show a Bootstrap modal by ID
export function showModal(modalId) {
  const modal = bootstrap.Modal.getOrCreateInstance(
    document.getElementById(modalId),
  );
  modal.show();
  return modal;
}

// Hide a Bootstrap modal by ID
export function hideModal(modalId) {
  const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
  if (modal) modal.hide();
}

// Format UTC dates to the user's local timezone
export function formatLocalDates() {
  document.querySelectorAll("time.post-date[datetime]").forEach((el) => {
    const utcString = el.getAttribute("datetime");
    if (!utcString) return;
    const iso = utcString.endsWith("Z") || utcString.includes("+") ? utcString : utcString + "Z";
    const date = new Date(iso);
    if (!isNaN(date.getTime())) {
      el.textContent = date.toLocaleDateString(undefined, {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    }
  });
}

// Auto-run on page load
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", formatLocalDates);
} else {
  formatLocalDates();
}