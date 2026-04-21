"""Script para poblar la base de datos con datos de ejemplo."""
import os
from datetime import datetime
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
from models import ProductoCreate

# Lista ampliada de productos para poblar la base de datos
PRODUCTOS_SEED = [
    # Tecnología (6 productos)
    {"sku": "SKU-TEC-001", "nombre": "Mouse Inalámbrico Pro", "descripcion": "Mouse ergonómico 2.4GHz con 5 botones programables", "categoria": "Tecnología", "precio_compra": 12.50, "precio_venta": 19.90, "stock_actual": 40, "stock_minimo": 8, "proveedor": "Tech Import SAC"},
    {"sku": "SKU-TEC-002", "nombre": "Teclado Mecánico TKL", "descripcion": "Switches rojos, retroiluminado RGB", "categoria": "Tecnología", "precio_compra": 35.00, "precio_venta": 59.90, "stock_actual": 18, "stock_minimo": 5, "proveedor": "Tech Import SAC"},
    {"sku": "SKU-TEC-003", "nombre": "Monitor 24\" Full HD", "descripcion": "IPS 75Hz, bordes ultrafinos", "categoria": "Tecnología", "precio_compra": 120.00, "precio_venta": 189.90, "stock_actual": 2, "stock_minimo": 3, "proveedor": "DisplayCorp Perú"},
    {"sku": "SKU-TEC-004", "nombre": "Webcam HD 1080p", "descripcion": "Micrófono integrado, autoenfoque", "categoria": "Tecnología", "precio_compra": 25.00, "precio_venta": 45.90, "stock_actual": 30, "stock_minimo": 8, "proveedor": "Tech Import SAC"},
    {"sku": "SKU-TEC-005", "nombre": "Hub USB-C 7 en 1", "descripcion": "HDMI 4K, USB 3.0, lector SD", "categoria": "Tecnología", "precio_compra": 18.00, "precio_venta": 32.50, "stock_actual": 45, "stock_minimo": 12, "proveedor": "Accesorios Tech"},
    {"sku": "SKU-TEC-006", "nombre": "Auriculares Bluetooth", "descripcion": "Cancelación de ruido, 30h batería", "categoria": "Tecnología", "precio_compra": 45.00, "precio_venta": 79.90, "stock_actual": 22, "stock_minimo": 6, "proveedor": "AudioMax Perú"},

    # Oficina (5 productos)
    {"sku": "SKU-OFI-001", "nombre": "Cuaderno Ejecutivo A5", "descripcion": "80 hojas rayadas, tapa dura", "categoria": "Oficina", "precio_compra": 2.20, "precio_venta": 4.50, "stock_actual": 120, "stock_minimo": 30, "proveedor": "Papelería Central"},
    {"sku": "SKU-OFI-002", "nombre": "Resma Papel A4 500h", "descripcion": "Papel multiuso 75g/m²", "categoria": "Oficina", "precio_compra": 3.50, "precio_venta": 6.90, "stock_actual": 200, "stock_minimo": 50, "proveedor": "Papelería Central"},
    {"sku": "SKU-OFI-003", "nombre": "Grapadora Industrial", "descripcion": "Capacidad 40 hojas, metálica", "categoria": "Oficina", "precio_compra": 8.00, "precio_venta": 15.90, "stock_actual": 35, "stock_minimo": 10, "proveedor": "Office Supply SAC"},
    {"sku": "SKU-OFI-004", "nombre": "Porta Documentos A4", "descripcion": "Plástico transparente, pack 10", "categoria": "Oficina", "precio_compra": 1.50, "precio_venta": 3.20, "stock_actual": 80, "stock_minimo": 20, "proveedor": "Papelería Central"},
    {"sku": "SKU-OFI-005", "nombre": "Marcadores Permanentes", "descripcion": "Pack 12 colores surtidos", "categoria": "Oficina", "precio_compra": 4.00, "precio_venta": 8.50, "stock_actual": 60, "stock_minimo": 15, "proveedor": "Arte y Oficina"},

    # Limpieza (5 productos)
    {"sku": "SKU-LIM-001", "nombre": "Detergente Multiusos 1L", "descripcion": "Limpieza de superficies, aroma limón", "categoria": "Limpieza", "precio_compra": 1.80, "precio_venta": 3.20, "stock_actual": 65, "stock_minimo": 20, "proveedor": "Distribuidora Hogar"},
    {"sku": "SKU-LIM-002", "nombre": "Desinfectante Spray 500ml", "descripcion": "Elimina 99.9% de bacterias", "categoria": "Limpieza", "precio_compra": 2.50, "precio_venta": 4.50, "stock_actual": 8, "stock_minimo": 15, "proveedor": "Química Hogar"},
    {"sku": "SKU-LIM-003", "nombre": "Esponjas de Cocina", "descripcion": "Pack 6 unidades, doble cara", "categoria": "Limpieza", "precio_compra": 1.20, "precio_venta": 2.40, "stock_actual": 90, "stock_minimo": 25, "proveedor": "Distribuidora Hogar"},
    {"sku": "SKU-LIM-004", "nombre": "Papel Higiénico 12 rollos", "descripcion": "Doble hoja, 30m c/u", "categoria": "Limpieza", "precio_compra": 4.00, "precio_venta": 8.90, "stock_actual": 55, "stock_minimo": 15, "proveedor": "Papelera Nacional"},
    {"sku": "SKU-LIM-005", "nombre": "Bolsas de Basura 50L", "descripcion": "Pack 30 unidades, extra resistentes", "categoria": "Limpieza", "precio_compra": 3.00, "precio_venta": 5.90, "stock_actual": 40, "stock_minimo": 12, "proveedor": "Distribuidora Hogar"},

    # Alimentos (5 productos)
    {"sku": "SKU-ALI-001", "nombre": "Café Molido 500g", "descripcion": "Tueste medio premium, arabica", "categoria": "Alimentos", "precio_compra": 5.60, "precio_venta": 8.90, "stock_actual": 5, "stock_minimo": 10, "proveedor": "Café Andino"},
    {"sku": "SKU-ALI-002", "nombre": "Galletas Integrales 12u", "descripcion": "Bajo azúcar, alto en fibra", "categoria": "Alimentos", "precio_compra": 1.10, "precio_venta": 1.90, "stock_actual": 90, "stock_minimo": 25, "proveedor": "Snacks del Valle"},
    {"sku": "SKU-ALI-003", "nombre": "Aceite Vegetal 1L", "descripcion": "Aceite de girasol, primera presión", "categoria": "Alimentos", "precio_compra": 3.20, "precio_venta": 5.50, "stock_actual": 75, "stock_minimo": 20, "proveedor": "Granos del Norte"},
    {"sku": "SKU-ALI-004", "nombre": "Arroz Extra 5kg", "descripcion": "Grano largo, libre de impurezas", "categoria": "Alimentos", "precio_compra": 8.00, "precio_venta": 14.90, "stock_actual": 50, "stock_minimo": 15, "proveedor": "Granos del Norte"},
    {"sku": "SKU-ALI-005", "nombre": "Leche Evaporada 400g", "descripcion": "Vitaminas A, D y calcio", "categoria": "Alimentos", "precio_compra": 2.80, "precio_venta": 4.50, "stock_actual": 85, "stock_minimo": 25, "proveedor": "Lácteos del Sur"},

    # Hogar (5 productos)
    {"sku": "SKU-HOG-001", "nombre": "Foco LED 9W", "descripcion": "Luz blanca 6500K, ahorro energético", "categoria": "Hogar", "precio_compra": 1.00, "precio_venta": 1.80, "stock_actual": 150, "stock_minimo": 40, "proveedor": "Electro Hogar"},
    {"sku": "SKU-HOG-002", "nombre": "Organizador Plástico", "descripcion": "Caja apilable 20L con tapa", "categoria": "Hogar", "precio_compra": 4.50, "precio_venta": 7.90, "stock_actual": 24, "stock_minimo": 8, "proveedor": "Home Storage Perú"},
    {"sku": "SKU-HOG-003", "nombre": "Almohada Viscoelástica", "descripcion": "Memory foam, funda lavable", "categoria": "Hogar", "precio_compra": 15.00, "precio_venta": 29.90, "stock_actual": 18, "stock_minimo": 5, "proveedor": "Comfort Dreams"},
    {"sku": "SKU-HOG-004", "nombre": "Cortinas Blackout", "descripcion": "Bloquea 100% luz, 140x220cm", "categoria": "Hogar", "precio_compra": 22.00, "precio_venta": 39.90, "stock_actual": 0, "stock_minimo": 4, "proveedor": "Textiles Hogar"},
    {"sku": "SKU-HOG-005", "nombre": "Set Cubiertos 24 piezas", "descripcion": "Acero inoxidable, mango ergonómico", "categoria": "Hogar", "precio_compra": 12.00, "precio_venta": 22.50, "stock_actual": 28, "stock_minimo": 8, "proveedor": "Cocina Pro"},

    # Deportes (4 productos)
    {"sku": "SKU-DEP-001", "nombre": "Botella Deportiva 750ml", "descripcion": "Aluminio, tapa antiderrame", "categoria": "Deportes", "precio_compra": 5.00, "precio_venta": 9.90, "stock_actual": 42, "stock_minimo": 12, "proveedor": "SportLife Perú"},
    {"sku": "SKU-DEP-002", "nombre": "Cuerda Saltar Ajustable", "descripcion": "Rodamientos de acero, contador", "categoria": "Deportes", "precio_compra": 3.50, "precio_venta": 7.20, "stock_actual": 55, "stock_minimo": 15, "proveedor": "Fitness Gear"},
    {"sku": "SKU-DEP-003", "nombre": "Balón Fútbol Talla 5", "descripcion": "Cubierta PU, costuras reforzadas", "categoria": "Deportes", "precio_compra": 18.00, "precio_venta": 32.90, "stock_actual": 20, "stock_minimo": 6, "proveedor": "SportLife Perú"},
    {"sku": "SKU-DEP-004", "nombre": "Bandas Elásticas Set", "descripcion": "5 resistencias, incluye bolsa", "categoria": "Deportes", "precio_compra": 8.00, "precio_venta": 15.90, "stock_actual": 35, "stock_minimo": 10, "proveedor": "Fitness Gear"},

    # Salud y Belleza (4 productos)
    {"sku": "SKU-SAL-001", "nombre": "Shampoo Hidratante 400ml", "descripcion": "Aloe vera, sin parabenos", "categoria": "Salud y Belleza", "precio_compra": 4.50, "precio_venta": 8.90, "stock_actual": 38, "stock_minimo": 12, "proveedor": "Belleza Natural"},
    {"sku": "SKU-SAL-002", "nombre": "Protector Solar SPF 50", "descripcion": "Resistente al agua, 200ml", "categoria": "Salud y Belleza", "precio_compra": 8.00, "precio_venta": 15.90, "stock_actual": 25, "stock_minimo": 8, "proveedor": "Dermacare Perú"},
    {"sku": "SKU-SAL-003", "nombre": "Cepillo Dental Eléctrico", "descripcion": "3 modos, temporizador integrado", "categoria": "Salud y Belleza", "precio_compra": 15.00, "precio_venta": 28.90, "stock_actual": 3, "stock_minimo": 5, "proveedor": "DentalPro"},
    {"sku": "SKU-SAL-004", "nombre": "Alcohol en Gel 250ml", "descripcion": "70% alcohol, con glicerina", "categoria": "Salud y Belleza", "precio_compra": 1.80, "precio_venta": 3.50, "stock_actual": 100, "stock_minimo": 30, "proveedor": "Belleza Natural"},
]


