import os
import requests
import re
from groq import Groq
from datetime import datetime

# 1. Configuración de APIs
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def limpiar_nombre_archivo(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9\s-]', '', texto)
    texto = re.sub(r'\s+', '-', texto).strip('-')
    return texto[:50]

def obtener_noticia():
    url = f'[https://newsapi.org/v2/everything?q=IA+tecnologia&language=es&sortBy=publishedAt&pageSize=1&apiKey=](https://newsapi.org/v2/everything?q=IA+tecnologia&language=es&sortBy=publishedAt&pageSize=1&apiKey=){NEWS_API_KEY}'
    response = requests.get(url).json()
    if response.get('articles'):
        return response['articles'][0]
    return None

def redactar_articulo(noticia):
    fecha_hoy = datetime.now().strftime("%d de %B, %Y")
    
    prompt = f"""
    Eres David Martínez, experto con MBA. Genera el código HTML para una entrada de blog.
    Noticia: {noticia['title']}
    Fuente: {noticia['url']}
    Descripción: {noticia['description']}

    INSTRUCCIONES DE FORMATO (CRÍTICO):
    1. Comienza directamente con <!DOCTYPE html>.
    2. En el <head>, incluye <link rel="stylesheet" href="../style.css" />.
    3. En el <style>, copia exactamente esto:
       .article{{max-width:780px;margin:0 auto;text-align:left;padding:20px}}
       .article h1{{margin-bottom:.5rem; font-size: 2.5rem;}}
       .article h2.label{{color:#b5b5b5;margin-top:2rem;font-weight:600; text-transform: uppercase; font-size: 0.9rem;}}
       .article p{{line-height:1.7; margin-bottom: 1.5rem;}}
       .post-nav{{margin-top:40px; border-top: 1px solid #333; padding-top: 20px;}}
       .back-button{{padding:10px 20px; background:var(--card-bg); color:var(--text-color); text-decoration:none; border-radius:8px;}}

    4. En el <body>, incluye el botón <button id="toggle-mode">🌓</button>.
    5. Envuelve TODO el contenido en <main class="container article">.
    6. Secciones: <h1>Título</h1>, <h2 class="label">1. ¿Qué pasó?</h2>, <h2 class="label">2. ¿Por qué es importante?</h2>, <h2 class="label">3. Fuentes</h2> (con link).

    PROHIBIDO: No uses bloques de código (```), no saludes, no expliques nada. Solo el HTML.
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3, # Bajamos temperatura para más precisión estructural
    )
    # Limpieza de seguridad por si Groq añade basura
    contenido = completion.choices[0].message.content
    if "```html" in contenido:
        contenido = contenido.split("```html")[1].split("```")[0]
    return contenido.strip()

# 2. Ejecución
noticia = obtener_noticia()
if noticia:
    try:
        html_completo = redactar_articulo(noticia)
        nombre_limpio = limpiar_nombre_archivo(noticia['title'])
        nombre_archivo = f"blog/{nombre_limpio}.html"
        
        os.makedirs("blog", exist_ok=True)
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(html_completo)
        print(f"✅ Web con estilo generada: {nombre_archivo}")
    except Exception as e:
        print(f"❌ Error: {e}")
