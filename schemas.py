from pydantic import BaseModel, Field

# Esquema base para los datos de un cliente
class ClienteBase(BaseModel):
    cliente: str = Field(..., max_length=255)#esta linea indica que el campo cliente es obligatorio
    tipo_factura: str = Field(..., max_length=50)
    precios: float = Field(..., gt=0) # gt=0 asegura que el precio sea positivo

# Esquema para crear un cliente (usa ClienteBase)
class ClienteCreate(ClienteBase):
    pass #esta clase hereda todos los campos de ClienteBase

# Esquema para actualizar un cliente (todos los campos son opcionales)
class ClienteUpdate(BaseModel):
    cliente: str | None = Field(None, max_length=255) #esta linea indica que el campo cliente es opcional
    tipo_factura: str | None = Field(None, max_length=50)#esta linea indica que el campo tipo_factura es opcional
    precios: float | None = Field(None, gt=0)#esta linea indica que el campo precios es opcional

# Esquema para la respuesta de la API (incluye el ID), funciona de manera local
#orm es Object Relational Mapping
#esto sirve para que pydantic pueda trabajar con objetos ORM como los de SQLAlchemy
class ClienteResponse(ClienteBase):
    id: int#esta clase indica que la respuesta incluirá el campo id además de los campos heredados de ClienteBase

    class Config:
        # Esto permite que Pydantic lea los datos del objeto ORM osea que los datos pueden venir de una base de datos
        from_attributes = True
