import streamlit as st

from ui_theme import apply_ui_theme, kpi_card, section_card
from utils import generar_reporte_gestion, generar_reporte_inventario, obtener_productos

st.set_page_config(page_title="Reportes", layout="wide")
apply_ui_theme()

# Sidebar contextual de Reportes
with st.sidebar:
    st.markdown("### 📑 Módulo de Reportes")
    st.markdown("---")
    
    st.markdown("#### 📋 Tipos de Reporte")
    st.markdown("""
    **📄 Reporte de Inventario**
    - Listado completo de productos
    - Valoración por categoría
    - Stock actual vs mínimo
    
    **📊 Reporte de Gestión**
    - KPIs del sistema
    - Alertas de stock
    - Análisis de inventario
    """)
    
    st.markdown("---")
    
    # Info del sistema
    st.markdown("#### ℹ️ Información")
    st.info("Los reportes se generan en formato PDF y pueden descargarse directamente.")
    
    st.markdown("---")
    st.markdown("#### 🚀 Navegación")
    st.markdown("[📊 Ir al Dashboard](./Dashboard)")
    st.markdown("[📦 Gestionar Productos](./Productos)")

st.title("Módulo de Reportes")
section_card(
    "Reportes Operativos y Estratégicos",
    "Genera documentos PDF para inventario y análisis de gestión.",
    icon="📑"
)

st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

# Sección de reporte de inventario
st.markdown("<h3>📦 Reporte Operacional - Inventario</h3>", unsafe_allow_html=True)

categorias = []
productos = obtener_productos()
if productos:
    categorias = sorted({p["categoria"] for p in productos})

with st.container():
    st.markdown("<div style='background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%); border: 1px solid rgba(68, 1, 84, 0.1); border-radius: 14px; padding: 1.5rem; margin: 1rem 0;'>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        categoria_filter = st.selectbox(
            "Filtrar por categoría (opcional)",
            ["Todas"] + categorias,
            help="Selecciona una categoría específica o deja 'Todas' para incluir todo el inventario"
        )

    with col2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)  # Spacer for alignment
        if st.button("📄 Generar PDF", use_container_width=True):
            with st.spinner("Generando reporte de inventario..."):
                cat = None if categoria_filter == "Todas" else categoria_filter
                pdf = generar_reporte_inventario(cat)
                if pdf:
                    st.download_button(
                        "⬇️ Descargar PDF",
                        data=pdf,
                        file_name=f"reporte_inventario_{categoria_filter.lower().replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

    st.markdown("</div>", unsafe_allow_html=True)

# Sección de reporte de gestión
st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
st.markdown("<h3>📊 Reporte de Gestión - Análisis Estratégico</h3>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div style='background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%); border: 1px solid rgba(68, 1, 84, 0.1); border-radius: 14px; padding: 1.5rem; margin: 1rem 0;'>", unsafe_allow_html=True)

    col_info, col_action = st.columns([3, 1])

    with col_info:
        st.markdown("""
        <div style='color: #6B7280; font-size: 0.95rem;'>
        <strong>Este reporte incluye:</strong><br>
        • Resumen ejecutivo de KPIs<br>
        • Gráficos de distribución por categoría<br>
        • Análisis de productos con bajo stock<br>
        • Valoración total del inventario
        </div>
        """, unsafe_allow_html=True)

    with col_action:
        if st.button("📈 Generar Reporte", use_container_width=True):
            pdf = generar_reporte_gestion()
            if pdf:
                st.download_button(
                    "⬇️ Descargar PDF",
                    data=pdf,
                    file_name="reporte_gestion.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

    st.markdown("</div>", unsafe_allow_html=True)

# Resumen de datos disponibles
if productos:
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    st.markdown("<h3>📈 Resumen de Datos Disponibles</h3>", unsafe_allow_html=True)

    # Estadísticas rápidas
    total_categorias = len(categorias)
    total_productos = len(productos)
    valor_total = sum(p["precio_venta"] * p["stock_actual"] for p in productos)

    stats_col1, stats_col2, stats_col3 = st.columns(3)
    with stats_col1:
        kpi_card("Total Productos", f"{total_productos}")
    with stats_col2:
        kpi_card("Categorías", f"{total_categorias}")
    with stats_col3:
        kpi_card("Valor Total", f"${valor_total:,.2f}")

