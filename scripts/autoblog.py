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
    # Elimina caracteres especiales para crear una URL válida
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9\s-]', '', texto)
    texto = re.sub(r'\s+', '-', texto).strip('-')
    return texto[:50] # Limitamos longitud

def obtener_noticia():
    url = f'https://newsapi.org/v2/everything?q=IA+tecnologia&language=es&sortBy=publishedAt&pageSize=1&apiKey={NEWS_API_KEY}'
    response = requests.get(url).json()
    if response.get('articles'):
        return response['articles'][0]
    return None

def redactar_articulo(noticia):
    fecha_hoy = datetime.now().strftime("%d de %B, %Y")
    
    prompt = f"""
    Eres David Martínez, consultor con MBA experto en IA. 
    Escribe un archivo HTML COMPLETO basado en esta noticia: {noticia['title']}
    Url fuente: {noticia['url']}
    Descripción: {noticia['description']}

    DEBES SEGUIR ESTA ESTRUCTURA EXACTA:
    1. <!DOCTYPE html> y etiquetas <head> con SEO (meta description basada en la noticia).
    2. Incluye Google Analytics (G-TPRYYR8VJP).
    3. Usa el CSS interno para .article que ya conoces.
    4. Contenido:
       - <h1> con el título de la noticia.
       - <h2 class="label">1. ¿Qué pasó?</h2> resumen ejecutivo.
       - <h2 class="label">2. ¿Por qué es importante?</h2> análisis estratégico para Latam.
       - <h2 class="label">3. Fuentes</h2> link <a> a la noticia original.
       - Fecha de publicación al final.

    REGLA: Devuelve SOLO el código HTML. No pongas "Aquí tienes el código".
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )
    return completion.choices[0].message.content

# 2. Ejecución
noticia = obtener_noticia()
if noticia:
    try:
        html_completo = redactar_articulo(noticia)
        # El nombre del archivo ahora es el título de la noticia
        nombre_limpio = limpiar_nombre_archivo(noticia['title'])
        nombre_archivo = f"blog/{nombre_limpio}.html"
        
        os.makedirs("blog", exist_ok=True)
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(html_completo)
        print(f"✅ Web generada: {nombre_archivo}")
    except Exception as e:
        print(f"❌ Error: {e}")
