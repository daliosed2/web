import os
import requests
import re
from groq import Groq
from datetime import datetime

# 1. Configuración de APIs
# Asegúrate de que en GitHub Secrets los nombres coincidan exactamente
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def limpiar_nombre_archivo(texto):
    # Genera un nombre de archivo amigable para URL
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9\s-]', '', texto)
    texto = re.sub(r'\s+', '-', texto).strip('-')
    return texto[:60]

def obtener_noticia():
    # URL construida de forma limpia sin corchetes de markdown
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': 'IA tecnologia',
        'language': 'es',
        'sortBy': 'publishedAt',
        'pageSize': 1,
        'apiKey': NEWS_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('articles'):
            return data['articles'][0]
    except Exception as e:
        print(f"❌ Error al conectar con NewsAPI: {e}")
    return None

def redactar_articulo(noticia):
    prompt = f"""
    Eres David Martínez, consultor con MBA. Genera el código HTML para una entrada de blog profesional.
    Noticia: {noticia['title']}
    Fuente: {noticia['url']}
    Descripción: {noticia['description']}

    REQUISITOS ESTRUCTURALES:
    1. Comienza con <!DOCTYPE html>.
    2. En el <head>, incluye <link rel="stylesheet" href="../style.css">.
    3. Usa este CSS interno exactamente:
       .article{{max-width:780px;margin:0 auto;text-align:left;padding:40px 20px; font-family: sans-serif;}}
       .article h1{{font-size: 2.5rem; line-height: 1.2; margin-bottom: 2rem;}}
       .article h2.label{{color:#b5b5b5; margin-top:2.5rem; font-weight:600; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 1px;}}
       .article p{{line-height:1.8; margin-bottom: 1.5rem; font-size: 1.1rem; color: var(--text-color);}}
       .post-nav{{margin-top:50px; border-top: 1px solid #444; padding-top: 30px;}}
       .back-button{{padding:12px 24px; background:#222; color:#fff; text-decoration:none; border-radius:8px; display: inline-block;}}

    4. En el <body>, pon el botón <button id="toggle-mode">🌓</button>.
    5. Envuelve TODO en <main class="container article">.
    6. Secciones: <h1>Título noticia</h1>, <h2 class="label">1. Resumen Ejecutivo</h2>, <h2 class="label">2. Impacto Estratégico y Valor en Latam</h2>, <h2 class="label">3. Fuente Original</h2>.

    IMPORTANTE: Devuelve SOLO el código HTML limpio. Nada de comentarios ni bloques de código markdown (```).
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    
    content = completion.choices[0].message.content.strip()
    # Limpieza de seguridad por si la IA pone etiquetas de código
    if content.startswith("```"):
        content = re.sub(r'^```html?\s*', '', content)
        content = re.sub(r'\s*```$', '', content)
    return content

# 2. Ejecución
noticia = obtener_noticia()
if noticia:
    try:
        html_final = redactar_articulo(noticia)
        slug = limpiar_nombre_archivo(noticia['title'])
        filename = f"blog/{slug}.html"
        
        os.makedirs("blog", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_final)
        print(f"✅ Artículo publicado con éxito: {filename}")
    except Exception as e:
        print(f"❌ Error en el proceso: {e}")
else:
    print("❌ No se pudo obtener la noticia.")
