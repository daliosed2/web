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
    # Ampliamos el rango a 7 días pero ordenamos por frescura
    # Esto garantiza que si hoy es un día "lento" de noticias, tome la mejor de ayer
    hace_7_dias = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    url = "https://newsapi.org/v2/everything"
    
    # Query diversificada: IA mundial, Big Tech y Negocios Digitales
    queries = [
        'OpenAI OR "Inteligencia Artificial" OR ChatGPT',
        'NVIDIA OR "Apple Intelligence" OR Google Gemini',
        'Tecnología OR "Transformación Digital" OR Meta'
    ]
    
    for q in queries:
        params = {
            'q': q,
            'from': hace_7_dias,
            'language': 'es',
            'sortBy': 'publishedAt',
            'pageSize': 10,
            'apiKey': NEWS_API_KEY
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data.get('articles'):
                # Buscamos el primer artículo que tenga descripción (evita spam)
                for art in data['articles']:
                    if art['description'] and len(art['description']) > 50:
                        return art
        except Exception as e:
            print(f"⚠️ Fallo con query {q}: {e}")
            continue
            
    return None

def redactar_articulo(noticia):
    prompt = f"""
    Eres David Martínez, consultor con MBA. Genera el código HTML para una entrada de blog premium.
    Noticia: {noticia['title']}
    Fuente: {noticia['url']}
    Descripción: {noticia['description']}

    REQUISITOS ESTRUCTURALES:
    1. Comienza con <!DOCTYPE html>.
    2. En el <head>, incluye <link rel="stylesheet" href="../style.css">.
    3. CSS Interno para diseño .article (idéntico a tus otras entradas).
    4. Envuelve todo en <main class="container article">.
    5. Usa etiquetas <h2 class="label"> para: 1. RESUMEN EJECUTIVO, 2. ANÁLISIS ESTRATÉGICO, 3. IMPACTO EN EL MERCADO.
    6. Incluye la fuente con un enlace <a> y el botón de modo oscuro 🌓.

    IMPORTANTE: No uses bloques de código (```). Solo HTML puro.
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    
    content = completion.choices[0].message.content.strip()
    if content.startswith("```"):
        content = re.sub(r'^```html?\s*', '', content)
        content = re.sub(r'\s*```$', '', content)
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
        print(f"✅ Éxito: {filename}")
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("❌ No se encontró nada relevante en ninguna categoría.")
