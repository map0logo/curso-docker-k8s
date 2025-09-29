from typing import Union

from fastapi import FastAPI

## Inicialización de FastAPI, que incluye un título y una descripción que se mostrará al iniciar la aplicación
app = FastAPI(
    title="Mi App FastAPI Dockerizada",
    description="Una aplicación simple contenerizada con Docker",
    version="1.0.0"
)

## Función 'Hola Mundo' que incluye además el nombre del host
@app.get("/")
def read_root():
    return {
        "message": "¡Hola Mundo desde Docker!",
        "version": "1.0.0"
    }

## Función que devolverá el estado actual de la aplicación junto a la fecha.
## Por el momento, no hace nada más que devolver el status "healthy"
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": __import__('datetime').datetime.now().isoformat()}

## Función que devuelve un objeto de una base de datos.
## Por el momento, solo devolverá un string vacio y el ID del objeto.
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

