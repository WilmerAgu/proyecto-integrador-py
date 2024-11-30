import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Configuración de la página
st.set_page_config(layout="wide")

st.subheader("Análisis y Filtrado de Datos del Metro de Medellín")

# Leer el archivo CSV
try:
    df = pd.read_csv('static/datasets/Afluencia_2023.csv')
    st.success("Datos cargados correctamente.")
except FileNotFoundError:
    st.error("El archivo 'Afluencia_2023.csv' no se encontró. Verifica la ruta y vuelve a intentarlo.")
    st.stop()

# Validar si el DataFrame tiene datos
if df.empty:
    st.error("El archivo cargado no contiene datos.")
    st.stop()

# Tabs para la navegación
tab_descripcion, tab_analisis, tab_filtro = st.tabs(["Descripción", "Análisis Exploratorio", "Filtro Dinámico"])

# ----------------------------------------------------------
# Descripción de los datos
# ----------------------------------------------------------
with tab_descripcion:
    st.markdown("""
    ## Plantilla Básica para Proyecto Integrador
    Este archivo contiene datos sobre la afluencia de personas en el Sistema Metro de Medellín durante 2023.
    """)
    
    # Mostrar la hora actual
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"**Hora actual:** {current_time}")
    
    # Mostrar las primeras filas del DataFrame
    st.write("**Vista previa de los datos:**")
    st.dataframe(df.head())

# ----------------------------------------------------------
# Análisis Exploratorio
# ----------------------------------------------------------
with tab_analisis:
    st.title("Análisis Exploratorio")

    # Mostrar información general
    st.markdown("### Información general del DataFrame")
    st.write(f"El DataFrame tiene **{df.shape[0]} filas** y **{df.shape[1]} columnas**.")
    st.write("**Tipos de datos:**")
    st.dataframe(df.dtypes)

    # Identificar valores nulos
    st.markdown("### Valores nulos en las columnas")
    st.dataframe(df.isnull().sum(), height=150)

    # Resumen estadístico
    st.markdown("### Resumen estadístico de las columnas numéricas")
    st.dataframe(df.describe())

    # Gráfico de barras basado en las columnas relevantes
    if 'Línea de Servicio' in df.columns and 'Afluencia' in df.columns:
        afluencia_por_linea = df.groupby('Línea de Servicio')['Afluencia'].sum()
        fig, ax = plt.subplots(figsize=(10, 6))
        afluencia_por_linea.plot(kind='bar', ax=ax, color='blue')  # Gráfico de barras
        ax.set_title("Afluencia de Pasajeros por Línea de Servicio")
        ax.set_xlabel("Línea de Servicio")
        ax.set_ylabel("Total de Afluencia")
        st.pyplot(fig)

# ----------------------------------------------------------
# Filtro Dinámico
# ----------------------------------------------------------
with tab_filtro:
    st.sidebar.title("Filtro Dinámico")
    st.markdown("### Filtrado por Línea de Servicio")

    if 'Línea de Servicio' in df.columns:
        # Lista de líneas de servicio
        lineas = df['Línea de Servicio'].dropna().unique()
        seleccion_linea = st.sidebar.selectbox("Selecciona una línea de servicio:", lineas)

        # Filtrar el DataFrame por la línea seleccionada
        df_filtrado = df[df['Línea de Servicio'] == seleccion_linea]
        st.write(f"**Datos filtrados para la línea:** {seleccion_linea}")
        st.dataframe(df_filtrado)

        # Gráfico de barras para la línea filtrada
        if 'Afluencia' in df_filtrado.columns:
            afluencia_por_linea_filtrada = df_filtrado.groupby('Línea de Servicio')['Afluencia'].sum()
            fig, ax = plt.subplots(figsize=(10, 6))
            afluencia_por_linea_filtrada.plot(kind='bar', ax=ax, color='green')  # Gráfico de barras
            ax.set_title(f"Afluencia de Pasajeros por Línea - {seleccion_linea}")
            ax.set_xlabel("Línea de Servicio")
            ax.set_ylabel("Total de Afluencia")
            st.pyplot(fig)
    else:
        st.warning("La columna 'Línea de Servicio' no está disponible en el DataFrame.")
