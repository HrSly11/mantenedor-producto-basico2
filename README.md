# Sistema de gestión de productos (mantenedor-productos2)

Sistema para PYMES: inventario, KPIs, gráficos interactivos y reportes PDF.

## Arquitectura

- **Backend:** FastAPI + SQLAlchemy + PostgreSQL (API REST).
- **Frontend:** Streamlit que consume la API por HTTP (`requests`).
- **Ventajas:** Separación de responsabilidades, API reutilizable, la UI no accede a la base de datos.

## Prerrequisitos

- Python 3.9+
- PostgreSQL 13+ (local)
- `pip`

## Instalación y ejecución paso a paso (sin Docker)

### Paso 1: Crear entorno virtual

Abrir PowerShell en la raíz del proyecto:

```powershell
cd mantenedor-productos2
python -m venv venv
```

### Paso 2: Activar entorno virtual

```powershell
.\venv\Scripts\Activate.ps1
```

> Si da error de política de ejecución:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Paso 3: Instalar dependencias del backend

```powershell
cd backend
pip install -r requirements.txt
cd ..
```

### Paso 4: Instalar dependencias del frontend

```powershell
cd frontend
pip install -r requirements.txt
cd ..
```

### Paso 5: Configurar archivo `.env`

Crear archivo `.env` en la carpeta `backend/` con este contenido:

```env
DATABASE_URL=postgresql://postgres:TU_CONTRASEÑA@localhost:5432/product_db
API_BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:8501,http://127.0.0.1:8501
```

> Reemplaza `TU_CONTRASEÑA` con la contraseña real de PostgreSQL.
> Si usas SQLite, cambia la URL a: `sqlite:///./app.db`

### Paso 6: Crear base de datos en PostgreSQL (solo si usas PostgreSQL)

```sql
CREATE DATABASE product_db;
```

### Paso 7: Levantar backend (Terminal 1)

Desde la raíz del proyecto, con el entorno virtual activado:

```powershell
.\venv\Scripts\Activate.ps1
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

> Las tablas y 34 productos de ejemplo se crean automáticamente al iniciar.

### Paso 8: Levantar frontend (Terminal 2)

Abrir **nueva terminal** PowerShell en la raíz del proyecto:

```powershell
cd mantenedor-productos2
.\venv\Scripts\Activate.ps1
streamlit run .\frontend\app.py --server.port 8501 --server.address 0.0.0.0
```

- Aplicación: http://localhost:8501

### Paso 9: Verificar que todo funciona

En una tercera terminal PowerShell:

```powershell
# Verificar backend
curl.exe http://localhost:8000/health
# Debe devolver: {"status":"ok"}

# Verificar frontend
curl.exe -I http://localhost:8501
# Debe devolver: HTTP/1.1 200 OK
```

## Solución de errores comunes

### a) `streamlit : no se reconoce...`
El entorno virtual no está activado o no se instaló streamlit.

```powershell
.\venv\Scripts\Activate.ps1
pip install streamlit
streamlit run .\frontend\app.py --server.port 8501
```

### b) `Port XXXX is already in use`
El puerto ya lo usa otro proceso.

**Opción 1 - Liberar el puerto:**
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Opción 2 - Usar otro puerto:**
```powershell
# Backend en puerto 8010
uvicorn main:app --reload --host 127.0.0.1 --port 8010

# Frontend en puerto 8502
streamlit run .\frontend\app.py --server.port 8502
```

> Si cambias el puerto del backend, actualiza `API_BASE_URL` en `.env`

### c) Error de conexión con PostgreSQL
Verificar que PostgreSQL esté corriendo:
```powershell
# En pgAdmin o psql:
SELECT version();
```

O cambiar a SQLite temporalmente en `.env`:
```env
DATABASE_URL=sqlite:///./app.db
```

## Migrar a otra máquina (paso a paso)

1. **Instalar Python 3.9+** desde python.org
2. **Instalar PostgreSQL 13+** (o usar SQLite para pruebas)
3. **Copiar/clonar** el proyecto completo (sin la carpeta `venv`)
4. **Seguir los 9 pasos** de arriba desde "Paso 1: Crear entorno virtual"

> **Importante:** No copies la carpeta `venv` entre máquinas. Siempre recrea el entorno virtual en la máquina destino.

## Uso de la aplicación

- Menú lateral: **Dashboard**, **Productos**, **Reportes**.
- **Productos:** alta, edición por selección, búsqueda por nombre/SKU/categoría, baja con confirmación.
- **Dashboard:** KPIs, gráficos Plotly, tabla de reorden con productos de bajo stock.
- **Reportes:** PDF de inventario (filtro por categoría) y PDF de gestión (KPIs + análisis).

## Verificación automática (API)

Desde `backend/` (no requiere PostgreSQL; usa SQLite temporal):

```bash
python verify_api.py
```

Para incluir también el PDF de gestión:

```bash
set VERIFY_FULL=1
python verify_api.py
```

## Notas técnicas

- Los PDF de gestión generan PNG con Plotly + **Kaleido** en el servidor (`kaleido` en `backend/requirements.txt`).
- Validación `precio_venta >= precio_compra` en Pydantic v2 (`model_validator`) y de nuevo en **actualización parcial** en `crud.update_producto`.
- **Rutas:** `GET /productos/bajo-stock/` va **antes** que `GET /productos/{id}` para no capturar `bajo-stock` como entero.
- **KPIs y reportes** usan `listar_todos_productos` (sin límite 100); el listado paginado sigue en `GET /productos/`.
- **Transacciones:** `get_db` y operaciones CRUD hacen `rollback` ante errores; `pool_pre_ping` en el engine para PostgreSQL.
- **Salud:** `GET /health` para balanceadores y el sidebar de Streamlit (`verificar_backend`).
- No se usa `kpis_logic.py`: `calcular_kpis` está en `main.py`.

## Docker (opcional)

```bash
docker compose up --build
```

Requiere los `Dockerfile` en `backend/` y `frontend/`. Postgres monta `database/schema.sql` al crear el volumen por primera vez.

## Mejoras futuras

- Autenticación de usuarios.
- Paginación en listados.
- Exportación a Excel.
