from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import ProductoCreate, ProductoDB, ProductoUpdate


def get_producto(db: Session, producto_id: int):
    return db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()


def get_producto_by_sku(db: Session, sku: str):
    return db.query(ProductoDB).filter(ProductoDB.sku == sku).first()


def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(ProductoDB)
        .order_by(ProductoDB.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def listar_todos_productos(db: Session):
    """Todos los registros: KPIs, reportes y gráficos (evita el límite paginado por defecto)."""
    return db.query(ProductoDB).order_by(ProductoDB.id).all()


def create_producto(db: Session, producto: ProductoCreate):
    if get_producto_by_sku(db, producto.sku):
        raise HTTPException(status_code=400, detail="SKU ya existe")
    db_producto = ProductoDB(**producto.model_dump())
    db.add(db_producto)
    try:
        db.commit()
        db.refresh(db_producto)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="SKU ya existe o violación de integridad")
    except Exception:
        db.rollback()
        raise
    return db_producto


def update_producto(db: Session, producto_id: int, producto_update: ProductoUpdate):
    db_producto = get_producto(db, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    update_data = producto_update.model_dump(exclude_unset=True)
    if "sku" in update_data and update_data["sku"] != db_producto.sku:
        if get_producto_by_sku(db, update_data["sku"]):
            raise HTTPException(status_code=400, detail="SKU ya existe")

    pc = update_data.get("precio_compra", db_producto.precio_compra)
    pv = update_data.get("precio_venta", db_producto.precio_venta)
    if pv < pc:
        raise HTTPException(
            status_code=400,
            detail="El precio de venta debe ser mayor o igual al precio de compra",
        )

    for key, value in update_data.items():
        setattr(db_producto, key, value)
    try:
        db.commit()
        db.refresh(db_producto)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="SKU ya existe o violación de integridad")
    except Exception:
        db.rollback()
        raise
    return db_producto


def delete_producto(db: Session, producto_id: int):
    db_producto = get_producto(db, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    try:
        db.delete(db_producto)
        db.commit()
    except Exception:
        db.rollback()
        raise
    return {"ok": True}
