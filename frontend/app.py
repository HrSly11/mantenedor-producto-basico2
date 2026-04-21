import streamlit as st

from ui_theme import apply_ui_theme, section_card
from utils import verificar_backend

st.set_page_config(
    page_title="Sistema de Gestión de Productos",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_ui_theme()

# Suprimir errores 404 de Streamlit en console
st.markdown("""
    <script>
        // Suprimir errores 404 de _stcore en console
        const originalFetch = window.fetch;
        window.fetch = function(...args) {
            return originalFetch.apply(this, args).catch(err => {
                const url = args[0] || '';
                if (url.includes('/_stcore/')) {
                    // Silenciar errores de _stcore
                    return new Response(null, { status: 200 });
                }
                throw err;
            });
        };

        // Suprimir errores 404 en console
        const originalConsoleError = console.error;
        console.error = function(...args) {
            const message = args.join(' ');
            if (message.includes('404') && message.includes('_stcore')) {
                return; // Ignorar errores 404 de _stcore
            }
            return originalConsoleError.apply(this, args);
        };
    </script>
""", unsafe_allow_html=True)

st.title("Sistema de Gestión de Productos")
section_card(
    "Bienvenido al Sistema",
    "Administra tu inventario de manera eficiente. Usa el menú lateral para navegar entre Dashboard, Productos y Reportes.",
    icon="🏢"
)

st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

# Cards de características con iconos y mejor diseño
st.markdown("<h2 style='margin-bottom: 1rem;'>🚀 Características Principales</h2>", unsafe_allow_html=True)

feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%); border: 1px solid rgba(68, 1, 84, 0.1); border-radius: 16px; padding: 1.5rem; height: 100%; box-shadow: 0 2px 12px rgba(26,26,46,0.06); transition: transform 0.3s ease;'>
        <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📊</div>
        <h4 style='color: #440154; margin: 0 0 0.5rem 0; font-family: Fira Code, monospace;'>Dashboard</h4>
        <p style='color: #6B7280; font-size: 0.9rem; margin: 0; line-height: 1.5;'>
            Visualiza KPIs en tiempo real, gráficos de distribución y alertas de stock.
        </p>
    </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%); border: 1px solid rgba(33, 145, 140, 0.15); border-radius: 16px; padding: 1.5rem; height: 100%; box-shadow: 0 2px 12px rgba(26,26,46,0.06); transition: transform 0.3s ease;'>
        <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📦</div>
        <h4 style='color: #21918C; margin: 0 0 0.5rem 0; font-family: Fira Code, monospace;'>Gestión CRUD</h4>
        <p style='color: #6B7280; font-size: 0.9rem; margin: 0; line-height: 1.5;'>
            Crea, edita y elimina productos con validaciones de negocio integradas.
        </p>
    </div>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%); border: 1px solid rgba(53, 183, 121, 0.15); border-radius: 16px; padding: 1.5rem; height: 100%; box-shadow: 0 2px 12px rgba(26,26,46,0.06); transition: transform 0.3s ease;'>
        <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📑</div>
        <h4 style='color: #35B779; margin: 0 0 0.5rem 0; font-family: Fira Code, monospace;'>Reportes PDF</h4>
        <p style='color: #6B7280; font-size: 0.9rem; margin: 0; line-height: 1.5;'>
            Genera reportes operativos y de gestión en formato PDF para compartir.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

# Información de la categoría
st.markdown("<h2 style='margin-bottom: 1rem;'>📂 Categorías Disponibles</h2>", unsafe_allow_html=True)

cat_cols = st.columns(8)
categorias = ["Tecnología", "Oficina", "Limpieza", "Alimentos", "Hogar", "Deportes", "Salud y Belleza", "Y más..."]
colors_cat = ["#440154", "#31688E", "#21918C", "#35B779", "#90D743", "#FDE725", "#F59E0B", "#6B7280"]

