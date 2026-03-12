import os
import requests
import google.generativeai as genai
from datetime import datetime

# 1. Configuración de APIs (Usando variables de entorno por seguridad)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # El más rápido y eficiente para esto

def obtener_noticia():
    # Buscamos noticias de IA y Tecnología en español
    url = f'https://newsapi.org/v2/everything?q=IA+tecnologia&language=es&sortBy=publishedAt&pageSize=1&apiKey={NEWS_API_KEY}'
    response = requests.get(url).json()
    if response.get('articles'):
        return response['articles'][0]
    return None

def redactar_articulo(noticia):
    prompt = f"""
    Actúa como David Martínez, experto en IA y Marketing con un MBA. 
    Escribe un artículo de blog breve y profesional basado en esta noticia: {noticia['title']}.
    
    Contexto de la noticia: {noticia['description']}
    
    Estructura del artículo (usa etiquetas HTML <h2>, <p>, <strong>):
    1. Título llamativo pero serio.
    2. Resumen ejecutivo de la noticia.
    3. Análisis de valor: ¿Por qué esto es importante para empresas en Latam?
    4. Una conclusión breve con "mi enfoque de consultor".
    
    Importante: No inventes datos. Mantén el tono directo al grano. Solo entrega el código HTML interno.
    """
    
    response = model.generate_content(prompt)
    return response.text

# 2. Ejecución principal
noticia = obtener_noticia()

if noticia:
    contenido_ia = redactar_articulo(noticia)
    
    # Crear nombre de archivo basado en la fecha
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"blog/post-{fecha_hoy}.html"
    
    # Guardar el archivo
    os.makedirs("blog", exist_ok=True)
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido_ia)
    
    print(f"✅ Artículo creado exitosamente: {nombre_archivo}")
else:
    print("❌ No se encontraron noticias hoy.")
