import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# ================================
# 1. OBTENER DATABASE_URL
# ================================
DATABASE_URL = "postgresql://crud_db_e25g_user:B59N3tXf76ErC4JJSQwHzLEjhxBgTwJN@dpg-d4sr89i4d50c73d3ud6g-a.oregon-postgres.render.com/crud_db_e25g"
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no está configurada")
#este bloque obtiene la URL de la base de datos desde una variable de entorno o usa una URL por defecto para desarrollo local
# ================================
# 2. AÑADIR SSL PARA RENDER
# ================================
# Render siempre usa sslmode=require
if "render.com" in DATABASE_URL and "sslmode" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

#este bloque añade el parámetro sslmode=require a la URL de la base de datos si no está ya presente y si la base de datos está alojada en Render.com

# ================================
# 3. CREAR ENGINE
# ================================
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True#esto ayuda a mantener las conexiones vivas
)
#esto crea el engine de SQLAlchemy que se usará para conectarse a la base de datos

# ================================
# 4. CONFIGURAR SESIÓN
# ================================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
#esta clase se usa para crear sesiones de base de datos que se usarán en las rutas de FastAPI
# ================================
# 5. BASE DE MODELOS
# ================================
Base = declarative_base()
#esta clase se usa como base para definir los modelos de la base de datos con SQLAlchemy

# ================================
# 6. VALIDAR CONEXIÓN
# ================================
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("🔥 [conexion] Conexión a PostgreSQL exitosa.")
except Exception as e:
    print("❌ [conexion] Error al conectar a PostgreSQL:", e)

# ================================
# 7. DEPENDENCIA PARA FASTAPI
# ================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#esta funcion se usa en fastapi para obtener una sesión de base de datos y asegurarse de que se cierre correctamente después de usarla