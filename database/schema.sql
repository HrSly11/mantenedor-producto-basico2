-- Manual: crear BD y conectar antes de ejecutar el resto (psql):
-- CREATE DATABASE product_db;
-- \c product_db

-- Tabla principal (compatible con init de Docker si POSTGRES_DB=product_db)
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(100) NOT NULL,
    precio_compra DOUBLE PRECISION NOT NULL,
    precio_venta DOUBLE PRECISION NOT NULL,
    stock_actual INTEGER NOT NULL CHECK (stock_actual >= 0),
    stock_minimo INTEGER NOT NULL CHECK (stock_minimo >= 0),
    proveedor VARCHAR(200),
    fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    fecha_ultima_actualizacion TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_productos_sku ON productos (sku);
CREATE INDEX IF NOT EXISTS idx_productos_nombre ON productos (nombre);
CREATE INDEX IF NOT EXISTS idx_productos_categoria ON productos (categoria);

-- Datos semilla ampliados con múltiples categorías y productos variados
INSERT INTO productos (
    sku, nombre, descripcion, categoria, precio_compra, precio_venta,
    stock_actual, stock_minimo, proveedor
) VALUES
    -- Tecnología (6 productos)
    ('SKU-TEC-001', 'Mouse Inalámbrico Pro', 'Mouse ergonómico 2.4GHz con 5 botones programables', 'Tecnología', 12.50, 19.90, 40, 8, 'Tech Import SAC'),
    ('SKU-TEC-002', 'Teclado Mecánico TKL', 'Switches rojos, retroiluminado RGB', 'Tecnología', 35.00, 59.90, 18, 5, 'Tech Import SAC'),
    ('SKU-TEC-003', 'Monitor 24" Full HD', 'IPS 75Hz, bordes ultrafinos', 'Tecnología', 120.00, 189.90, 12, 3, 'DisplayCorp Perú'),
    ('SKU-TEC-004', 'Webcam HD 1080p', 'Micrófono integrado, autoenfoque', 'Tecnología', 25.00, 45.90, 30, 8, 'Tech Import SAC'),
    ('SKU-TEC-005', 'Hub USB-C 7 en 1', 'HDMI 4K, USB 3.0, lector SD', 'Tecnología', 18.00, 32.50, 45, 12, 'Accesorios Tech'),
    ('SKU-TEC-006', 'Auriculares Bluetooth', 'Cancelación de ruido, 30h batería', 'Tecnología', 45.00, 79.90, 22, 6, 'AudioMax Perú'),

    -- Oficina (5 productos)
    ('SKU-OFI-001', 'Cuaderno Ejecutivo A5', '80 hojas rayadas, tapa dura', 'Oficina', 2.20, 4.50, 120, 30, 'Papelería Central'),
    ('SKU-OFI-002', 'Resma Papel A4 500h', 'Papel multiuso 75g/m²', 'Oficina', 3.50, 6.90, 200, 50, 'Papelería Central'),
    ('SKU-OFI-003', 'Grapadora Industrial', 'Capacidad 40 hojas, metálica', 'Oficina', 8.00, 15.90, 35, 10, 'Office Supply SAC'),
    ('SKU-OFI-004', 'Porta Documentos A4', 'Plástico transparente, pack 10', 'Oficina', 1.50, 3.20, 80, 20, 'Papelería Central'),
    ('SKU-OFI-005', 'Marcadores Permanentes', 'Pack 12 colores surtidos', 'Oficina', 4.00, 8.50, 60, 15, 'Arte y Oficina'),

    -- Limpieza (5 productos)
    ('SKU-LIM-001', 'Detergente Multiusos 1L', 'Limpieza de superficies, aroma limón', 'Limpieza', 1.80, 3.20, 65, 20, 'Distribuidora Hogar'),
    ('SKU-LIM-002', 'Desinfectante Spray 500ml', 'Elimina 99.9% de bacterias', 'Limpieza', 2.50, 4.50, 48, 15, 'Química Hogar'),
    ('SKU-LIM-003', 'Esponjas de Cocina', 'Pack 6 unidades, doble cara', 'Limpieza', 1.20, 2.40, 90, 25, 'Distribuidora Hogar'),
    ('SKU-LIM-004', 'Papel Higiénico 12 rollos', 'Doble hoja, 30m c/u', 'Limpieza', 4.00, 8.90, 55, 15, 'Papelera Nacional'),
    ('SKU-LIM-005', 'Bolsas de Basura 50L', 'Pack 30 unidades, extra resistentes', 'Limpieza', 3.00, 5.90, 40, 12, 'Distribuidora Hogar'),

    -- Alimentos (5 productos)
    ('SKU-ALI-001', 'Café Molido 500g', 'Tueste medio premium, arabica', 'Alimentos', 5.60, 8.90, 32, 10, 'Café Andino'),
    ('SKU-ALI-002', 'Galletas Integrales 12u', 'Bajo azúcar, alto en fibra', 'Alimentos', 1.10, 1.90, 90, 25, 'Snacks del Valle'),
    ('SKU-ALI-003', 'Aceite Vegetal 1L', 'Aceite de girasol, primera presión', 'Alimentos', 3.20, 5.50, 75, 20, 'Granos del Norte'),
    ('SKU-ALI-004', 'Arroz Extra 5kg', 'Grano largo, libre de impurezas', 'Alimentos', 8.00, 14.90, 50, 15, 'Granos del Norte'),
    ('SKU-ALI-005', 'Leche Evaporada 400g', 'Vitaminas A, D y calcio', 'Alimentos', 2.80, 4.50, 85, 25, 'Lácteos del Sur'),

    -- Hogar (5 productos)
    ('SKU-HOG-001', 'Foco LED 9W', 'Luz blanca 6500K, ahorro energético', 'Hogar', 1.00, 1.80, 150, 40, 'Electro Hogar'),
    ('SKU-HOG-002', 'Organizador Plástico', 'Caja apilable 20L con tapa', 'Hogar', 4.50, 7.90, 24, 8, 'Home Storage Perú'),
    ('SKU-HOG-003', 'Almohada Viscoelástica', 'Memory foam, funda lavable', 'Hogar', 15.00, 29.90, 18, 5, 'Comfort Dreams'),
    ('SKU-HOG-004', 'Cortinas Blackout', 'Bloquea 100% luz, 140x220cm', 'Hogar', 22.00, 39.90, 12, 4, 'Textiles Hogar'),
    ('SKU-HOG-005', 'Set Cubiertos 24 piezas', 'Acero inoxidable, mango ergonómico', 'Hogar', 12.00, 22.50, 28, 8, 'Cocina Pro'),

    -- Deportes (4 productos - nueva categoría)
    ('SKU-DEP-001', 'Botella Deportiva 750ml', 'Aluminio, tapa antiderrame', 'Deportes', 5.00, 9.90, 42, 12, 'SportLife Perú'),
    ('SKU-DEP-002', 'Cuerda Saltar Ajustable', 'Rodamientos de acero, contador', 'Deportes', 3.50, 7.20, 55, 15, 'Fitness Gear'),
    ('SKU-DEP-003', 'Balón Fútbol Talla 5', 'Cubierta PU, costuras reforzadas', 'Deportes', 18.00, 32.90, 20, 6, 'SportLife Perú'),
    ('SKU-DEP-004', 'Bandas Elásticas Set', '5 resistencias, incluye bolsa', 'Deportes', 8.00, 15.90, 35, 10, 'Fitness Gear'),

    -- Salud y Belleza (4 productos - nueva categoría)
    ('SKU-SAL-001', 'Shampoo Hidratante 400ml', 'Aloe vera, sin parabenos', 'Salud y Belleza', 4.50, 8.90, 38, 12, 'Belleza Natural'),
    ('SKU-SAL-002', 'Protector Solar SPF 50', 'Resistente al agua, 200ml', 'Salud y Belleza', 8.00, 15.90, 25, 8, 'Dermacare Perú'),
    ('SKU-SAL-003', 'Cepillo Dental Eléctrico', '3 modos, temporizador integrado', 'Salud y Belleza', 15.00, 28.90, 15, 5, 'DentalPro'),
    ('SKU-SAL-004', 'Alcohol en Gel 250ml', '70% alcohol, con glicerina', 'Salud y Belleza', 1.80, 3.50, 100, 30, 'Belleza Natural')
ON CONFLICT (sku) DO NOTHING;
