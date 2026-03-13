// --- LÓGICA DE MODO OSCURO UNIVERSAL ---
const setupDarkMode = () => {
    const toggleButton = document.getElementById('toggle-mode');
    const savedMode = localStorage.getItem('color-mode');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    const applyMode = (dark) => {
        if (dark) {
            document.body.classList.add('dark');
            if (toggleButton) toggleButton.textContent = '☀️';
        } else {
            document.body.classList.remove('dark');
            if (toggleButton) toggleButton.textContent = '🌓';
        }
    };

    // Inicialización
    let useDark = savedMode === 'dark' || (savedMode === null && prefersDark);
    applyMode(useDark);

    // Evento de clic
    if (toggleButton) {
        toggleButton.onclick = () => {
            useDark = !useDark;
            localStorage.setItem('color-mode', useDark ? 'dark' : 'light');
            applyMode(useDark);
        };
    }
};

// --- LÓGICA DE CARGA DE POSTS ---
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
                container.innerHTML = '<p>🤖 Analizando tendencias tecnológicas...</p>';
                return;
            }

            htmlFiles.forEach(file => {
                const card = document.createElement('a');
                card.href = `blog/${file.name}`;
                card.className = 'card';
                card.target = '_self'; // Cambiado a _self para mejor UX
                const displayTitle = file.name.replace('.html', '').replace(/-/g, ' ').toUpperCase();
                card.innerHTML = `🌐 ${displayTitle}`;
                container.appendChild(card);
            });
        }
    } catch (error) {
        console.error("Error cargando posts:", error);
    }
}

// --- INICIALIZACIÓN GENERAL ---
document.addEventListener('DOMContentLoaded', () => {
    setupDarkMode();
    loadDynamicPosts();
});
