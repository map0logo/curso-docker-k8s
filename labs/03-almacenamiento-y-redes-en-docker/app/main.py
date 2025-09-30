from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import asyncpg
import os
import datetime
from contextlib import asynccontextmanager

# Configuración de la base de datos
DATABASE_URL = f"postgresql://{os.getenv('DB_USER', 'api_user')}:{os.getenv('DB_PASSWORD', 'secure_password123')}@{os.getenv('DB_HOST', 'postgres-db')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'taller_db')}"

# Modelos Pydantic
class UsuarioCreate(BaseModel):
    nombre: str
    email: str


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    fecha_creacion: datetime.datetime

# Conexión a la base de datos
async def get_db_connection():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización: crear tabla si no existe
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Tabla 'usuarios' verificada/creada")
    finally:
        await conn.close()
    yield
    # Cleanup (opcional)

app = FastAPI(
    title="API Taller Docker",
    description="API de ejemplo para el taller de Docker",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a la API del Taller Docker!", "status": "active"}

@app.get("/health")
async def health_check(conn=Depends(get_db_connection)):
    try:
        # Verificar conexión a la base de datos
        result = await conn.fetchval("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected" if result == 1 else "disconnected"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")

@app.post("/usuarios/", response_model=UsuarioResponse)
async def crear_usuario(usuario: UsuarioCreate, conn=Depends(get_db_connection)):
    try:
        query = "INSERT INTO usuarios (nombre, email) VALUES ($1, $2) RETURNING id, nombre, email, fecha_creacion"
        result = await conn.fetchrow(query, usuario.nombre, usuario.email)
        return dict(result)
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=400, detail="El email ya existe")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.get("/usuarios/", response_model=List[UsuarioResponse])
async def listar_usuarios(conn=Depends(get_db_connection)):
    try:
        results = await conn.fetch("SELECT id, nombre, email, fecha_creacion FROM usuarios ORDER BY id")
        return [dict(row) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: int, conn=Depends(get_db_connection)):
    result = await conn.fetchrow(
        "SELECT id, nombre, email, fecha_creacion FROM usuarios WHERE id = $1", 
        usuario_id
    )
    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return dict(result)