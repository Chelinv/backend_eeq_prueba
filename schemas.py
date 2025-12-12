from pydantic import BaseModel, Field

# Esquema base para los datos de un cliente
class ClienteBase(BaseModel):
    cliente: str = Field(..., max_length=255)
    tipo_factura: str = Field(..., max_length=50)
    precios: float = Field(..., gt=0) # gt=0 asegura que el precio sea positivo

# Esquema para crear un cliente (usa ClienteBase)
class ClienteCreate(ClienteBase):
    pass

# Esquema para actualizar un cliente (todos los campos son opcionales)
class ClienteUpdate(BaseModel):
    cliente: str | None = Field(None, max_length=255)
    tipo_factura: str | None = Field(None, max_length=50)
    precios: float | None = Field(None, gt=0)

# Esquema para la respuesta de la API (incluye el ID)
class ClienteResponse(ClienteBase):
    id: int

    class Config:
        # Esto permite que Pydantic lea los datos del objeto ORM
        from_attributes = True
