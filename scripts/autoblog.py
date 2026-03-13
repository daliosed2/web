import os
import requests
import re
from groq import Groq
from datetime import datetime, timedelta

# 1. Configuración de APIs
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def limpiar_nombre_archivo(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9\s-]', '', texto)
    texto = re.sub(r'\s+', '-', texto).strip('-')
    return texto[:65]

def obtener_noticia():
    hace_7_dias = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    url = "https://newsapi.org/v2/everything"
    queries = [
        'OpenAI OR "Inteligencia Artificial" OR ChatGPT',
        'NVIDIA OR "Apple Intelligence" OR Google Gemini',
        'Tecnología OR "Transformación Digital" OR Meta'
    ]
    
    for q in queries:
        params = {'q': q, 'from': hace_7_dias, 'language': 'es', 'sortBy': 'publishedAt', 'pageSize': 10, 'apiKey': NEWS_API_KEY}
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data.get('articles'):
                for art in data['articles']:
                    if art['description'] and len(art['description']) > 50:
                        return art
        except: continue
    return None

def redactar_articulo(noticia):
    prompt = f"""
    Eres David Martínez. Genera un HTML profesional para esta noticia: {noticia['title']}
    Fuente: {noticia['url']}
    
    ESTRUCTURA OBLIGATORIA:
    1. <!DOCTYPE html> y <head> con:
       - <link rel="stylesheet" href="../style.css">
       - <script defer src="../script.js"></script> 
    2. En el <body>:
       - <button id="toggle-mode" aria-label="Cambiar modo oscuro">🌓</button>
       - <main class="container article">
         <h1>{noticia['title']}</h1>
         <h2 class="label">1. Resumen Ejecutivo</h2>
         <p>(Redacta un análisis profesional aquí)</p>
         <h2 class="label">2. Impacto Estratégico</h2>
         <p>(Redacta el valor estratégico aquí)</p>
         <h2 class="label">3. Fuente</h2>
         <a href="{noticia['url']}" target="_blank">Leer noticia original</a>
         <nav class="post-nav"><a href="../benchmark.html" class="back-button">Volver al Blog</a></nav>
       </main>

    REGLA: Devuelve SOLO el HTML, sin bloques de código ```.
    """
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    content = completion.choices[0].message.content.strip()
    if content.startswith("```"):
        content = re.sub(r'^```html?\s*', '', content).replace('```', '')
    return content

# Ejecución
noticia = obtener_noticia()
if noticia:
    try:
        html_final = redactar_articulo(noticia)
        slug = limpiar_nombre_archivo(noticia['title'])
        filename = f"blog/{slug}.html"
        os.makedirs("blog", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_final)
        print(f"✅ Publicado: {filename}")
    except Exception as e: print(f"❌ Error: {e}")
