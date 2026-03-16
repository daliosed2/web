import os
import requests
import re
import time
from groq import Groq
from datetime import datetime, timedelta

# APIs
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def limpiar_nombre(t):
    t = t.lower()
    t = re.sub(r'[^a-z0-9\s-]', '', t)
    return re.sub(r'\s+', '-', t).strip('-')[:60]

def obtener_noticia():
    # Ampliamos búsqueda para asegurar que siempre haya algo
    hace_5_dias = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': 'IA OR "Inteligencia Artificial" OR OpenAI OR NVIDIA',
        'from': hace_5_dias,
        'language': 'es',
        'sortBy': 'publishedAt',
        'pageSize': 5,
        'apiKey': NEWS_API_KEY
    }
    try:
        r = requests.get(url, params=params)
        data = r.json()
        if data.get('articles'):
            for a in data['articles']:
                if a.get('description') and len(a['description']) > 40:
                    return a
    except: return None
    return None

def redactar(noticia):
    prompt = f"Eres David Martínez, consultor MBA. Escribe un HTML profesional con <link rel='stylesheet' href='../style.css'> y <script defer src='../script.js'></script> sobre: {noticia['title']}. Incluye botón de modo oscuro 🌓. Solo HTML puro."
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    c = res.choices[0].message.content.strip()
    ini, fin = c.find("<!DOCTYPE"), c.find("</html>")
    return c[ini:fin+7] if ini != -1 else c

if __name__ == "__main__":
    # Limpieza de archivos de más de 15 días
    if os.path.exists("blog"):
        for f in os.listdir("blog"):
            if time.time() - os.path.getmtime(f"blog/{f}") > (15 * 86400):
                os.remove(f"blog/{f}")
    
    noticia = obtener_noticia()
    if noticia:
        os.makedirs("blog", exist_ok=True)
        filename = f"blog/{limpiar_nombre(noticia['title'])}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(redactar(noticia))
        print(f"✅ Post creado: {filename}")
