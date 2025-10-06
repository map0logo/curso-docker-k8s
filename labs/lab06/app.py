from fastapi import FastAPI, HTTPException
import os
import asyncpg
from pydantic import BaseModel
import socket

app = FastAPI()

# Configuración desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/mydb")
DB_USERNAME = os.getenv("DB_USERNAME", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

class Item(BaseModel):
    name: str
    description: str = None

@app.get("/")
async def read_root():
    return {
        "message": "Bienvenido a FastAPI en Kubernetes",
        "database_url": DATABASE_URL,
        "database_connected": False  # En producción verificar conexión real
    }

@app.get("/items/")
async def read_items():
    return {"items": ["item1", "item2", "item3"]}

@app.post("/items/")
async def create_item(item: Item):
    return {
        "message": "Item creado",
        "item": item.dict(),
        "database_config": {
            "url": DATABASE_URL,
            "username": DB_USERNAME
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fastapi-app"}

@app.get("/hostname")
def get_hostname():
    return {"pod_hostname": socket.gethostname()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

