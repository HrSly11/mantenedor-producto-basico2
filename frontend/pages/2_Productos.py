import pandas as pd
import streamlit as st

from ui_theme import apply_ui_theme, badge, section_card
from utils import actualizar_producto, crear_producto, eliminar_producto, obtener_productos

st.set_page_config(page_title="Gestión de Productos", layout="wide")
apply_ui_theme()

# Sidebar contextual de Productos
with st.sidebar:
    st.markdown("### 📦 Gestión de Productos")
    st.markdown("---")
    
    # Obtener datos para resumen
    productos_sidebar = obtener_productos()
    if productos_sidebar:
        total_prod = len(productos_sidebar)
        categorias = set(p.get("categoria", "Sin categoría") for p in productos_sidebar)
        bajo_stock_count = len([p for p in productos_sidebar if p.get("stock_actual", 0) <= p.get("stock_minimo", 0)])
        
        st.markdown(f"**📊 Total:** {total_prod} productos")
        st.markdown(f"**📂 Categorías:** {len(categorias)}")
        
        if bajo_stock_count > 0:
            st.warning(f"⚠️ {bajo_stock_count} en alerta")
        else:
            st.success("✅ Stock OK")
        
        st.markdown("---")
        st.markdown("#### 📂 Categorías")
        for cat in sorted(categorias)[:5]:  # Mostrar máximo 5
            count = len([p for p in productos_sidebar if p.get("categoria") == cat])
            st.markdown(f"- {cat}: {count}")
    
    st.markdown("---")
    st.markdown("#### 🚀 Atajos")
    st.markdown("[📊 Ver Dashboard](./Dashboard)")
    st.markdown("[📑 Ir a Reportes](./Reportes)")

st.title("Gestión de Productos")
section_card(
    "Administración de Catálogo",
    "Crea, busca, actualiza y elimina productos con validaciones de negocio integradas.",
    icon="📦"
)

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

with st.expander("➕ Agregar Producto", expanded=st.session_state.edit_id is not None):
    if st.session_state.edit_id:
        st.subheader(f"Editando producto ID: {st.session_state.edit_id}")
        productos = obtener_productos() or []
        producto_edit = next((p for p in productos if p["id"] == st.session_state.edit_id), None)
        if producto_edit:
            sku_val = producto_edit["sku"]
            nombre_val = producto_edit["nombre"]
            desc_val = producto_edit.get("descripcion") or ""
            cat_val = producto_edit["categoria"]
            pc_val = producto_edit["precio_compra"]
            pv_val = producto_edit["precio_venta"]
            stock_val = producto_edit["stock_actual"]
            min_val = producto_edit["stock_minimo"]
            prov_val = producto_edit.get("proveedor") or ""
        else:
            st.error("Producto no encontrado")
            st.session_state.edit_id = None
            st.stop()
    else:
        sku_val = nombre_val = desc_val = cat_val = prov_val = ""
        pc_val = pv_val = 0.0
        stock_val = min_val = 0

    with st.form("producto_form", clear_on_submit=not st.session_state.edit_id):
        col1, col2 = st.columns(2)
        with col1:
            sku = st.text_input("SKU *", value=sku_val if st.session_state.edit_id else "")
            nombre = st.text_input("Nombre *", value=nombre_val if st.session_state.edit_id else "")
            categoria = st.text_input("Categoría *", value=cat_val if st.session_state.edit_id else "")
            precio_compra = st.number_input(
                "Precio compra *",
                min_value=0.01,
                step=0.01,
                value=float(pc_val) if st.session_state.edit_id else 0.01,
            )
            stock_actual = st.number_input(
                "Stock actual *",
                min_value=0,
                step=1,
                value=int(stock_val) if st.session_state.edit_id else 0,
            )
        with col2:
            precio_venta = st.number_input(
                "Precio venta *",
                min_value=0.01,
                step=0.01,
                value=float(pv_val) if st.session_state.edit_id else 0.01,
            )
            stock_minimo = st.number_input(
                "Stock mínimo *",
                min_value=0,
                step=1,
                value=int(min_val) if st.session_state.edit_id else 0,
            )
            proveedor = st.text_input("Proveedor", value=prov_val if st.session_state.edit_id else "")
            descripcion = st.text_area("Descripción", value=desc_val if st.session_state.edit_id else "")

        submitted = st.form_submit_button("Guardar producto")
        if submitted:
            if not sku or not nombre or not categoria or precio_compra <= 0 or precio_venta <= 0:
                st.error("Complete los campos obligatorios (*)")
            elif precio_venta < precio_compra:
                st.error("El precio de venta debe ser mayor o igual al precio de compra")
            else:
                data = {
                    "sku": sku,
                    "nombre": nombre,
                    "categoria": categoria,
                    "precio_compra": precio_compra,
                    "precio_venta": precio_venta,
                    "stock_actual": int(stock_actual),
                    "stock_minimo": int(stock_minimo),
                    "descripcion": descripcion or None,
                    "proveedor": proveedor or None,
                }
                if st.session_state.edit_id:
                    resp = actualizar_producto(st.session_state.edit_id, data)
                    if resp:
                        st.success("Producto actualizado")
                        st.session_state.edit_id = None
                        st.rerun()
                else:
                    resp = crear_producto(data)
                    if resp:
                        st.success("Producto creado")
                        st.rerun()

    if st.session_state.edit_id:
        if st.button("Cancelar edición"):
            st.session_state.edit_id = None
            st.rerun()

