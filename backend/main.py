import os
from typing import List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy.orm import Session

import crud
import models
from database import engine, get_db
from models import ProductoCreate, ProductoResponse, ProductoUpdate
from report_generator import generar_reporte_gestion_pdf, generar_reporte_inventario_pdf

models.Base.metadata.create_all(bind=engine)

# Ejecutar seeding automáticamente al iniciar
def run_startup_migrations():
    """Ejecutar migraciones y seeding al iniciar la aplicación."""
    try:
        from seed_data import seed_database
        seed_database()
    except Exception as e:
        print(f"No se pudo ejecutar seeding: {e}")
run_startup_migrations()

app = FastAPI(title="Product Manager API", version="1.0")

_cors = os.getenv("CORS_ORIGINS", "http://localhost:8501,http://127.0.0.1:8501")
allow_origins = [o.strip() for o in _cors.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def calcular_kpis(productos):
    if not productos:
        return {
            "total_productos": 0,
            "valor_inventario_total": 0.0,
            "productos_bajo_stock": 0,
            "producto_mas_valioso": None,
        }
    total_productos = len(productos)
    valor_total = sum(p.stock_actual * p.precio_compra for p in productos)
    bajo_stock = sum(1 for p in productos if p.stock_actual < p.stock_minimo)
    valores = [(p.id, p.nombre, p.stock_actual * p.precio_compra) for p in productos]
    if valores:
        max_producto = max(valores, key=lambda x: x[2])
        producto_mas_valioso = {"nombre": max_producto[1], "valor": max_producto[2]}
    else:
        producto_mas_valioso = None
    return {
        "total_productos": total_productos,
        "valor_inventario_total": round(valor_total, 2),
        "productos_bajo_stock": bajo_stock,
        "producto_mas_valioso": producto_mas_valioso,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/productos/", response_model=ProductoResponse, status_code=201)
def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_producto(db, producto)


@app.get("/productos/", response_model=List[ProductoResponse])
def read_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_productos(db, skip=skip, limit=limit)


@app.get("/productos/bajo-stock/", response_model=List[ProductoResponse])
def productos_bajo_stock(db: Session = Depends(get_db)):
    productos = crud.listar_todos_productos(db)
    bajo_stock = [p for p in productos if p.stock_actual <= p.stock_minimo]
    bajo_stock.sort(key=lambda x: x.stock_actual)
    return bajo_stock


@app.get("/productos/{producto_id}", response_model=ProductoResponse)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.get_producto(db, producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto


@app.put("/productos/{producto_id}", response_model=ProductoResponse)
def update_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    return crud.update_producto(db, producto_id, producto)


@app.delete("/productos/{producto_id}")
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    return crud.delete_producto(db, producto_id)


@app.get("/kpis/")
def get_kpis(db: Session = Depends(get_db)):
    productos = crud.listar_todos_productos(db)
    return calcular_kpis(productos)


@app.get("/datos/grafico-categorias-cantidad/")
def datos_categorias_cantidad(db: Session = Depends(get_db)):
    productos = crud.listar_todos_productos(db)
    if not productos:
        return []
    df = pd.DataFrame([(p.categoria,) for p in productos], columns=["categoria"])
    conteo = df["categoria"].value_counts().head(10).reset_index()
    conteo.columns = ["categoria", "cantidad"]
    return conteo.to_dict(orient="records")


@app.get("/datos/grafico-valor-por-categoria/")
def datos_valor_categoria(db: Session = Depends(get_db)):
    productos = crud.listar_todos_productos(db)
    if not productos:
        return []
    data = []
    for p in productos:
        valor = p.stock_actual * p.precio_compra
        data.append({"categoria": p.categoria, "valor": valor})
    df = pd.DataFrame(data)
    suma = df.groupby("categoria")["valor"].sum().reset_index()
    return suma.to_dict(orient="records")


@app.post("/reportes/inventario/")
def reporte_inventario(categoria: Optional[str] = None, db: Session = Depends(get_db)):
    productos = crud.listar_todos_productos(db)
    if categoria:
        productos = [p for p in productos if p.categoria.lower() == categoria.lower()]
    pdf_bytes = generar_reporte_inventario_pdf(productos, categoria)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=reporte_inventario.pdf"},
    )


@app.post("/reportes/gestion/")
def reporte_gestion(db: Session = Depends(get_db)):
    """Generar reporte de gestión SIN gráficos (más rápido y confiable)."""
    productos = crud.listar_todos_productos(db)
    kpis = calcular_kpis(productos)
    bajo_stock = [p for p in productos if p.stock_actual <= p.stock_minimo]
    bajo_stock.sort(key=lambda x: x.stock_actual)

    # NO generar imágenes - usar reporte solo con tablas (instantáneo)
    pdf_bytes = generar_reporte_gestion_pdf(productos, kpis, bajo_stock, None, None)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=reporte_gestion.pdf"},
    )
