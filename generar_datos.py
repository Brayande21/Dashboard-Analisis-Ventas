"""Create reproducible, entirely fictional sample sales."""
from datetime import date, timedelta
import random
from database import DB_PATH, connect, initialize, count_sales

PRODUCTOS = [
    ('Laptop empresarial', 'Tecnología', 39500, 29800),
    ('Monitor 24 pulgadas', 'Tecnología', 8900, 6300),
    ('Teclado inalámbrico', 'Accesorios', 1450, 790),
    ('Mouse ergonómico', 'Accesorios', 1150, 520),
    ('Silla de oficina', 'Mobiliario', 11500, 7400),
    ('Escritorio ejecutivo', 'Mobiliario', 16500, 10800),
    ('Impresora multifunción', 'Tecnología', 12900, 9100),
    ('Audífonos USB', 'Accesorios', 1850, 980),
    ('Router Wi-Fi', 'Redes', 3900, 2500),
    ('Switch 8 puertos', 'Redes', 4700, 3150),
]
REGIONES = ['Santiago', 'Santo Domingo', 'La Vega', 'Puerto Plata', 'San Francisco de Macorís']
CANALES = ['Tienda física', 'En línea', 'Venta corporativa']


def seed(db_path=DB_PATH, rows=1800, reset=False):
    initialize(db_path)
    if count_sales(db_path) and not reset:
        return 0
    rng = random.Random(2026)
    end = date(2026, 11, 1)
    start = date(2025, 1, 1)
    days = (end - start).days
    records = []
    for _ in range(rows):
        product, category, price, cost = rng.choice(PRODUCTOS)
        sold_on = start + timedelta(days=rng.randint(0, days))
        qty = rng.choices([1, 2, 3, 4, 5, 6, 8, 10], weights=[34, 25, 15, 9, 7, 5, 3, 2])[0]
        factor = rng.choice([0.90, 0.95, 1.0, 1.0, 1.0, 1.05])
        records.append((sold_on.isoformat(), product, category, rng.choice(REGIONES),
                        rng.choice(CANALES), qty, round(price * factor, 2), cost))
    with connect(db_path) as conn:
        if reset:
            conn.execute('DELETE FROM ventas')
        conn.executemany('''INSERT INTO ventas
            (fecha, producto, categoria, region, canal, cantidad, precio_unitario, costo_unitario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', records)
    return len(records)


if __name__ == '__main__':
    added = seed(reset=True)
    print(f'Base de datos generada: {added} ventas ficticias.')
