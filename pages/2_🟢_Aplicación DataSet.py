import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

st.set_page_config(layout="wide")

st.subheader("Análisis y Filtrado de Datos")

# Cargar los datos desde un archivo CSV
try:
    df = pd.read_csv('static/datasets/Afluencia_2023.csv')
except FileNotFoundError:
    st.error("El archivo 'Afluencia_2023.csv' no se encontró. Verifica la ruta y vuelve a intentarlo.")
    df = pd.DataFrame()  # Crear un DataFrame vacío en caso de error
except Exception as e:
    st.error(f"Se produjo un error al procesar el archivo: {e}")
    df = pd.DataFrame()

tab_descripcion, tab_analisis_exploratorio, tab_filtro_final_dinamico = st.tabs(["Descripción", "Análisis Exploratorio", "Filtro Final Dinámico"])

# ----------------------------------------------------------
# Generador de datos
# ----------------------------------------------------------
with tab_descripcion:      
    st.markdown('''
    ## Plantilla Básica para Proyecto Integrador

    El archivo contiene datos sobre la afluencia de personas en el Sistema de Metro de Medellín durante el año 2023. 
    Este conjunto de datos presenta información detallada sobre los momentos de mayor afluencia de pasajeros, organizados por horas a lo largo del día. Además, incluye detalles relacionados con las líneas de autobuses que complementan el servicio del metro.

    Específicamente, cada registro en la tabla indica:

    - **Hora de subida**: El horario específico en el que los usuarios abordaron el metro.
    - **Líneas de autobuses**: Las rutas de transporte público (buses) que operan en conjunto con el metro y que pueden estar relacionadas con los patrones de afluencia de los usuarios.

    Este archivo permite analizar los patrones de movilidad de las personas en el sistema de transporte público de la ciudad, proporcionando datos útiles para la planificación y optimización del servicio tanto para el metro como para las líneas de autobuses. La información puede ser empleada para identificar los momentos de mayor demanda de transporte y para coordinar mejor las conexiones entre el metro y los autobuses.
    ''')

    # Mostrar la hora actual
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"Hora actual: {current_time}")

# ----------------------------------------------------------
# Analítica 1
# ----------------------------------------------------------
with tab_analisis_exploratorio:    
    st.title("Análisis del Metro de Medellín")
    
    st.markdown("## Afluencias del Metro de Medellín")

    if not df.empty:
        st.markdown("### 1. Muestra las primeras 5 filas del DataFrame")
        st.dataframe(df.head())

        st.markdown("### 2. Muestra la cantidad de filas y columnas del DataFrame")
        st.write(f"El DataFrame tiene **{df.shape[0]} filas** y **{df.shape[1]} columnas**.")

        st.markdown("### 3. Identifica y muestra las columnas con valores nulos")
        st.dataframe(df.isnull().sum(), height=150)

        st.markdown("### 4. Muestra un resumen estadístico de las columnas numéricas")
        st.dataframe(df.describe())

# ----------------------------------------------------------
# Filtros Dinámicos
# ----------------------------------------------------------
with tab_filtro_final_dinamico:
    st.sidebar.title("Filtro Dinámico")
    st.markdown("### Filtrado por Línea de Servicio")

    if not df.empty and 'Línea de Servicio' in df.columns:
        # Lista de líneas de servicio
        lineas = df['Línea de Servicio'].dropna().unique()
        seleccion_linea = st.sidebar.selectbox("Selecciona una línea de servicio:", lineas)

        # Filtrar el DataFrame por la línea seleccionada
        df_filtrado = df[df['Línea de Servicio'] == seleccion_linea]
        st.write(f"*Datos filtrados para la línea:* {seleccion_linea}")
        st.dataframe(df_filtrado)

        # Gráfico de barras: Total de pasajeros por hora
        if 'Hora de operación' in df_filtrado.columns and 'Total' in df_filtrado.columns:
            st.markdown("### Total de Pasajeros por Hora de Operación")
            total_por_hora = df_filtrado.groupby('Hora de operación')['Total'].sum()
            fig, ax = plt.subplots(figsize=(10, 6))
            total_por_hora.plot(kind='bar', ax=ax, color='blue', alpha=0.7)
            ax.set_title(f"Total de Pasajeros por Hora - {seleccion_linea}")
            ax.set_xlabel("Hora de Operación")
            ax.set_ylabel("Total de Pasajeros")
            st.pyplot(fig)

        # Gráfico de barras: Afluencia por estación
        if 'Estación' in df_filtrado.columns and 'Afluencia' in df_filtrado.columns:
            st.markdown("### Afluencia por Estación")
            afluencia_por_estacion = df_filtrado.groupby('Estación')['Afluencia'].sum()
            fig, ax = plt.subplots(figsize=(10, 6))
            afluencia_por_estacion.plot(kind='bar', ax=ax, color='orange', alpha=0.8)
            ax.set_title(f"Afluencia por Estación - {seleccion_linea}")
            ax.set_xlabel("Estación")
            ax.set_ylabel("Afluencia Total")
            st.pyplot(fig)

        # Gráfico de barras: Afluencia promedio por día
        if 'Día de operación' in df_filtrado.columns and 'Afluencia' in df_filtrado.columns:
            st.markdown("### Afluencia Promedio por Día de Operación")
            afluencia_promedio_por_dia = df_filtrado.groupby('Día de operación')['Afluencia'].mean()
            fig, ax = plt.subplots(figsize=(10, 6))
            afluencia_promedio_por_dia.plot(kind='bar', ax=ax, color='green', alpha=0.6)
            ax.set_title(f"Afluencia Promedio por Día - {seleccion_linea}")
            ax.set_xlabel("Día de Operación")
            ax.set_ylabel("Afluencia Promedio")
            st.pyplot(fig)
    else:
        st.warning("La columna 'Línea de Servicio' no está disponible en el DataFrame.")
