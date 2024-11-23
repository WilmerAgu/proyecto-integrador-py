import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.subheader("Análisis y Filtrado de Datos")

df = pd.read_csv('static\datasets\Afluencia_2023.csv')


tad_descripcion, tab_Análisis_Exploratorio, tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Análisis Exploratorio", "Filtro Final Dinámico"])

#----------------------------------------------------------
#Generador de datos
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

#----------------------------------------------------------
#Analítica 1
#----------------------------------------------------------
# Crear una pestaña para el análisis exploratorio
    tab_Análisis_Exploratorio = st.container()

    # Crear una pestaña para el análisis exploratorio
    tab_Análisis_Exploratorio = st.container()

   

# Crear una pestaña para el análisis exploratorio
tab_Análisis_Exploratorio = st.container()

with tab_Análisis_Exploratorio:    
    st.title("Análisis del Metro de Medellin")
    
    # Agregar texto explicativo (Markdown)
    st.markdown("## Afluecias del Metro de Medellin")

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

    except FileNotFoundError:
        st.error("El archivo 'Afluencia_2023.csv' no se encontró. Verifica la ruta y vuelve a intentarlo.")
    except Exception as e:
        st.error(f"Se produjo un error al procesar el archivo: {e}")

      
    
#----------------------------------------------------------

#Analítica 3
#----------------------------------------------------------
with tab_Filtro_Final_Dinámico:
        st.title("Filtro Final Dinámico")
        st.markdown("""
        * Muestra un resumen dinámico del DataFrame filtrado. 
        * Incluye información como los criterios de filtrado aplicados, la tabla de datos filtrados, gráficos y estadísticas relevantes.
        * Se actualiza automáticamente cada vez que se realiza un filtro en las pestañas anteriores. 
        """)

     # Cargar el archivo CSV
    
    try:
        df = pd.read_csv('static/datasets/Afluencia_2023.csv')
    except FileNotFoundError:
        st.error(f"No se encontró el archivo en la ruta: {file_path}")
        return

    # Renombrar las columnas principales
    data.columns = ['Día', 'Línea de Servicio', 'Hora de operación'] + [f'Intervalo_{i}' for i in range(3, len(data.columns) - 1)] + ['Total']

    # Limpiar el DataFrame
    data['Día'] = pd.to_datetime(data['Día'], errors='coerce')  # Convertir fechas
    data = data.dropna(subset=['Día'])  # Eliminar filas con días inválidos

    # Convertir valores de columnas numéricas (remover comas y convertir a float)
    for col in data.columns[3:]:
        data[col] = data[col].replace({',': ''}, regex=True).astype(float, errors='ignore')

    # Crear filtros dinámicos
    linea_seleccionada = st.selectbox("Selecciona una Línea de Servicio", options=data['Línea de Servicio'].unique())
    rango_fechas = st.date_input("Selecciona un rango de fechas", [data['Día'].min(), data['Día'].max()])

    # Aplicar filtros
    data_filtrada = data[
        (data['Línea de Servicio'] == linea_seleccionada) &
        (data['Día'] >= rango_fechas[0]) & 
        (data['Día'] <= rango_fechas[1])
    ]

    # Mostrar la tabla filtrada
    st.dataframe(data_filtrada)

    # Estadísticas relevantes
    st.subheader("Estadísticas")
    st.write("Total de pasajeros filtrados:", data_filtrada['Total'].sum())

    # Gráfico de pasajeros por día
    st.subheader("Gráfico de Pasajeros por Día")
    pasajeros_por_dia = data_filtrada.groupby('Día')['Total'].sum()
    fig, ax = plt.subplots()
    pasajeros_por_dia.plot(kind='bar', ax=ax)
    ax.set_title("Pasajeros por Día")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Total Pasajeros")
    st.pyplot(fig)

    




