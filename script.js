const button = document.getElementById('toggle-mode');
function setDarkMode(isDark) {
  document.body.classList.toggle('dark', isDark);
  if (button) {
    button.textContent = isDark ? 'Modo claro' : 'Modo oscuro';
    button.setAttribute('aria-label', isDark ? 'Activar modo claro' : 'Activar modo oscuro');
    button.setAttribute('aria-pressed', String(isDark));
  }
  try { localStorage.setItem('color-mode', isDark ? 'dark' : 'light'); } catch {}
}
let savedMode = null;
try { savedMode = localStorage.getItem('color-mode'); } catch {}
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
setDarkMode(savedMode === 'dark' || (savedMode === null && prefersDark));
button?.addEventListener('click', () => setDarkMode(!document.body.classList.contains('dark')));
document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
