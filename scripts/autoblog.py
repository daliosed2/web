import os
import requests
from google import genai
from datetime import datetime

# 1. Configuración de APIs
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Nueva forma de configurar el cliente en 2026
client = genai.Client(api_key=GEMINI_API_KEY)

def obtener_noticia():
    url = f'https://newsapi.org/v2/everything?q=IA+tecnologia&language=es&sortBy=publishedAt&pageSize=1&apiKey={NEWS_API_KEY}'
    response = requests.get(url).json()
    if response.get('articles'):
        return response['articles'][0]
    return None

def redactar_articulo(noticia):
    prompt = f"""
    Actúa como David Martínez, experto en IA y Marketing con un MBA. 
    Escribe un artículo de blog breve y profesional basado en esta noticia: {noticia['title']}.
    Contexto: {noticia['description']}
    
    Estructura HTML (usar <h2>, <p>, <strong>):
    - Título ejecutivo.
    - Resumen de impacto.
    - Análisis de valor para Latam.
    - Conclusión tipo consultor.
    """
    
    # Usamos el modelo más actual y estable de 2026
    response = client.models.generate_content(
        model="gemini-1.5-flash-8b", 
        contents=prompt
    )
    return response.text

# 2. Ejecución
noticia = obtener_noticia()
if noticia:
    contenido_ia = redactar_articulo(noticia)
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"blog/post-{fecha_hoy}.html"
    
    os.makedirs("blog", exist_ok=True)
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido_ia)
    print(f"✅ Éxito: {nombre_archivo}")
else:
    print("❌ No hay noticias.")
