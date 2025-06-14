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

// 🔁 Agregar script de MailerLite al final
(function(w,d,e,u,f,l,n){w[f]=w[f]||function(){(w[f].q=w[f].q||[])
.push(arguments);},l=d.createElement(e),l.async=1,l.src=u,
n=d.getElementsByTagName(e)[0],n.parentNode.insertBefore(l,n);})
(window,document,'script','https://assets.mailerlite.com/js/universal.js','ml');
ml('account', '1493483');
