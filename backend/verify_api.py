"""
Comprobaciones rápidas de rutas y lógica (SQLite temporal). Ejecutar desde la carpeta backend:
  python verify_api.py
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
_fd, _db_path = tempfile.mkstemp(prefix="verify_mantenedor_", suffix=".db")
os.close(_fd)
_DB = Path(_db_path)
os.environ["DATABASE_URL"] = f"sqlite:///{_DB.as_posix()}"
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402


def main():
    client = TestClient(app)

    h = client.get("/health")
    assert h.status_code == 200 and h.json() == {"status": "ok"}, h.text

    r = client.get("/productos/bajo-stock/")
    assert r.status_code == 200 and r.json() == [], r.text

    payload = {
        "sku": "SKU-1",
        "nombre": "Test",
        "categoria": "Cat",
        "precio_compra": 10.0,
        "precio_venta": 15.0,
        "stock_actual": 2,
        "stock_minimo": 5,
        "descripcion": None,
        "proveedor": None,
    }
    c = client.post("/productos/", json=payload)
    assert c.status_code == 201, c.text
    pid = c.json()["id"]

    r2 = client.get("/productos/bajo-stock/")
    assert r2.status_code == 200 and len(r2.json()) == 1, r2.text

    k = client.get("/kpis/")
    assert k.status_code == 200 and k.json()["total_productos"] == 1, k.text

    d = client.get("/datos/grafico-categorias-cantidad/")
    assert d.status_code == 200 and len(d.json()) == 1, d.text

    u = client.put(f"/productos/{pid}", json={"precio_venta": 5.0})
    assert u.status_code == 400, u.text

    u2 = client.put(f"/productos/{pid}", json={"precio_venta": 20.0})
    assert u2.status_code == 200, u2.text

    inv = client.post("/reportes/inventario/")
    assert inv.status_code == 200 and inv.headers.get("content-type", "").startswith("application/pdf")

    if os.environ.get("VERIFY_FULL") == "1":
        gest = client.post("/reportes/gestion/")
        assert gest.status_code == 200 and gest.headers.get("content-type", "").startswith(
            "application/pdf"
        )

    try:
        _DB.unlink(missing_ok=True)
    except OSError:
        pass
    print("verify_api: OK")


if __name__ == "__main__":
    main()
