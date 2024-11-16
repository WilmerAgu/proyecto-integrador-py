import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.subheader("Análisis y Filtrado de Datos")

df = pd.read_csv('./static/datasets/ventas.csv')


tad_descripcion, tab_Análisis_Exploratorio, tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Análisis Exploratorio", "Filtro Final Dinámico"])

#----------------------------------------------------------
#Generador de datos
#----------------------------------------------------------
with tad_descripcion:      

    st.markdown('''
    ## Plantilla Básica para Proyecto Integrador

    ### Introducción

    -   ¿Qué es el proyecto?
    -   ¿Cuál es el objetivo principal?
    -   ¿Por qué es importante?

    ### Desarrollo

    -   Explicación detallada del proyecto
    -   Procedimiento utilizado
    -   Resultados obtenidos

    ### Conclusión

    -   Resumen de los resultados
    -   Logros alcanzados
    -   Dificultades encontradas
    -   Aportes personales
    ''')

#----------------------------------------------------------
#Analítica 1
#----------------------------------------------------------
# Crear una pestaña para el análisis exploratorio
    tab_Análisis_Exploratorio = st.container()

    # Crear una pestaña para el análisis exploratorio
    tab_Análisis_Exploratorio = st.container()

    import pandas as pd
    import streamlit as st

# Crear una pestaña para el análisis exploratorio
tab_Análisis_Exploratorio = st.container()

with tab_Análisis_Exploratorio:    
    st.title("Análisis Exploratorio")
    
    # Agregar texto explicativo (Markdown)
    st.markdown("## Datos cargados y análisis descriptivo")

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



    




