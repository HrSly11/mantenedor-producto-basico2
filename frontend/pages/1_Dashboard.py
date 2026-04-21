import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ui_theme import apply_ui_theme, badge, section_card
from utils import obtener_bajo_stock, obtener_datos_grafico_barras, obtener_datos_grafico_pastel, obtener_kpis, obtener_productos

st.set_page_config(page_title="Dashboard", layout="wide")
apply_ui_theme()

# Sidebar contextual del Dashboard
with st.sidebar:
    st.markdown("### 📊 Panel de Control")
    st.markdown("---")
    
    # Resumen de alertas
    bajo_stock_sidebar = obtener_bajo_stock()
    if bajo_stock_sidebar:
        criticos = len([x for x in bajo_stock_sidebar if x["stock_actual"] == 0])
        bajos = len(bajo_stock_sidebar) - criticos
        
        st.markdown("#### ⚠️ Alertas de Stock")
        if criticos > 0:
            st.error(f"🔴 {criticos} sin stock")
        if bajos > 0:
            st.warning(f"🟡 {bajos} stock bajo")
        st.markdown(f"**Total:** {len(bajo_stock_sidebar)} productos")
    else:
        st.success("✅ Sin alertas")
    
    st.markdown("---")
    st.markdown("#### 🚀 Navegación Rápida")
    st.markdown("[📦 Gestionar Productos](./Productos)")
    st.markdown("[📑 Generar Reportes](./Reportes)")

st.title("Panel de Control")
section_card(
    "Resumen Ejecutivo",
    "Monitorea inventario, bajo stock y distribución de valor por categoría en tiempo real.",
    icon="📊"
)

kpis = obtener_kpis()
bajo_stock = obtener_bajo_stock()

if kpis:
    # Métricas principales en cards mejoradas - Usando st.metric para alineación perfecta
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📦 Total Productos",
            value=f"{kpis.get('total_productos', 0)}",
            delta=None
        )

    with col2:
        total_valor = kpis.get('valor_inventario_total', 0)
        st.metric(
            label="💰 Valor Inventario",
            value=f"${total_valor:,.2f}",
            delta=None
        )

    with col3:
        bajo_stock_count = kpis.get('productos_bajo_stock', 0)
        delta_val = f"{bajo_stock_count} alertas" if bajo_stock_count > 0 else "OK"
        delta_color = "inverse" if bajo_stock_count > 0 else "normal"
        st.metric(
            label="⚠️ Bajo Stock",
            value=bajo_stock_count,
            delta=delta_val,
            delta_color=delta_color
        )

    with col4:
        prod_valioso = kpis.get("producto_mas_valioso")
        if prod_valioso:
            nombre_corto = prod_valioso["nombre"][:18] + "..." if len(prod_valioso["nombre"]) > 18 else prod_valioso["nombre"]
            st.metric(
                label="🏆 Producto más valioso",
                value=f"${prod_valioso['valor']:,.0f}",
                delta=nombre_corto
            )
        else:
            st.metric(
                label="🏆 Producto más valioso",
                value="N/A"
            )
else:
    st.warning("No se pudieron cargar los KPIs")

st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

# Gráficos en dos columnas
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("<h3 style='margin-bottom: 1rem;'>📈 Top Categorías por Cantidad</h3>", unsafe_allow_html=True)
    data_bar = obtener_datos_grafico_barras()
    if data_bar and len(data_bar) > 0:
        df_bar = pd.DataFrame(data_bar)

        # Colores del sistema de diseño Viridis
        colors = ['#440154', '#31688E', '#21918C', '#35B779', '#90D743', '#FDE725']

        fig_bar = go.Figure(data=[
            go.Bar(
                x=df_bar["categoria"],
                y=df_bar["cantidad"],
                marker=dict(
                    color=colors[:len(df_bar)],
                    line=dict(color='rgba(68,1,84,0.3)', width=1)
                ),
                text=df_bar["cantidad"],
                textposition='outside',
                textfont=dict(family='Fira Code', size=12)
            )
        ])
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Fira Sans', size=12, color='#1A1A2E'),
            xaxis=dict(title='Categoría', gridcolor='rgba(0,0,0,0.05)'),
            yaxis=dict(title='Cantidad', gridcolor='rgba(0,0,0,0.05)'),
            margin=dict(l=40, r=20, t=20, b=60),
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("No hay datos suficientes para el gráfico de barras")

