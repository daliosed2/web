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
    return texto[:60]

def obtener_noticia():
    # Calculamos la fecha de ayer para filtrar frescura absoluta
    ayer = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    url = "https://newsapi.org/v2/everything"
    # Query optimizada para intereses mundiales en IA y Tech
    query_busqueda = '(OpenAI OR "Artificial Intelligence" OR NVIDIA OR Gemini OR "Llama 3") AND (tecnología OR innovación)'
    
    params = {
        'q': query_busqueda,
        'from': ayer,
        'language': 'es',
        'sortBy': 'publishedAt', # Prioriza lo más reciente
        'pageSize': 1,
        'apiKey': NEWS_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('articles') and len(data['articles']) > 0:
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
    2. En el <head>, incluye <link rel="stylesheet" href="../style.css"> e incluye Google Analytics (G-TPRYYR8VJP).
    3. Usa este CSS interno:
       .article{{max-width:780px;margin:0 auto;text-align:left;padding:40px 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}}
       .article h1{{font-size: 2.2rem; line-height: 1.2; margin-bottom: 2rem; color: var(--text-color);}}
       .article h2.label{{color:#b5b5b5; margin-top:2.5rem; font-weight:600; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 1px;}}
       .article p{{line-height:1.8; margin-bottom: 1.5rem; font-size: 1.1rem; color: var(--text-color);}}
       .post-nav{{margin-top:50px; border-top: 1px solid #444; padding-top: 30px;}}
       .back-button{{padding:12px 24px; background:var(--card-bg); color:var(--text-color); text-decoration:none; border-radius:8px; display: inline-block;}}

    4. En el <body>, pon el botón <button id="toggle-mode">🌓</button>.
    5. Envuelve TODO en <main class="container article">.
    6. Secciones: 
       - <h1>Título noticia</h1>
       - <h2 class="label">1. Análisis de Actualidad</h2> (Resumen de lo ocurrido en las últimas 24h).
       - <h2 class="label">2. Impacto Estratégico Mundial</h2> (Por qué esto cambia las reglas del juego).
       - <h2 class="label">3. Fuente</h2> (Link directo).

    IMPORTANTE: Devuelve SOLO el código HTML limpio.
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    
    content = completion.choices[0].message.content.strip()
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
        print(f"✅ Análisis de actualidad publicado: {filename}")
    except Exception as e:
        print(f"❌ Error en el proceso: {e}")
else:
    print("❌ No se encontraron noticias de impacto en las últimas 24 horas.")
