from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from conexion import engine, get_db, Base
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

app = FastAPI(title="API PostgreSQL - Clientes")

# ⭐ Crear tablas automáticamente en Render y local
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
#esta función se ejecuta al iniciar la aplicación y crea las tablas en la base de datos si no existen

# REDIRECCIÓN AUTOMÁTICA DEL ROOT → /clientes
@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(
        url="/clientes/",
        status_code=status.HTTP_308_PERMANENT_REDIRECT
    )
# si quieres editar tus datos en vez de poner clientes enla barra de navegacion escribes docs
#
#  ---- CREATE ----
@app.post("/clientes/", response_model=schemas.ClienteResponse, status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    new_client = models.ClienteDB(
        cliente=cliente.cliente,
        tipo_factura=cliente.tipo_factura,
        precios=cliente.precios
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client
#esta función crea un nuevo cliente en la base de datos usando los datos proporcionados en el cuerpo de la solicitud

# ---- READ ALL ----
@app.get("/clientes/", response_model=list[schemas.ClienteResponse])
def read_clientes(db: Session = Depends(get_db)):
    return db.query(models.ClienteDB).all()

# ---- READ BY ID ----
@app.get("/clientes/{cliente_id}", response_model=schemas.ClienteResponse)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.ClienteDB).filter(models.ClienteDB.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente
#esto función obtiene un cliente específico por su ID y devuelve un error 404 si no se encuentra
# ---- UPDATE ----
@app.patch("/clientes/{cliente_id}", response_model=schemas.ClienteResponse)
def update_cliente(cliente_id: int, data: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    cliente = db.query(models.ClienteDB).filter(models.ClienteDB.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    updates = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)
    return cliente
#esta función actualiza los datos de un cliente específico usando los datos proporcionados en el cuerpo de la solicitud. Solo se actualizan los campos que se proporcionan.
# ---- DELETE ----
@app.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.ClienteDB).filter(models.ClienteDB.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    db.delete(cliente)
    db.commit()
    return {"ok": True}

#esta función elimina un cliente específico de la base de datos y devuelve un error 404 si no se encuentra

@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/clientes/", status_code=status.HTTP_308_PERMANENT_REDIRECT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-eeq-8.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#--esta funcion solo fucniona cuando el frontend y backend estan en diferentes dominios--
#esta configuración de CORS permite que solo el frontend alojado en el dominio especificado acceda a esta API
