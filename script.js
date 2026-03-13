// 1. GESTIÓN MODO OSCURO
const toggleButton = document.getElementById('toggle-mode');
const body = document.body;

function applyTheme(dark) {
    if (dark) {
        body.classList.add('dark');
        if (toggleButton) toggleButton.textContent = '☀️';
    } else {
        body.classList.remove('dark');
        if (toggleButton) toggleButton.textContent = '🌓';
    }
}

// Inicializar tema al cargar
let isDark = localStorage.getItem('color-mode') === 'dark' || 
             (localStorage.getItem('color-mode') === null && window.matchMedia('(prefers-color-scheme: dark)').matches);

applyTheme(isDark);

// Evento Clic
if (toggleButton) {
    toggleButton.addEventListener('click', () => {
        isDark = !body.classList.contains('dark');
        applyTheme(isDark);
        localStorage.setItem('color-mode', isDark ? 'dark' : 'light');
    });
}

// 2. CARGA DE POSTS DINÁMICOS
async function loadPosts() {
    const container = document.getElementById('dynamic-posts');
    if (!container) return;

    try {
        const res = await fetch('https://api.github.com/repos/daliosed2/web/contents/blog?ref=codex/crear-p%C3%A1gina-web-personal');
        const files = await res.json();
        
        if (Array.isArray(files)) {
            container.innerHTML = '';
            files.filter(f => f.name.endsWith('.html')).reverse().forEach(file => {
                const card = document.createElement('a');
                card.href = `blog/${file.name}`;
                card.className = 'card';
                card.innerHTML = `🌐 ${file.name.replace('.html', '').replace(/-/g, ' ').toUpperCase()}`;
                container.appendChild(card);
            });
        }
    } catch (e) { console.log("Posts no cargados"); }
}

document.addEventListener('DOMContentLoaded', loadPosts);
