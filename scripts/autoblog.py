import os
import requests
from groq import Groq
from datetime import datetime

# 1. Configuración de APIs (Cargadas desde los Secrets de GitHub)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def obtener_noticia():
    # Buscamos noticias de tecnología en español
    url = f'https://newsapi.org/v2/everything?q=IA+tecnologia&language=es&sortBy=publishedAt&pageSize=1&apiKey={NEWS_API_KEY}'
    response = requests.get(url).json()
    if response.get('articles'):
        return response['articles'][0]
    return None

def redactar_articulo(noticia):
    prompt = f"""
    Actúa como David Martínez, experto en IA y Marketing con un MBA. 
    Escribe un artículo de blog breve y profesional basado en esta noticia: {noticia['title']}.
    Contexto original: {noticia['description']}
    
    Estructura HTML (usar solo etiquetas <h2>, <p>, <strong>):
    - Título ejecutivo con impacto.
    - Resumen ejecutivo de la noticia.
    - Análisis de valor: ¿Por qué es relevante para el mercado de Latam/Ecuador?
    - Conclusión estratégica con visión de consultor.
    
    Importante: No incluyas etiquetas <html> o <body>, solo el contenido del artículo.
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return completion.choices[0].message.content

# 2. Ejecución principal
noticia = obtener_noticia()
if noticia:
    try:
        contenido_ia = redactar_articulo(noticia)
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        nombre_archivo = f"blog/post-{fecha_hoy}.html"
        
        # Asegurar que la carpeta blog existe
        os.makedirs("blog", exist_ok=True)
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido_ia)
        print(f"✅ Artículo generado con éxito: {nombre_archivo}")
    except Exception as e:
        print(f"❌ Error en la generación: {e}")
else:
    print("❌ No se encontraron noticias hoy.")