with col_chart2:
    st.markdown("<h3 style='margin-bottom: 1rem;'>🥧 Distribución de Valor</h3>", unsafe_allow_html=True)
    data_pie = obtener_datos_grafico_pastel()
    if data_pie and len(data_pie) > 0:
        df_pie = pd.DataFrame(data_pie)

        fig_pie = go.Figure(data=[
            go.Pie(
                labels=df_pie["categoria"],
                values=df_pie["valor"],
                hole=0.5,
                marker=dict(
                    colors=['#440154', '#3E4A89', '#31688E', '#21918C', '#35B779', '#90D743', '#FDE725'],
                    line=dict(color='white', width=2)
                ),
                textinfo='label+percent',
                textfont=dict(family='Fira Sans', size=11),
                hovertemplate='%{label}<br>$%{value:,.2f}<br>%{percent}<extra></extra>'
            )
        ])
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Fira Sans', size=12, color='#1A1A2E'),
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
            height=350,
            annotations=[dict(text=f'Total<br>${df_pie["valor"].sum():,.0f}', x=0.5, y=0.5, font_size=14, showarrow=False)]
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("No hay datos suficientes para el gráfico de pastel")

st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

# Alertas de stock bajo
st.markdown("<h3>⚠️ Productos a Reordenar (stock ≤ mínimo)</h3>", unsafe_allow_html=True)

if bajo_stock:
    df_alerts = pd.DataFrame(bajo_stock)
    df_alerts["estado"] = df_alerts.apply(
        lambda x: "Crítico" if x["stock_actual"] == 0 else "Bajo",
        axis=1
    )

    # Colores para el estado
    def color_estado(val):
        if val == "Crítico":
            return 'background-color: rgba(239, 68, 68, 0.15); color: #EF4444; font-weight: 600;'
        return 'background-color: rgba(253, 231, 37, 0.15); color: #9A7D0A; font-weight: 600;'

    styled_df = df_alerts[["sku", "nombre", "stock_actual", "stock_minimo", "categoria", "estado"]].style\
        .map(color_estado, subset=["estado"])\
        .set_properties(**{
            'font-family': 'Fira Sans',
            'font-size': '0.9rem'
        })

    st.dataframe(styled_df, use_container_width=True, height=250)

    # Resumen de alertas
    criticos = len([x for x in bajo_stock if x["stock_actual"] == 0])
    bajos = len(bajo_stock) - criticos

    alert_cols = st.columns(3)
    with alert_cols[0]:
        st.markdown(f"<div style='text-align: center; background: #EFF6FF; padding: 1rem; border-radius: 10px;'><span style='font-size: 2rem; color: #440154;'>{len(bajo_stock)}</span><br><span style='color: #1A1A2E;'>Productos en alerta</span></div>", unsafe_allow_html=True)
    with alert_cols[1]:
        st.markdown(f"<div style='text-align: center; background: #FEF2F2; padding: 1rem; border-radius: 10px;'><span style='font-size: 2rem; color: #EF4444;'>{criticos}</span><br><span style='color: #1A1A2E;'>Sin stock</span></div>", unsafe_allow_html=True)
    with alert_cols[2]:
        st.markdown(f"<div style='text-align: center; background: #FEF9C3; padding: 1rem; border-radius: 10px;'><span style='font-size: 2rem; color: #9A7D0A;'>{bajos}</span><br><span style='color: #1A1A2E;'>Stock bajo</span></div>", unsafe_allow_html=True)
else:
    # Si no hay productos en alerta, mostrar los productos con menor stock
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #35B779;'>
        <h4 style='color: #065F46; margin: 0;'>✅ Inventario Saludable</h4>
        <p style='color: #047857; margin: 0.5rem 0 0 0;'>No hay productos con bajo stock. Todo está en orden.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar productos con menor stock (aunque no estén en alerta)
    st.markdown("<h4 style='color: #1A1A2E;'>📦 Productos con menor stock (top 10)</h4>", unsafe_allow_html=True)
    productos_all = obtener_productos()
    if productos_all:
        # Ordenar por stock actual ascendente y mostrar los primeros 10
        productos_ordenados = sorted(productos_all, key=lambda x: x.get("stock_actual", 999))[:10]
        df_low = pd.DataFrame(productos_ordenados)
        if not df_low.empty and "stock_actual" in df_low.columns:
            st.dataframe(df_low[["id", "sku", "nombre", "categoria", "stock_actual", "stock_minimo"]], 
                        use_container_width=True, height=300)

