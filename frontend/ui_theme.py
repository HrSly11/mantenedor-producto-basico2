import streamlit as st


# Colores del tema profesional Viridis (fijo, sin toggle)
PRIMARY = "#440154"      # Púrpura Viridis
SECONDARY = "#21918C"    # Teal
ACCENT = "#FDE725"       # Amarillo
BG_COLOR = "#F8FAFC"     # Gris muy claro
TEXT_COLOR = "#1A1A2E"   # Texto oscuro
CARD_BG = "#FFFFFF"      # Cards blancas
SIDEBAR_BG = "linear-gradient(180deg, #440154 0%, #31688E 100%)"
BORDER_COLOR = "rgba(68, 1, 84, 0.12)"
MUTED_COLOR = "#4B5563"


def apply_ui_theme() -> None:
    """Apply professional Viridis design system - tema fijo."""

    css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700&display=swap');

    :root {
        --color-primary: #440154;
        --color-secondary: #21918C;
        --color-accent: #FDE725;
        --color-background: #F8FAFC;
        --color-text: #1A1A2E;
        --color-muted: #4B5563;
        --color-border: rgba(68, 1, 84, 0.12);
        --color-card-bg: #FFFFFF;
    }

    .stApp {
        background: #F8FAFC;
        color: #1A1A2E;
        font-family: 'Fira Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Sidebar styling - Gradiente Viridis */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #440154 0%, #31688E 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FDE725 !important;
        font-family: 'Fira Code', monospace;
    }

    /* Main content area */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Typography */
    h1 {
        color: #440154 !important;
        font-family: 'Fira Code', monospace;
        font-weight: 700;
        font-size: 2.25rem;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }

    h2 {
        color: #31688E !important;
        font-family: 'Fira Code', monospace;
        font-weight: 600;
        font-size: 1.5rem;
        letter-spacing: -0.01em;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    h3 {
        color: #21918C !important;
        font-family: 'Fira Sans', sans-serif;
        font-weight: 600;
        font-size: 1.125rem;
    }

    /* Cards */
    .app-card {
        background: #FFFFFF;
        border: 1px solid rgba(68, 1, 84, 0.12);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(26,26,46,0.06);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .app-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(68,1,84,0.15);
        border-color: rgba(68, 1, 84, 0.2);
    }

    /* KPI cards */
    .kpi-card {
        background: #FFFFFF;
        border: 2px solid rgba(33, 145, 140, 0.2);
        border-radius: 14px;
        padding: 1.25rem;
        box-shadow: 0 2px 12px rgba(26,26,46,0.06);
        transition: all 0.3s ease;
    }

    .kpi-card:hover {
        box-shadow: 0 4px 20px rgba(33, 145, 140, 0.25);
        border-color: rgba(33, 145, 140, 0.4);
    }

    [data-testid="stMetricValue"] {
        color: #21918C !important;
        font-family: 'Fira Code', monospace;
        font-weight: 700;
        font-size: 1.75rem;
    }

    [data-testid="stMetricLabel"] {
        color: #440154 !important;
        font-weight: 600;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* BOTONES - Alto contraste, siempre visibles */
    .stButton > button {
        background: linear-gradient(135deg, #440154 0%, #31688E 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.25rem !important;
        font-weight: 600 !important;
        font-family: 'Fira Sans', sans-serif !important;
        box-shadow: 0 2px 8px rgba(68, 1, 84, 0.3) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(68, 1, 84, 0.4) !important;
        background: linear-gradient(135deg, #5a1a6e 0%, #41789e 100%) !important;
    }

    /* Botones secundarios */
    .stButton > button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #440154 !important;
        border: 2px solid #440154 !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: rgba(68, 1, 84, 0.05) !important;
    }

    /* Labels de formularios - Texto oscuro visible */
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stTextArea > label,
    .stMultiSelect > label {
        color: #1A1A2E !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.25rem !important;
    }

    /* Form elements - Fondo blanco, texto oscuro */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > textarea {
        border: 2px solid #D1D5DB;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-family: 'Fira Sans', sans-serif;
        background: #FFFFFF !important;
        color: #111827 !important;
        font-weight: 500;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > textarea:focus {
        border-color: #21918C;
        box-shadow: 0 0 0 3px rgba(33, 145, 140, 0.25);
    }

    /* Selectbox - Estilo claro */
    .stSelectbox > div[data-baseweb="select"] > div,
    .stMultiSelect > div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 2px solid #D1D5DB !important;
        border-radius: 10px !important;
        color: #111827 !important;
    }

    .stSelectbox > div[data-baseweb="select"] > div:hover,
    .stMultiSelect > div[data-baseweb="select"] > div:hover {
        border-color: #21918C !important;
    }

    /* Dropdown menu */
    div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
    }

    div[data-baseweb="popover"] div[role="listbox"] {
        background-color: #FFFFFF !important;
    }

    div[data-baseweb="popover"] div[role="option"] {
        background-color: #FFFFFF !important;
        color: #111827 !important;
    }

    div[data-baseweb="popover"] div[role="option"]:hover {
        background-color: #EFF6FF !important;
        color: #440154 !important;
    }

    /* TABLAS - Filas intercaladas azul y blanco */
    .stDataFrame {
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(26,26,46,0.06);
    }

    .stDataFrame th {
        background: linear-gradient(135deg, #440154 0%, #31688E 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600;
        padding: 0.75rem;
        text-align: center !important;
    }

    .stDataFrame td {
        padding: 0.6rem 0.75rem;
        border-bottom: 1px solid #E5E7EB;
    }

    /* Filas intercaladas - azul claro y blanco */
    .stDataFrame tbody tr:nth-child(odd) {
        background-color: #FFFFFF !important;
    }

    .stDataFrame tbody tr:nth-child(even) {
        background-color: #EFF6FF !important;
    }

    .stDataFrame tbody tr:hover {
        background-color: #DBEAFE !important;
    }

    /* Section cards */
    .section-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1px solid rgba(68, 1, 84, 0.1);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 2px 12px rgba(26,26,46,0.06);
    }

    .section-card h2 {
        color: #440154 !important;
        margin: 0 0 0.5rem 0;
        font-size: 1.25rem;
    }

    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .badge-success {
        background: rgba(53, 183, 121, 0.15);
        color: #15803d;
    }

    .badge-warning {
        background: rgba(253, 231, 37, 0.2);
        color: #9A7D0A;
    }

    .badge-danger {
        background: rgba(239, 68, 68, 0.1);
        color: #EF4444;
    }

    .badge-primary {
        background: rgba(68, 1, 84, 0.1);
        color: #440154;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #440154 0%, #31688E 100%) !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 0.75rem 1rem !important;
        font-weight: 600 !important;
    }

    .streamlit-expanderContent {
        background: #FFFFFF;
        border: 1px solid rgba(68, 1, 84, 0.12);
        border-radius: 0 0 10px 10px;
        padding: 1rem;
    }

    /* Responsive */
    @media (max-width: 768px) {
        h1 { font-size: 1.75rem; }
        .app-card { padding: 1rem; }
        [data-testid="stMetricValue"] { font-size: 1.5rem; }
    }
</style>
    """

    st.markdown(css, unsafe_allow_html=True)


def section_card(title: str, subtitle: str = "", icon: str = "") -> None:
    """Display a section header card with optional icon and subtitle."""
    icon_html = f"<span style='font-size: 1.5rem; margin-right: 0.5rem;'>{icon}</span>" if icon else ""
    extra = f"<p class='muted' style='margin-top: 0.5rem; margin-bottom: 0; color: #4B5563;'>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class='app-card'>
            <h3 style='display: flex; align-items: center; margin: 0; color: #21918C;'>
                {icon_html}{title}
            </h3>
            {extra}
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str = "") -> None:
    """Display a KPI metric card."""
    delta_html = f"<span style='color: #35B779; font-size: 0.875rem;'>▲ {delta}</span>" if delta else ""
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div style='font-size: 0.75rem; color: #440154; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;'>
                {label}
            </div>
            <div style='font-size: 1.75rem; font-family: "Fira Code", monospace; font-weight: 700; color: #21918C; margin: 0.25rem 0;'>
                {value}
            </div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge(text: str, variant: str = "primary") -> str:
    """Return a badge HTML string."""
    variants = {
        "primary": "badge-primary",
        "success": "badge-success",
        "warning": "badge-warning",
        "danger": "badge-danger",
    }
    css_class = variants.get(variant, "badge-primary")
    return f"<span class='badge {css_class}'>{text}</span>"


def chart_container(chart_func):
    """Wrapper for charts with consistent styling container."""
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    chart_func()
    st.markdown("</div>", unsafe_allow_html=True)
