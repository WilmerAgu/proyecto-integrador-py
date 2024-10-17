import random
from faker import Faker
import streamlit as st 
import pandas as pd  
import firebase_admin  
from firebase_admin import credentials, firestore  
from datetime import datetime

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


tad_descripcion, tab_Generador, tab_datos, tab_Análisis_Exploratorio, tab_Filtrado_Básico, tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Generador de datos", "Datos", "Análisis Exploratorio", "Filtrado Básico", "Filtro Final Dinámico"])

#----------------------------------------------------------
#Generador de datos
#----------------------------------------------------------
with tad_descripcion:      

    st.markdown('''   

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
#Generador de datos
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
                # 'fecha': datetime.combine(fake.date_between(start_date='-1y', end_date='today'), datetime.min.time())  # Convertir a datetime
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

with st.container():  # Usar un contenedor que toma todo el ancho
    st.subheader('Facturas')
    num_facturas = st.number_input('Número de facturas a generar', min_value=1, max_value=100, value=10)
    if st.button('Generar y Añadir Facturas'):
        with st.spinner('Eliminando facturas existentes...'):
            delete_collection('facturas')
        with st.spinner('Generando y añadiendo nuevas facturas...'):
            datos_facturas = generate_fake_facturas(num_facturas)
            add_data_to_firestore('facturas', datos_facturas)
        st.success(f'{num_facturas} facturas añadidas a Firestore')
        st.dataframe(pd.DataFrame(datos_facturas))


#----------------------------------------------------------
#Datos
#----------------------------------------------------------
with tab_datos:
    st.write('Esta función muestra datos de usuarios y productos almacenados en una base de datos Firestore, permitiendo una visualización organizada y fácil acceso a la información.')
    
    # Cambiar aquí, desempaquetando la pestaña correctamente
    tab_factura, = st.tabs(["Facturas"])  # Nota el uso de la coma para desempaquetar una sola pestaña

    with tab_factura:
        # Obtener datos de una colección de Firestore
        datos_facturas = db.collection('facturas').stream()
        # Convertir datos a una lista de diccionarios
        factura_data = [doc.to_dict() for doc in datos_facturas]
        # Crear DataFrame
        df_datos_facturas = pd.DataFrame(factura_data)
        # Reordenar las columnas
        column_order = ['numeroFactura', 'monto', 'categorias', 'vendedor', 'ciudad', ]
        df_datos_facturas = df_datos_facturas.reindex(columns=column_order)   

        st.dataframe(df_datos_facturas)

#----------------------------------------------------------
#Analítica 1
#----------------------------------------------------------
with tab_Análisis_Exploratorio:    
    st.title("Análisis Exploratorio")
    st.markdown("""
    * Muestra las primeras 5 filas del DataFrame.  **(df.head())**
                
    * Muestra la cantidad de filas y columnas del DataFrame.  **(df.shape)**
    * Muestra los tipos de datos de cada columna.  **(df.dtypes)**
    * Identifica y muestra las columnas con valores nulos. **(df.isnull().sum())**
    * Muestra un resumen estadístico de las columnas numéricas.  **(df.describe())**
    * Muestra una tabla con la frecuencia de valores únicos para una columna categórica seleccionada. **(df['columna_categorica'].value_counts())** 
    * Otra información importante  
    """)
    
#----------------------------------------------------------
#Analítica 2
#----------------------------------------------------------
with tab_Filtrado_Básico:
        st.title("Filtro Básico")
        st.markdown("""
        * Permite filtrar datos usando condiciones simples. **(df[df['columna'] == 'valor'])**
        * Permite seleccionar una columna y un valor para el filtro. **(st.selectbox, st.text_input)**
        * Permite elegir un operador de comparación (igual, diferente, mayor que, menor que). **(st.radio)**
        * Muestra los datos filtrados en una tabla. **(st.dataframe)** 
        """)

#----------------------------------------------------------
#Analítica 2
#----------------------------------------------------------
with tab_Filtro_Final_Dinámico:
        st.title("Filtro Final Dinámico")
        st.markdown("""
        * Muestra un resumen dinámico del DataFrame filtrado. 
        * Incluye información como los criterios de filtrado aplicados, la tabla de datos filtrados, gráficos y estadísticas relevantes.
        * Se actualiza automáticamente cada vez que se realiza un filtro en las pestañas anteriores. 
        """)


