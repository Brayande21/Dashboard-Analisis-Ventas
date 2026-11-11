"""Interactive sales analytics dashboard."""
import pandas as pd
import plotly.express as px
import streamlit as st
from database import get_sales
from generar_datos import seed

st.set_page_config(page_title='Dashboard de Ventas | RD', page_icon='📊', layout='wide')

st.markdown('''<style>
.block-container {padding-top: 1.6rem; padding-bottom: 2rem;}
[data-testid="stMetric"] {background: #f4f7fc; padding: 1rem; border-radius: 12px; border: 1px solid #e5ebf4;}
[data-testid="stMetricLabel"] {color: #43546b;}
</style>''', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_data():
    return get_sales()


def money(value):
    return f'RD$ {value:,.2f}'


def main():
    seed()  # Populates only if the local database is empty.
    df = load_data()
    st.title('📊 Dashboard de Análisis de Ventas')
    st.caption('Proyecto de portafolio · Python + SQL + Pandas + Streamlit + Plotly · Datos ficticios')
    if df.empty:
        st.warning('No hay ventas para mostrar. Ejecuta: python generar_datos.py')
        return

    with st.sidebar:
        st.header('🔎 Filtros')
        min_date = df['fecha'].min().date()
        max_date = df['fecha'].max().date()
        selected = st.date_input('Período', value=(min_date, max_date), min_value=min_date, max_value=max_date)
        categories = st.multiselect('Categorías', sorted(df['categoria'].unique()), default=sorted(df['categoria'].unique()))
        regions = st.multiselect('Regiones', sorted(df['region'].unique()), default=sorted(df['region'].unique()))
        channels = st.multiselect('Canales de venta', sorted(df['canal'].unique()), default=sorted(df['canal'].unique()))
        st.divider()
        st.caption('Los filtros afectan todos los indicadores, gráficos y descargas.')

    if not isinstance(selected, (tuple, list)) or len(selected) != 2:
        st.info('Selecciona una fecha inicial y una fecha final.')
        return
    start, end = selected
    filtered = df.loc[
        df['fecha'].dt.date.between(start, end)
        & df['categoria'].isin(categories)
        & df['region'].isin(regions)
        & df['canal'].isin(channels)
    ].copy()
    if filtered.empty:
        st.warning('No hay ventas con estos filtros. Ajusta las opciones de la barra lateral.')
        return

    revenue = filtered['ingresos'].sum()
    profit = filtered['beneficio'].sum()
    margin = (profit / revenue * 100) if revenue else 0
    units = int(filtered['cantidad'].sum())
    orders = len(filtered)
    cols = st.columns(5)
    for col, label, value in zip(cols,
        ['Ingresos totales', 'Beneficio bruto', 'Margen bruto', 'Transacciones', 'Unidades vendidas'],
        [money(revenue), money(profit), f'{margin:.1f}%', f'{orders:,}', f'{units:,}']):
        col.metric(label, value)

    st.divider()
    left, right = st.columns([1.6, 1])
    monthly = filtered.assign(mes=filtered['fecha'].dt.to_period('M').dt.to_timestamp())\
        .groupby('mes', as_index=False)[['ingresos', 'beneficio']].sum()
    with left:
        st.subheader('Evolución mensual')
        fig = px.line(monthly, x='mes', y=['ingresos', 'beneficio'], markers=True,
                      labels={'mes': 'Mes', 'value': 'RD$', 'variable': 'Indicador'},
                      color_discrete_sequence=['#2563eb', '#16a34a'])
        fig.update_layout(legend_title_text='', hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader('Ingresos por categoría')
        by_cat = filtered.groupby('categoria', as_index=False)['ingresos'].sum()
        fig = px.pie(by_cat, names='categoria', values='ingresos', hole=.55,
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(legend_title_text='Categoría')
        st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader('Top 10 productos por ingresos')
        top = filtered.groupby('producto', as_index=False)['ingresos'].sum().nlargest(10, 'ingresos')
        fig = px.bar(top.sort_values('ingresos'), x='ingresos', y='producto', orientation='h',
                     labels={'ingresos': 'Ingresos (RD$)', 'producto': 'Producto'},
                     color_discrete_sequence=['#2563eb'])
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader('Ventas por región')
        by_region = filtered.groupby('region', as_index=False)['ingresos'].sum().sort_values('ingresos', ascending=False)
        fig = px.bar(by_region, x='region', y='ingresos',
                     labels={'ingresos': 'Ingresos (RD$)', 'region': 'Región'},
                     color_discrete_sequence=['#14b8a6'])
        fig.update_xaxes(tickangle=-25)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader('Canales de venta')
    by_channel = filtered.groupby('canal', as_index=False).agg(
        ingresos=('ingresos', 'sum'), transacciones=('id', 'count'), unidades=('cantidad', 'sum'))
    st.dataframe(by_channel, use_container_width=True, hide_index=True,
                 column_config={'ingresos': st.column_config.NumberColumn('Ingresos (RD$)', format='%.2f')})

    st.subheader('Detalle de transacciones')
    display = filtered.sort_values('fecha', ascending=False).copy()
    display['fecha'] = display['fecha'].dt.strftime('%Y-%m-%d')
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.download_button('⬇️ Descargar ventas filtradas (CSV)',
                       data=display.to_csv(index=False).encode('utf-8-sig'),
                       file_name='ventas_filtradas.csv', mime='text/csv')
    st.caption('Importante: las cifras son simuladas y no representan operaciones reales.')


if __name__ == '__main__':
    main()
