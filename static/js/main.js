/**
 * JobNest — Main JavaScript
 * Handles progressive enhancement, flash dismissal, and minor UX polish.
 */

document.addEventListener('DOMContentLoaded', () => {

  // ── Auto-dismiss flash messages after 5 seconds ──────────────────────
  document.querySelectorAll('.flash').forEach(flash => {
    setTimeout(() => {
      flash.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      flash.style.opacity = '0';
      flash.style.transform = 'translateY(-8px)';
      setTimeout(() => flash.remove(), 400);
    }, 5000);
  });

  // ── Animate score bars on page load ──────────────────────────────────
  // The .bar > span widths are already set inline; CSS transition handles animation.
  // We just trigger a re-paint by reading offsetWidth.
  document.querySelectorAll('.bar span').forEach(bar => {
    const w = bar.style.width;
    bar.style.width = '0';
    requestAnimationFrame(() => {
      requestAnimationFrame(() => { bar.style.width = w; });
    });
  });

  // ── Confirm delete forms ──────────────────────────────────────────────
  // Already handled via inline onsubmit; nothing extra needed.

  // ── Active nav link highlighting ──────────────────────────────────────
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') && path.startsWith(link.getAttribute('href')) && link.getAttribute('href') !== '/') {
      link.style.color = 'var(--accent)';
    }
  });

  // ── File input label update (upload page) ────────────────────────────
  const fileInput = document.getElementById('resume_file');
  const fileName  = document.getElementById('file-name');
  if (fileInput && fileName) {
    fileInput.addEventListener('change', () => {
      if (fileInput.files.length) {
        fileName.textContent = fileInput.files[0].name;
      }
    });
  }

  // ── Role radio UI toggle (register page) ─────────────────────────────
  // Handled inline in register.html for simplicity.

});