def seed_database():
    """Poblar la base de datos con datos de ejemplo."""
    db = SessionLocal()
    try:
        # FORZAR RESETEO: Eliminar todos los productos existentes
        from sqlalchemy import text
        db.execute(text("DELETE FROM productos"))
        db.commit()
        print("✓ Base de datos limpiada.")

        print(f"→ Insertando {len(PRODUCTOS_SEED)} productos iniciales...")
        count = 0
        for producto_data in PRODUCTOS_SEED:
            try:
                producto = ProductoCreate(**producto_data)
                crud.create_producto(db, producto)
                count += 1
            except Exception as e:
                print(f"  ✗ Error insertando {producto_data['sku']}: {e}")

        print(f"✓ Se insertaron {count} productos exitosamente.")
        print(f"✓ Categorías: {len(set(p['categoria'] for p in PRODUCTOS_SEED))}")

    except Exception as e:
        print(f"✗ Error en seed_database: {e}")
        db.rollback()
    finally:
        db.close()


def run_migrations():
    """Ejecutar migraciones y seeding automáticamente."""
    print("=" * 50)
    print("INICIANDO MIGRACIONES Y SEEDING")
    print("=" * 50)

    # Crear tablas si no existen
    from database import engine
    from models import Base

    print("→ Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas/verificadas")

    # Seed datos
    seed_database()

    print("=" * 50)
    print("MIGRACIONES COMPLETADAS")
    print("=" * 50)


if __name__ == "__main__":
    run_migrations()