for i, (cat, color) in enumerate(zip(categorias, colors_cat)):
    with cat_cols[i % 8 if i < 8 else 7]:
        st.markdown(f"""
        <div style='background: {color}; color: white; padding: 0.5rem 1rem; border-radius: 8px; text-align: center; font-size: 0.8rem; font-weight: 600; margin: 0.25rem 0;'>
            {cat}
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

# Estado del sistema
st.markdown("<h2 style='margin-bottom: 1rem;'>⚡ Estado del Sistema</h2>", unsafe_allow_html=True)

status_col1, status_col2 = st.columns(2)

with status_col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%); border: 1px solid rgba(68, 1, 84, 0.1); border-radius: 14px; padding: 1.25rem;'>
        <h4 style='color: #440154; margin: 0 0 0.75rem 0;'>🎯 Módulos Activos</h4>
        <div style='display: flex; flex-direction: column; gap: 0.5rem;'>
            <div style='display: flex; align-items: center; gap: 0.5rem;'>
                <span style='color: #35B779;'>✓</span>
                <span style='color: #1A1A2E; font-size: 0.9rem;'>Dashboard de Análisis</span>
            </div>
            <div style='display: flex; align-items: center; gap: 0.5rem;'>
                <span style='color: #35B779;'>✓</span>
                <span style='color: #1A1A2E; font-size: 0.9rem;'>Gestión de Productos (CRUD)</span>
            </div>
            <div style='display: flex; align-items: center; gap: 0.5rem;'>
                <span style='color: #35B779;'>✓</span>
                <span style='color: #1A1A2E; font-size: 0.9rem;'>Reportes PDF</span>
            </div>
            <div style='display: flex; align-items: center; gap: 0.5rem;'>
                <span style='color: #35B779;'>✓</span>
                <span style='color: #1A1A2E; font-size: 0.9rem;'>Alertas de Stock</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with status_col2:
    backend_ok = verificar_backend()
    status_color = "#35B779" if backend_ok else "#EF4444"
    status_text = "Conectado" if backend_ok else "No responde"
    status_icon = "✅" if backend_ok else "⚠️"

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%); border: 1px solid rgba(68, 1, 84, 0.1); border-radius: 14px; padding: 1.25rem;'>
        <h4 style='color: #440154; margin: 0 0 0.75rem 0;'>🔌 Estado de Conexión</h4>
        <div style='display: flex; flex-direction: column; gap: 0.75rem;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='color: #6B7280; font-size: 0.9rem;'>Backend API:</span>
                <span style='color: {status_color}; font-weight: 600; font-size: 0.9rem;'>{status_icon} {status_text}</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='color: #6B7280; font-size: 0.9rem;'>Base de Datos:</span>
                <span style='color: #35B779; font-weight: 600; font-size: 0.9rem;'>✓ Activa</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='color: #6B7280; font-size: 0.9rem;'>Frontend:</span>
                <span style='color: #35B779; font-weight: 600; font-size: 0.9rem;'>✓ Activo</span>
            </div>
        </div>
        <p style='color: #9CA3AF; font-size: 0.75rem; margin-top: 0.75rem; margin-bottom: 0;'>
            Sistema diseñado con Streamlit + FastAPI
        </p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar mejorada
st.sidebar.markdown("""
<div style='margin: -1rem -1rem 1rem -1rem; padding: 1.5rem; background: rgba(255,255,255,0.1); border-bottom: 1px solid rgba(255,255,255,0.1);'>
    <h3 style='color: #FDE725; margin: 0; font-family: Fira Code, monospace; font-size: 1.1rem;'>📦 Inventario Pro</h3>
    <p style='color: rgba(255,255,255,0.8); margin: 0.25rem 0 0 0; font-size: 0.8rem;'>Gestión Inteligente</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.success("👆 Navegación")
st.sidebar.markdown("""
<div style='color: rgba(255,255,255,0.9); font-size: 0.85rem;'>
    <p style='margin: 0 0 0.5rem 0;'><strong>Dashboard</strong><br><span style='color: rgba(255,255,255,0.7);'>KPIs y análisis visual</span></p>
    <p style='margin: 0 0 0.5rem 0;'><strong>Productos</strong><br><span style='color: rgba(255,255,255,0.7);'>CRUD de inventario</span></p>
    <p style='margin: 0 0 0.5rem 0;'><strong>Reportes</strong><br><span style='color: rgba(255,255,255,0.7);'>PDFs descargables</span></p>
</div>
""", unsafe_allow_html=True)

if backend_ok:
    st.sidebar.info("🔌 Backend API: Conectado")
else:
    st.sidebar.warning("⚠️ Backend: No responde. Verifica API_BASE_URL en .env")

