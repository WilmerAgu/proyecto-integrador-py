import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

st.set_page_config(layout="wide")

st.subheader("Análisis y Filtrado de Datos")

df = pd.read_csv('static/datasets/Afluencia_2023.csv')

tad_descripcion, tab_Análisis_Exploratorio, tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Análisis Exploratorio", "Filtro Final Dinámico"])

#----------------------------------------------------------
# Generador de datos
#----------------------------------------------------------
with tad_descripcion:      

    st.markdown('''
    ## Plantilla Básica para Proyecto Integrador

    El archivo contiene datos sobre la afluencia de personas en el Sistema de Metro de Medellín durante el año 2023. 
    Este conjunto de datos presenta información detallada sobre los momentos de mayor afluencia de pasajeros, organizados por horas a lo largo del día. Además, incluye detalles relacionados con las líneas de autobuses que complementan el servicio del metro.

    Específicamente, cada registro en la tabla indica:

    Hora de subida: El horario específico en el que los usuarios abordaron el metro.
    Líneas de autobuses: Las rutas de transporte público (buses) que operan en conjunto con el metro y que pueden estar relacionadas con los patrones de afluencia de los usuarios.
    Este archivo permite analizar los patrones de movilidad de las personas en el sistema de transporte público de la ciudad, proporcionando datos útiles para la planificación y optimización del servicio tanto para el metro como para las líneas de autobuses. La información puede ser empleada para identificar los momentos de mayor demanda de transporte y para coordinar mejor las conexiones entre el metro y los autobuses.
    ''')

    # Mostrar la hora actual
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"Hora actual: {current_time}")

#----------------------------------------------------------
# Analítica 1
#----------------------------------------------------------
with tab_Análisis_Exploratorio:    
    st.title("Análisis del Metro de Medellin")
    
    # Agregar texto explicativo (Markdown)
    st.markdown("## Afluencias del Metro de Medellin")

    # Cargar los datos desde un archivo CSV
    try:
        df = pd.read_csv('static/datasets/Afluencia_2023.csv')
        
        # Mostrar las primeras 5 filas del DataFrame
        st.markdown("### 1. Muestra las primeras 5 filas del DataFrame")
        st.dataframe(df.head())

        # Mostrar la cantidad de filas y columnas
        st.markdown("### 2. Muestra la cantidad de filas y columnas del DataFrame")
        st.write(f"El DataFrame tiene **{df.shape[0]} filas** y **{df.shape[1]} columnas**.")

        # Mostrar los tipos de datos de cada columna
        st.markdown("### 3. Muestra los tipos de datos de cada columna")
        st.dataframe(df.dtypes)

        # Identificar y mostrar las columnas con valores nulos
        st.markdown("### 4. Identifica y muestra las columnas con valores nulos")
        st.dataframe(df.isnull().sum(), height=150)

        # Mostrar un resumen estadístico de las columnas numéricas
        st.markdown("### 5. Muestra un resumen estadístico de las columnas numéricas")
        st.dataframe(df.describe())

        # Mostrar una tabla con la frecuencia de valores únicos para la columna 'Línea de Servicio'
        st.markdown("### 6. Frecuencia de valores únicos en la columna 'Línea de Servicio'")
        if 'Línea de Servicio' in df.columns:
            # Mostrar la frecuencia de valores únicos
            st.dataframe(df['Línea de Servicio'].value_counts().rename("Frecuencia"))
        else:
            # Mensaje de advertencia si la columna no existe
            st.warning("La columna 'Línea de Servicio' no está en el DataFrame.")

        # Agregar gráficos adicionales
        # Gráfico de afluencia por hora
        st.markdown("### Gráfico de Afluencia por Hora")
        if 'Hora de operación' in df.columns:
            afluencia_por_hora = df.groupby('Hora de operación')['Total'].sum()
            fig, ax = plt.subplots(figsize=(10, 6))
            afluencia_por_hora.plot(kind='line', ax=ax)
            ax.set_title("Afluencia de Pasajeros por Hora")
            ax.set_xlabel("Hora")
            ax.set_ylabel("Total de Pasajeros")
            st.pyplot(fig)

        # Gráfico de distribución de la afluencia total
        st.markdown("### Gráfico de Distribución de la Afluencia Total")
        fig, ax = plt.subplots(figsize=(10, 6))
        df['Total'].plot(kind='hist', bins=20, ax=ax, alpha=0.7, color='skyblue')
        ax.set_title("Distribución de la Afluencia Total")
        ax.set_xlabel("Total de Pasajeros")
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig)

    except FileNotFoundError:
        st.error("El archivo 'Afluencia_2023.csv' no se encontró. Verifica la ruta y vuelve a intentarlo.")
    except Exception as e:
        st.error(f"Se produjo un error al procesar el archivo: {e}")


#----------------------------------------------------------
# Analítica 3
#----------------------------------------------------------
# Pestaña de Filtro Final Dinámico
    with st.sidebar:  # Cambia esta línea según cómo quieras organizar tu app
     st.title("Filtro Final Dinámico")
    st.markdown("""
        * Muestra un resumen dinámico del DataFrame filtrado. 
        * Incluye información como los criterios de filtrado aplicados, la tabla de datos filtrados, gráficos y estadísticas relevantes.
        * Se actualiza automáticamente cada vez que se realiza un filtro en las pestañas anteriores. 
        """)



