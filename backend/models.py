from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from database import Base


class ProductoDB(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    categoria = Column(String(100), nullable=False)
    precio_compra = Column(Float, nullable=False)
    precio_venta = Column(Float, nullable=False)
    stock_actual = Column(Integer, nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    proveedor = Column(String(200), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_ultima_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())


class ProductoCreate(BaseModel):
    sku: str
    nombre: str
    descripcion: Optional[str] = None
    categoria: str
    precio_compra: float = Field(gt=0, description="Precio de compra debe ser mayor a 0")
    precio_venta: float = Field(gt=0, description="Precio de venta debe ser mayor a 0")
    stock_actual: int = Field(ge=0, description="Stock no negativo")
    stock_minimo: int = Field(ge=0, description="Stock mínimo no negativo")
    proveedor: Optional[str] = None

    @model_validator(mode="after")
    def precio_venta_mayor_que_compra(self):
        if self.precio_venta < self.precio_compra:
            raise ValueError("El precio de venta debe ser mayor o igual al precio de compra")
        return self


class ProductoResponse(ProductoCreate):
    id: int
    fecha_creacion: datetime
    fecha_ultima_actualizacion: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProductoUpdate(BaseModel):
    sku: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    precio_compra: Optional[float] = Field(None, gt=0)
    precio_venta: Optional[float] = Field(None, gt=0)
    stock_actual: Optional[int] = Field(None, ge=0)
    stock_minimo: Optional[int] = Field(None, ge=0)
    proveedor: Optional[str] = None

    @model_validator(mode="after")
    def validar_precios(self):
        pc, pv = self.precio_compra, self.precio_venta
        if pc is not None and pv is not None and pv < pc:
            raise ValueError("El precio de venta debe ser mayor o igual al precio de compra")
        return self
