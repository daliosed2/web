const toggleButton = document.getElementById('toggle-mode');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const savedMode = localStorage.getItem('color-mode');

function applyMode(dark) {
  if (dark) {
    document.body.classList.add('dark');
    toggleButton.textContent = '☀️';

document.querySelectorAll('.toggle-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const list = btn.nextElementSibling;
    if (list) {
      list.classList.toggle('open');
    }
  });
});
    toggleButton.setAttribute('aria-label', 'Activar modo claro');
  } else {
    document.body.classList.remove('dark');
    toggleButton.textContent = '🌓';
    toggleButton.setAttribute('aria-label', 'Activar modo oscuro');
  }
}

// initialize
let useDark = savedMode === 'dark' || (savedMode === null && prefersDark);
applyMode(useDark);

// toggle on click
if (toggleButton) {
  toggleButton.addEventListener('click', () => {
    useDark = !useDark;
    localStorage.setItem('color-mode', useDark ? 'dark' : 'light');
    applyMode(useDark);
  });
}
