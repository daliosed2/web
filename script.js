const toggleButton = document.getElementById('toggle-mode');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const savedMode = localStorage.getItem('color-mode');

function applyMode(dark) {
  if (dark) {
    document.body.classList.add('dark');
    toggleButton.textContent = '☀️';
    toggleButton.setAttribute('aria-label', 'Activar modo claro');
  } else {
    document.body.classList.remove('dark');
    toggleButton.textContent = '🌓';
    toggleButton.setAttribute('aria-label', 'Activar modo oscuro');
  }
}

let useDark = savedMode === 'dark' || (savedMode === null && prefersDark);
applyMode(useDark);

if (toggleButton) {
  toggleButton.addEventListener('click', () => {
    useDark = !useDark;
    localStorage.setItem('color-mode', useDark ? 'dark' : 'light');
    applyMode(useDark);
  });
}

async function loadDynamicPosts() {
    const container = document.getElementById('dynamic-posts');
    if (!container) return;

    const url = 'https://api.github.com/repos/daliosed2/web/contents/blog?ref=codex/crear-p%C3%A1gina-web-personal';

    try {
        const response = await fetch(url);
        const files = await response.json();

        if (Array.isArray(files)) {
            container.innerHTML = ''; 
            const htmlFiles = files.filter(f => f.name.endsWith('.html')).reverse();

            if (htmlFiles.length === 0) {
                container.innerHTML = '<p>🤖 No hay artículos automáticos aún.</p>';
                return;
            }

            htmlFiles.forEach(file => {
                const card = document.createElement('a');
                card.href = `blog/${file.name}`;
                card.className = 'card';
                card.target = '_blank';
                
                // Formateamos el nombre del archivo para mostrarlo como título
                // Ejemplo: openai-lanza-sora -> OPENAI LANZA SORA
                const displayTitle = file.name.replace('.html', '').replace(/-/g, ' ').toUpperCase();
                card.innerHTML = `🤖 ${displayTitle}`;
                
                container.appendChild(card);
            });
        }
    } catch (error) {
        container.innerHTML = '<p>🤖 El bot está preparando el análisis de hoy...</p>';
    }
}

document.addEventListener('DOMContentLoaded', loadDynamicPosts);
