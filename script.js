// --- 1. MODO OSCURO ---
const btn = document.getElementById('toggle-mode');

function setDarkMode(isDark) {
    if (isDark) {
        document.body.classList.add('dark');
        if (btn) btn.textContent = '☀️';
        localStorage.setItem('color-mode', 'dark');
    } else {
        document.body.classList.remove('dark');
        if (btn) btn.textContent = '🌓';
        localStorage.setItem('color-mode', 'light');
    }
}

// Cargar preferencia inicial
const saved = localStorage.getItem('color-mode');
const prefers = window.matchMedia('(prefers-color-scheme: dark)').matches;
setDarkMode(saved === 'dark' || (saved === null && prefers));

// Escuchar clic
if (btn) {
    btn.onclick = () => {
        const currentlyDark = document.body.classList.contains('dark');
        setDarkMode(!currentlyDark);
    };
}

// --- 2. CARGA DE NOTICIAS ---
const dynamicContainer = document.getElementById('dynamic-posts');
if (dynamicContainer) {
    fetch('https://api.github.com/repos/daliosed2/web/contents/blog?ref=codex/crear-p%C3%A1gina-web-personal')
        .then(res => res.json())
        .then(data => {
            if (Array.isArray(data)) {
                dynamicContainer.innerHTML = '';
                data.filter(f => f.name.endsWith('.html')).reverse().forEach(file => {
                    const card = document.createElement('a');
                    card.href = `blog/${file.name}`;
                    card.className = 'card';
                    card.innerHTML = `🌐 ${file.name.replace('.html', '').replace(/-/g, ' ').toUpperCase()}`;
                    dynamicContainer.appendChild(card);
                });
            }
        })
        .catch(err => console.error("Error GitHub:", err));
}
