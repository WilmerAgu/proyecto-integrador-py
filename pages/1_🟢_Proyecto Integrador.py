import random
from faker import Faker
from matplotlib import pyplot as plt
import streamlit as st 
import pandas as pd  
import firebase_admin  
from firebase_admin import credentials, firestore  
from datetime import datetime
import seaborn as sns

st.set_page_config(layout="wide")

st.subheader("Proyecto Integrador")

# Verificar si ya existe una instancia de la aplicación
if not firebase_admin._apps:  
    # Cargar las credenciales de Firebase desde los secretos de Streamlit
    firebase_credentials = st.secrets["FIREBASE_CREDENTIALS"] 
    # Convertir las credenciales a un diccionario Python
    secrets_dict = firebase_credentials.to_dict()  
    # Crear un objeto de credenciales usando el diccionario 
    cred = credentials.Certificate(secrets_dict)  
    # Inicializar la aplicación de Firebase con las credenciales
    app = firebase_admin.initialize_app(cred)
   

# Obtener el cliente de Firestore
db = firestore.client()

# Definición de las pestañas
tad_descripcion, tab_Generador, tab_datos, tab_Análisis_Exploratorio, tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Generador de datos", "Datos", "Análisis Exploratorio",  "Filtro Final Dinámico"])

#----------------------------------------------------------
# Descripción (Contenido estático)
#----------------------------------------------------------
with tad_descripcion:      
    st.markdown('''   
    ### Introducción

    -   ¿Qué es el proyecto?
                
                El proyecto es el desarrollo de una aplicación de facturación 
                y control de gastos diseñada para que el administrador de una 
                pequeña empresa gestione de manera más eficiente y organizada 
                las finanzas de la empresa, facilitando el registro de facturas 
                y gastos, así como la generación de reportes financieros.
    -   ¿Cuál es el objetivo principal?
                
                El objetivo principal del proyecto es desarrollar una herramienta 
                que permita al administrador gestionar la facturación y el control 
                de gastos de la empresa de manera organizada y precisa, mejorando 
                la eficiencia en el seguimiento financiero y reduciendo errores 
                asociados al registro manual.
    -   ¿Por qué es importante?
                
                Precisión Financiera: La automatización del registro de facturas y 
                gastos reduce la posibilidad de errores humanos, lo que se traduce 
                en una contabilidad más precisa y confiable.

                Eficiencia en la Gestión: Facilita el seguimiento y la gestión de las 
                finanzas de la empresa, permitiendo al administrador ahorrar tiempo y 
                dedicarlo a otras áreas críticas del negocio.

                Visibilidad Financiera: La generación de reportes financieros detallados 
                proporciona una visión clara del estado financiero de la empresa, lo que 
                es fundamental para la toma de decisiones estratégicas.

                Prevención de Problemas de Liquidez: Las alertas sobre pagos próximos a 
                vencer ayudan a evitar retrasos en los pagos, lo que puede prevenir 
                problemas de liquidez y mejorar las relaciones con proveedores.

                Escalabilidad: Una herramienta digital puede adaptarse a las necesidades 
                futuras de la empresa, facilitando su crecimiento y evolución sin la 
                necesidad de cambiar de sistema.

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
# Generador de datos (Aquí solo se generarán los datos si se está en la pestaña correspondiente)
#----------------------------------------------------------
with tab_Generador:
    st.write('Esta función Python genera datos ficticios de usuarios y productos y los carga en una base de datos Firestore, proporcionando una interfaz sencilla para controlar la cantidad de datos generados y visualizar los resultados.')
    # Inicializar Faker para Colombia
    fake = Faker('es_CO')

    # Lista de ciudades colombianas
    ciudades_colombianas = [
        'Bogotá', 'Medellín', 'Cali', 'Barranquilla','Manizales'
    ]
    # Lista de Productos
    categorias_productos = [
        'Celular', 'Laptop', 'Tablet', 'Audífonos', 'DDS'
    ]
    # Lista de Vendedores
    vendedores = [
        'Carlos Morales', 'Tatiana Salas', 'Camila Guzman', 'Sergio Torres',
        'Luisa Gomez', 'Daniel Salinas','Ana Florez', 'Andres Escobar', 'Juan Quiroz',
        'Marcela Ocampo'
    ]

    def generate_fake_facturas(n):
        datos_facturas = []
        for _ in range(n):
            factura = {
                'numeroFactura': f'FAC-{random.randint(1000, 9999)}-{random.randint(10000, 99999)}',
                'categorias': random.choice(categorias_productos),
                'monto': round(random.uniform(50000, 10000000), -3),
                'vendedor': random.choice(vendedores),
                'ciudad': random.choice(ciudades_colombianas),
                'cantidadProductos': random.randint(1, 10)  # Nueva columna de cantidad de productos
            }
            datos_facturas.append(factura)
        return datos_facturas


    def delete_collection(collection_name):
        docs = db.collection(collection_name).get()
        for doc in docs:
            doc.reference.delete()

    def add_data_to_firestore(collection, data):
        for item in data:
            db.collection(collection).add(item)

    num_facturas = st.number_input('Número de facturas a generar', min_value=1, max_value=100, value=50)
    if st.button('Generar y Añadir Facturas'):
            with st.spinner('Eliminando facturas existentes...'):
                delete_collection('facturas')
            with st.spinner('Generando y añadiendo nuevas facturas...'):
                datos_facturas = generate_fake_facturas(num_facturas)
                add_data_to_firestore('facturas', datos_facturas)
            st.success(f'{num_facturas} facturas añadidas a Firestore')
            st.dataframe(pd.DataFrame(datos_facturas))
            

#----------------------------------------------------------
# Datos
#----------------------------------------------------------
with tab_datos:
    st.write('Visualización de datos almacenados en Firestore.')
    tab_factura, = st.tabs(["Facturas"])

    with tab_factura:
        datos_facturas = db.collection('facturas').stream()
        factura_data = [doc.to_dict() for doc in datos_facturas]
        df_datos_facturas = pd.DataFrame(factura_data)
        column_order = ['numeroFactura', 'monto', 'categorias', 'vendedor', 'ciudad', 'cantidadProductos']
        df_datos_facturas = df_datos_facturas.reindex(columns=column_order)
        st.dataframe(df_datos_facturas)

 

#----------------------------------------------------------
# Analítica 1
#----------------------------------------------------------
with tab_Análisis_Exploratorio:
    st.title("Análisis Exploratorio")
    
    st.markdown("""
    * Muestra las primeras 5 filas del DataFrame. **(df.head())**
    * Muestra la cantidad de filas y columnas del DataFrame. **(df.shape)**
    * Muestra los tipos de datos de cada columna. **(df.dtypes)**
    * Identifica y muestra las columnas con valores nulos. **(df.isnull().sum())**
    * Muestra un resumen estadístico de las columnas numéricas. **(df.describe())**
    * Muestra una tabla con la frecuencia de valores únicos para una columna categórica seleccionada. **(df['columna_categorica'].value_counts())**
    * Otra información importante.
    """)
    
    if not df_datos_facturas.empty:
        # Mostrar las primeras 5 filas
        st.subheader("Primeras 5 filas del DataFrame")
        st.write(df_datos_facturas.head())

        # Mostrar la cantidad de filas y columnas
        st.subheader("Cantidad de filas y columnas")
        st.write(f"Filas: {df_datos_facturas.shape[0]}, Columnas: {df_datos_facturas.shape[1]}")

        # Mostrar los tipos de datos de cada columna
        st.subheader("Tipos de datos de las columnas")
        st.write(df_datos_facturas.dtypes)

        # Mostrar las columnas con valores nulos
        st.subheader("Columnas con valores nulos")
        st.write(df_datos_facturas.isnull().sum())

        # Resumen estadístico de las columnas numéricas
        st.subheader("Resumen estadístico de columnas numéricas")
        st.write(df_datos_facturas.describe())

        # Mostrar la frecuencia de valores únicos de una columna categórica
        st.subheader("Frecuencia de valores únicos en una columna categórica")
        columna_categorica = st.selectbox("Selecciona una columna categórica", df_datos_facturas.select_dtypes(include=['object']).columns)
        st.write(df_datos_facturas[columna_categorica].value_counts())

        # Otra información importante (puedes agregar más métricas o análisis)
        st.subheader("Otra información importante")
        # Ejemplo: Distribución de la columna 'monto'
        st.write(df_datos_facturas['monto'].describe())

    
#----------------------------------------------------------
# Analítica 2 con filtros dinámicos y gráficos
#----------------------------------------------------------
with tab_Filtro_Final_Dinámico:
    st.title("Filtros Dinámicos con Gráficas")
    
    if not df_datos_facturas.empty:
        # Filtros dinámicos: Productos por Vendedor
        st.subheader("Cantidad de productos vendidos por Vendedor")
        vendedor_filtro = st.selectbox("Selecciona un vendedor", df_datos_facturas['vendedor'].unique())
        df_vendedor = df_datos_facturas[df_datos_facturas['vendedor'] == vendedor_filtro]
        st.write(f"Cantidad de productos vendidos por {vendedor_filtro}:")
        
        # Mostrar tabla de productos vendidos por vendedor
        st.write(df_vendedor.groupby("categorias")["cantidadProductos"].sum().reset_index())

        # Mostrar gráfico de barras
        st.subheader(f"Gráfico de productos vendidos por {vendedor_filtro}")
        plt.figure(figsize=(8, 6))
        sns.barplot(x='categorias', y='cantidadProductos', data=df_vendedor.groupby("categorias")["cantidadProductos"].sum().reset_index())
        st.pyplot()
