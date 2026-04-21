import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")


def _url(endpoint: str) -> str:
    ep = endpoint.lstrip("/")
    return f"{API_BASE_URL}/{ep}"


def _format_api_error(detail):
    if isinstance(detail, list):
        msgs = []
        for item in detail:
            if isinstance(item, dict) and "msg" in item:
                loc = item.get("loc", [])
                msgs.append(f"{' → '.join(str(x) for x in loc)}: {item['msg']}")
        return "; ".join(msgs) if msgs else str(detail)
    return str(detail)


def api_get(endpoint):
    try:
        response = requests.get(_url(endpoint), timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión con el backend: {e}")
        return None


def api_post(endpoint, data=None, params=None):
    try:
        response = requests.post(_url(endpoint), json=data, params=params, timeout=120)
        response.raise_for_status()
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return response.content
    except requests.exceptions.RequestException as e:
        st.error(f"Error al enviar datos: {e}")
        return None


def api_put(endpoint, data):
    try:
        response = requests.put(_url(endpoint), json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        st.error(f"Error al actualizar: {_format_api_error(detail)}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error al actualizar: {e}")
        return None


def api_delete(endpoint):
    try:
        response = requests.delete(_url(endpoint), timeout=30)
        response.raise_for_status()
        if response.content:
            return response.json()
        return {"ok": True}
    except requests.exceptions.RequestException as e:
        st.error(f"Error al eliminar: {e}")
        return None


def obtener_productos():
    return api_get("productos/")


def crear_producto(producto):
    try:
        response = requests.post(_url("productos/"), json=producto, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        try:
            body = e.response.json()
            detail = body.get("detail", e.response.text)
        except Exception:
            detail = e.response.text
        st.error(f"Error al crear: {_format_api_error(detail)}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error al crear: {e}")
        return None


def actualizar_producto(pid, producto):
    return api_put(f"productos/{pid}", producto)


def eliminar_producto(pid):
    return api_delete(f"productos/{pid}")


def obtener_kpis():
    return api_get("kpis/")


def obtener_bajo_stock():
    return api_get("productos/bajo-stock/")


def obtener_datos_grafico_barras():
    return api_get("datos/grafico-categorias-cantidad/")


def obtener_datos_grafico_pastel():
    return api_get("datos/grafico-valor-por-categoria/")


def generar_reporte_inventario(categoria=None):
    try:
        params = {"categoria": categoria} if categoria else None
        response = requests.post(_url("reportes/inventario/"), params=params, timeout=120)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException:
        st.error("Error al generar reporte de inventario")
        return None


def generar_reporte_gestion():
    try:
        with st.spinner("Generando reporte de gestión..."):
            # Timeout de 30s es suficiente ahora que no hay gráficos
            response = requests.post(_url("reportes/gestion/"), timeout=30)
            response.raise_for_status()
            return response.content
    except requests.exceptions.Timeout:
        st.error("⏱️ El reporte está tardando demasiado. Reinicia el backend e intenta de nuevo.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error al generar reporte: {str(e)}")
        st.info("💡 Tip: Verifica que el backend esté corriendo en http://localhost:8010")
        return None


def verificar_backend() -> bool:
    try:
        r = requests.get(_url("health"), timeout=5)
        if r.status_code == 200:
            return r.json().get("status") == "ok"
    except requests.exceptions.RequestException:
        pass
    return False
