"""SQLite storage and reporting queries."""
from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = Path(__file__).resolve().parent / 'data' / 'ventas.db'


def connect(db_path=DB_PATH):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)


def initialize(db_path=DB_PATH):
    with connect(db_path) as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                producto TEXT NOT NULL,
                categoria TEXT NOT NULL,
                region TEXT NOT NULL,
                canal TEXT NOT NULL,
                cantidad INTEGER NOT NULL CHECK(cantidad > 0),
                precio_unitario REAL NOT NULL CHECK(precio_unitario >= 0),
                costo_unitario REAL NOT NULL CHECK(costo_unitario >= 0)
            );
            CREATE INDEX IF NOT EXISTS idx_ventas_fecha ON ventas(fecha);
            CREATE INDEX IF NOT EXISTS idx_ventas_categoria ON ventas(categoria);
        ''')


def count_sales(db_path=DB_PATH):
    initialize(db_path)
    with connect(db_path) as conn:
        return conn.execute('SELECT COUNT(*) FROM ventas').fetchone()[0]


def get_sales(db_path=DB_PATH):
    initialize(db_path)
    query = '''
        SELECT id, fecha, producto, categoria, region, canal, cantidad,
               precio_unitario, costo_unitario,
               ROUND(cantidad * precio_unitario, 2) AS ingresos,
               ROUND(cantidad * costo_unitario, 2) AS costos,
               ROUND(cantidad * (precio_unitario - costo_unitario), 2) AS beneficio
        FROM ventas ORDER BY fecha, id
    '''
    with connect(db_path) as conn:
        df = pd.read_sql_query(query, conn, parse_dates=['fecha'])
    return df
