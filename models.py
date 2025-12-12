from sqlalchemy import Column, Integer, String, Numeric
from conexion import Base

class ClienteDB(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, index=True)
    tipo_factura = Column(String)
    precios = Column(Numeric(10, 2))
