import os
import requests
import re
import time
from groq import Groq
from datetime import datetime, timedelta

# 1. Configuración de APIs
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def limpiar_carpeta_vieja(dias=15):
    """Borra archivos de la carpeta blog que tengan más de X días"""
    ruta_blog = "blog"
    if not os.path.exists(ruta_blog):
        return
    
    ahora = time.time()
    limite = ahora - (dias * 86400)
    
    for archivo in os.listdir(ruta_blog):
        ruta_archivo = os.path.join(ruta_blog, archivo)
        if os.path.isfile(ruta_archivo) and archivo.endswith(".html"):
            if os.path.getmtime(ruta_archivo) < limite:
                os.remove(ruta_archivo)
                print(f"🗑️ Archivo antiguo eliminado: {archivo}")

def limpiar_nombre_archivo(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9\s-]', '', texto)
    texto = re.sub(r'\s+', '-', texto).strip('-')
    return texto[:65]

def obtener_noticia():
    # Buscamos noticias de los últimos 3 días para garantizar resultados
    hace_3_dias = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    url = "https://newsapi.org/v2/everything"
    queries = ['OpenAI OR ChatGPT OR NVIDIA', 'Inteligencia Artificial', 'Tecnología']
    
    for q in queries:
        params = {'q': q, 'from': hace_3_dias, 'language': 'es', 'sortBy': 'publishedAt', 'pageSize': 5, 'apiKey': NEWS_API_KEY}
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data.get('articles'):
                for art in data['articles']:
                    if art.get('description') and len(art['description']) > 50:
                        return art
        except: continue
    return None

def redactar_articulo(noticia):
    prompt = f"""
    Eres David Martínez. Genera un HTML profesional para esta noticia: {noticia['title']}
    Fuente: {noticia['url']}
    
    ESTRUCTURA OBLIGATORIA:
    - <!DOCTYPE html> y <head> con <link rel="stylesheet" href="../style.css"> y <script defer src="../script.js"></script>
    - En el <body>: <button id="toggle-mode">🌓</button>
    - <main class="container article">
      <h1>{noticia['title']}</h1>
      <h2 class="label">Contexto</h2> <p>(Resumen profesional)</p>
      <h2 class="label">Análisis Estratégico</h2> <p>(Análisis de valor MBA)</p>
      <a href="{noticia['url']}" target="_blank">Fuente original</a>
      <nav class="post-nav"><a href="../benchmark.html">Volver al Blog</a></nav>
    </main>
    """
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    content = completion.choices[0].message.content.strip()
    
    # Limpieza de código para evitar errores de renderizado
    inicio = content.find("<!DOCTYPE")
    fin = content.find("</html>")
    if inicio != -1 and fin != -1:
        content = content[inicio:fin+7]
    
    return content.replace("```html", "").replace("```", "").strip()

# Ejecución Principal
if __name__ == "__main__":
    # 1. Limpiamos lo viejo primero
    limpiar_carpeta_vieja(dias=15)
    
    # 2. Generamos lo nuevo
    noticia = obtener_noticia()
    if noticia:
        try:
            html_final = redactar_articulo(noticia)
            slug = limpiar_nombre_archivo(noticia['title'])
            filename = f"blog/{slug}.html"
            os.makedirs("blog", exist_ok=True)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_final)
            print(f"✅ Nuevo análisis publicado: {filename}")
        except Exception as e:
            print(f"❌ Error en la redacción: {e}")
    else:
        print("❌ No se encontraron noticias nuevas para hoy.")