st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

# Sección de listado y filtros
st.markdown("<h3>📋 Inventario de Productos</h3>", unsafe_allow_html=True)

productos = obtener_productos()
if productos:
    df = pd.DataFrame(productos)

    # Filtros mejorados en una barra
    filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 1])

    with filter_col1:
        busqueda = st.text_input("🔍 Buscar por nombre, SKU o categoría", "", placeholder="Escribe para buscar...")

    with filter_col2:
        categorias = ["Todas"] + sorted(df["categoria"].unique().tolist())
        categoria_filter = st.selectbox("📂 Categoría", categorias)

    with filter_col3:
        estado_filter = st.selectbox("📊 Estado", ["Todos", "Stock OK", "Stock Bajo", "Sin Stock"])

    # Aplicar filtros
    df_filtered = df.copy()
    if busqueda:
        mask = (
            df_filtered["nombre"].astype(str).str.contains(busqueda, case=False, na=False)
            | df_filtered["sku"].astype(str).str.contains(busqueda, case=False, na=False)
            | df_filtered["categoria"].astype(str).str.contains(busqueda, case=False, na=False)
        )
        df_filtered = df_filtered.loc[mask]

    if categoria_filter != "Todas":
        df_filtered = df_filtered[df_filtered["categoria"] == categoria_filter]

    if estado_filter != "Todos":
        if estado_filter == "Sin Stock":
            df_filtered = df_filtered[df_filtered["stock_actual"] == 0]
        elif estado_filter == "Stock Bajo":
            df_filtered = df_filtered[
                (df_filtered["stock_actual"] > 0) &
                (df_filtered["stock_actual"] <= df_filtered["stock_minimo"])
            ]
        else:  # Stock OK
            df_filtered = df_filtered[df_filtered["stock_actual"] > df_filtered["stock_minimo"]]

    # Agregar columna de estado
    def get_estado(row):
        if row["stock_actual"] == 0:
            return "Sin Stock"
        elif row["stock_actual"] <= row["stock_minimo"]:
            return "Stock Bajo"
        return "OK"

    df_filtered["estado"] = df_filtered.apply(get_estado, axis=1)

    # Mostrar resumen de filtros
    total_filter = len(df_filtered)
    total_general = len(df)
    st.markdown(f"<p class='muted'>Mostrando <strong>{total_filter}</strong> de <strong>{total_general}</strong> productos</p>", unsafe_allow_html=True)

    # Tabla con estilos mejorados
    display_cols = [
        "id", "sku", "nombre", "categoria", "precio_compra",
        "precio_venta", "stock_actual", "stock_minimo", "estado"
    ]

    # Función para colorear el estado
    def color_estado_cell(val):
        if val == "Sin Stock":
            return 'background-color: rgba(239, 68, 68, 0.15); color: #EF4444; font-weight: 600; border-radius: 4px;'
        elif val == "Stock Bajo":
            return 'background-color: rgba(253, 231, 37, 0.15); color: #9A7D0A; font-weight: 600; border-radius: 4px;'
        return 'background-color: rgba(53, 183, 121, 0.15); color: #35B779; font-weight: 600; border-radius: 4px;'

    # Preparar dataframe con columna de seleccion
    df_editor = df_filtered[display_cols].copy()
    df_editor.insert(0, "✅", False)  # Columna de seleccion al inicio
    
    st.markdown("<p style='color: #440154; font-weight: 600;'>📋 Marca la casilla del producto que quieres editar/eliminar:</p>", unsafe_allow_html=True)
    
    # Tabla editable con columna de seleccion
    edited_df = st.data_editor(
        df_editor,
        column_config={
            "✅": st.column_config.CheckboxColumn("Seleccionar", help="Marca para seleccionar", default=False),
            "precio_compra": st.column_config.NumberColumn("Precio Compra", format="$%.2f"),
            "precio_venta": st.column_config.NumberColumn("Precio Venta", format="$%.2f"),
        },
        disabled=display_cols,  # Solo la columna de seleccion es editable
        hide_index=True,
        use_container_width=True,
        height=350,
        key="product_table"
    )
    
    # Obtener el producto seleccionado (el que tiene checkbox marcado)
    selected_rows = edited_df[edited_df["✅"] == True]
    
    # Acciones compactas en una sola fila
    st.markdown("<h3>⚙️ Acciones Rápidas</h3>", unsafe_allow_html=True)
    
    # Crear lista de opciones para selectbox
    productos_opciones = {f"#{p['id']} - {p['nombre']} ({p['sku']})": p['id'] for p in productos}
    opciones_list = list(productos_opciones.keys())
    
    # Determinar index por defecto basado en seleccion de la tabla
    default_index = 0
    if len(selected_rows) > 0:
        selected_id_from_table = int(selected_rows.iloc[0]["id"])
        for i, opt in enumerate(opciones_list):
            if productos_opciones[opt] == selected_id_from_table:
                default_index = i
                break
    
    # Fila compacta de acciones
    action_cols = st.columns([3, 1, 1])
    
    with action_cols[0]:
        selected_product = st.selectbox("Seleccionar producto", opciones_list, index=default_index, key="action_select")
        selected_id = productos_opciones[selected_product]
    
    with action_cols[1]:
        st.markdown("<div style='padding-top: 1.75rem;'>", unsafe_allow_html=True)
        if st.button("✏️ Editar", use_container_width=True):
            st.session_state.edit_id = selected_id
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with action_cols[2]:
        st.markdown("<div style='padding-top: 1.75rem;'>", unsafe_allow_html=True)
        # Expander para eliminar (evita clics accidentales)
        with st.expander("🗑️ Eliminar"):
            st.markdown(f"""
            <div style='background-color: #FEF3C7; border-left: 4px solid #F59E0B; padding: 0.75rem 1rem; border-radius: 6px; margin-bottom: 1rem;'>
                <span style='color: #92400E; font-weight: 600;'>⚠️ ¿Eliminar producto #{selected_id}?</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Confirmar eliminación", type="primary", use_container_width=True):
                if eliminar_producto(selected_id) is not None:
                    st.success(f"Producto #{selected_id} eliminado")
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("No hay productos registrados. Agrega productos usando el formulario de arriba.")
