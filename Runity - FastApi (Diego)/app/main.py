from fastapi import FastAPI
from app.api.v1.api import api_router

# Instancia principal de FastAPI. 
# Aquí configuramos los metadatos que aparecerán en la documentación automática (/docs).
app = FastAPI(
    title="Runity API", 
    description="Backend para el MVP de la aplicación Runity (Seguimiento deportivo)", 
    version="1.0.0"
)

# Registro del enrutador principal.
# Todas las rutas de la aplicación estarán bajo el prefijo global /api/v1 
# para permitir futuras versiones de la API sin romper la compatibilidad.
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    """Ruta raíz para verificar que el servidor está levantado."""
    return {"message": "API de Runity en funcionamiento. Visita /docs para la documentación."}