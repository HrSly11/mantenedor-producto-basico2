from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def generar_reporte_inventario_pdf(productos, categoria_filtro=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Reporte de Inventario Actual", styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph(f"Fecha: {fecha}", styles["Normal"]))
    if categoria_filtro:
        story.append(Paragraph(f"Categoría filtrada: {categoria_filtro}", styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    data = [["SKU", "Nombre", "Stock Actual", "Valor Total (stock x precio_venta)"]]
    for p in productos:
        valor_total = p.stock_actual * p.precio_venta
        data.append([p.sku, p.nombre, str(p.stock_actual), f"${valor_total:,.2f}"])

    table = Table(data)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    story.append(table)
    doc.build(story)
    buffer.seek(0)
    return buffer.read()


def generar_reporte_gestion_pdf(productos, kpis, productos_bajo_stock, img_bar_bytes, img_pie_bytes):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Reporte de Gestión - Análisis de Inventario", styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("KPIs Clave", styles["Heading2"]))
    pmv = kpis.get("producto_mas_valioso")
    if pmv:
        pmv_txt = f"{pmv['nombre']} (${pmv['valor']:,.2f})"
    else:
        pmv_txt = "N/A"
    kpi_text = f"""
    - Total de productos únicos: {kpis['total_productos']}<br/>
    - Valor total del inventario: ${kpis['valor_inventario_total']:,.2f}<br/>
    - Productos con bajo stock: {kpis['productos_bajo_stock']}<br/>
    - Producto más valioso: {pmv_txt}
    """
    story.append(Paragraph(kpi_text, styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    # Gráficos (si están disponibles)
    if img_bar_bytes:
        story.append(Paragraph("Gráfico: Top categorías por cantidad", styles["Heading2"]))
        story.append(Image(BytesIO(img_bar_bytes), width=5.5 * inch, height=3.5 * inch))
        story.append(Spacer(1, 0.2 * inch))

    if img_pie_bytes:
        story.append(Paragraph("Gráfico: Valor por categoría", styles["Heading2"]))
        story.append(Image(BytesIO(img_pie_bytes), width=5 * inch, height=3.5 * inch))
        story.append(Spacer(1, 0.2 * inch))

    # Si no hay gráficos, mostrar tablas de datos
    if not img_bar_bytes and productos:
        story.append(Paragraph("Distribución por Categoría (Tabla)", styles["Heading2"]))
        from collections import Counter
        cat_count = Counter([p.categoria for p in productos])
        data = [["Categoría", "Cantidad de Productos"]]
        for cat, count in cat_count.most_common(10):
            data.append([cat, str(count)])
        table = Table(data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.2 * inch))

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Productos a Reordenar (stock <= mínimo)", styles["Heading2"]))
    data = [["SKU", "Nombre", "Stock Actual", "Stock Mínimo"]]
    for p in productos_bajo_stock:
        data.append([p.sku, p.nombre, str(p.stock_actual), str(p.stock_minimo)])
    if len(data) == 1:
        story.append(Paragraph("No hay productos con bajo stock. Excelente gestión de inventario.", styles["Normal"]))
    else:
        table = Table(data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)

    # Agregar listado de todos los productos
    story.append(Spacer(1, 0.3 * inch))
    story.append(PageBreak())
    story.append(Paragraph("Listado Completo de Productos", styles["Heading2"]))
    story.append(Spacer(1, 0.2 * inch))

    data = [["SKU", "Nombre", "Categoría", "Stock", "P. Venta", "Valor Total"]]
    for p in productos[:50]:  # Limitar a 50 para no saturar el PDF
        valor_total = p.stock_actual * p.precio_venta
        data.append([
            p.sku,
            p.nombre[:25] + "..." if len(p.nombre) > 25 else p.nombre,
            p.categoria[:15],
            str(p.stock_actual),
            f"${p.precio_venta:.2f}",
            f"${valor_total:,.2f}"
        ])

    table = Table(data, colWidths=[1.2*inch, 2*inch, 1.3*inch, 0.8*inch, 1*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#440154")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(table)

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
