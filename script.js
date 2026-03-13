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

async function loadDynamicPosts() {
    const container = document.getElementById('dynamic-posts');
    if (!container) return;

    // URL codificada para evitar conflictos con la tilde en la rama "página"
    const url = 'https://api.github.com/repos/daliosed2/web/contents/blog?ref=codex/crear-p%C3%A1gina-web-personal';

    try {
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`GitHub API respondió con status: ${response.status}`);
        }

        const files = await response.json();

        if (Array.isArray(files)) {
            container.innerHTML = ''; // Limpiar mensaje de carga
            
            // Filtramos solo archivos HTML y ordenamos (más reciente arriba)
            const htmlFiles = files.filter(f => f.name.endsWith('.html')).reverse();

            if (htmlFiles.length === 0) {
                container.innerHTML = '<p>No hay artículos automáticos aún.</p>';
                return;
            }

            htmlFiles.forEach(file => {
                const card = document.createElement('a');
                // IMPORTANTE: La ruta relativa para llegar a la carpeta blog
                card.href = `blog/${file.name}`;
                card.className = 'card';
                card.target = '_blank';
                
                // Formateamos el título: post-2026-03-12 -> 🤖 POST 2026 03 12
                const cleanName = file.name.replace('.html', '').replace(/-/g, ' ').toUpperCase();
                card.innerHTML = `🤖 ${cleanName}`;
                
                container.appendChild(card);
            });
        }
    } catch (error) {
        console.error("Error al cargar posts dinámicos:", error);
        container.innerHTML = '<p>🤖 El bot está redactando nuevas noticias...</p>';
    }
}

// Escucha cuando el DOM esté listo para ejecutar la carga
document.addEventListener('DOMContentLoaded', loadDynamicPosts);
