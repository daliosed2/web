const button = document.getElementById('toggle-mode');

function setDarkMode(isDark) {
  document.body.classList.toggle('dark', isDark);
  if (button) {
    button.textContent = isDark ? '☀️' : '🌓';
    button.setAttribute('aria-label', isDark ? 'Activar modo claro' : 'Activar modo oscuro');
  }
  localStorage.setItem('color-mode', isDark ? 'dark' : 'light');
}

const savedMode = localStorage.getItem('color-mode');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
setDarkMode(savedMode === 'dark' || (savedMode === null && prefersDark));

button?.addEventListener('click', () => {
  setDarkMode(!document.body.classList.contains('dark'));
});
