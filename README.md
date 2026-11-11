# 📊 Dashboard de Análisis de Ventas

Aplicación web interactiva para explorar ventas ficticias de una empresa comercial en República Dominicana. Proyecto de portafolio de análisis de datos con **Python, Pandas, SQLite, SQL, Streamlit y Plotly**.

## Funcionalidades

- Cinco KPI: ingresos, beneficio bruto, margen bruto, transacciones y unidades vendidas.
- Gráfico de evolución mensual de ingresos y beneficio.
- Distribución por categoría, ranking de productos y ventas por región.
- Resumen de canales de venta.
- Filtros por rango de fechas, categoría, región y canal.
- Tabla de transacciones y exportación CSV de los resultados filtrados.
- Base de datos SQLite con **1,800 registros ficticios reproducibles**, creada automáticamente al iniciar por primera vez.

## Requisitos

- Python 3.10 o superior.
- Conexión a internet solo para instalar las dependencias por primera vez.

## Instalación en Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Se abrirá el navegador en `http://localhost:8501`. Para detener la aplicación, pulsa `Ctrl+C` en la terminal.

Si `python` no funciona, prueba `py` en el primer comando y usa después los comandos que comienzan por `.\.venv\Scripts\python.exe`.

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

## Estructura

```text
Dashboard-Analisis-Ventas/
├── app.py                # Interfaz y visualizaciones
├── database.py           # Esquema y consulta SQL
├── generar_datos.py      # Datos de ejemplo reproducibles
├── requirements.txt      # Dependencias
├── .gitignore            # Excluye bases de datos locales y entorno virtual
├── .streamlit/config.toml
├── data/                 # SQLite se crea aquí al iniciar
└── tests/test_database.py
```

## SQL utilizado

Los importes se calculan directamente desde SQLite:

```sql
SELECT fecha, producto, categoria, cantidad,
       cantidad * precio_unitario AS ingresos,
       cantidad * (precio_unitario - costo_unitario) AS beneficio
FROM ventas;
```

Pandas agrega los datos filtrados y Plotly genera los gráficos.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Reiniciar los datos de ejemplo

```powershell
.\.venv\Scripts\python.exe generar_datos.py
```

Este comando reemplaza las ventas existentes con los datos ficticios iniciales. **No lo ejecutes si agregaste información que deseas conservar.**
<img width="1913" height="907" alt="image" src="https://github.com/user-attachments/assets/17de6df1-4729-40ec-8174-58b9a95316a9" />
<img width="1920" height="904" alt="image" src="https://github.com/user-attachments/assets/ac628436-4647-45be-a84f-3cc2e638e7ec" />

## Aviso

Los datos, nombres de productos, importes y regiones de este ejemplo son **simulados**; no corresponden a ventas reales. La aplicación es demostrativa y no incluye autenticación ni controles de acceso para un entorno de producción.

## Autor

Brayan · [GitHub](https://github.com/Brayande21)
