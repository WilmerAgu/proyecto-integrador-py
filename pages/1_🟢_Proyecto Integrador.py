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
#Datos
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

 # Gráfica de Productos Vendidos por Vendedor
if not df_datos_facturas.empty:
    # Agrupar por vendedor y calcular la cantidad total de productos vendidos
    productos_por_vendedor = df_datos_facturas.groupby('vendedor').agg({
        'cantidadProductos': 'sum'
    }).reset_index()

    # Crear el gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='vendedor', y='cantidadProductos', data=productos_por_vendedor, palette='viridis', ax=ax)
    
    # Configurar etiquetas y título
    ax.set_xlabel('Vendedor')
    ax.set_ylabel('Cantidad de Unidades Vendidas')
    ax.set_title('Cantidad de Unidades')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

    # Agregar etiquetas en la parte superior de cada barra para mostrar la cantidad exacta
    for index, row in productos_por_vendedor.iterrows():
        ax.text(index, row['cantidadProductos'], int(row['cantidadProductos']), color='black', ha="center")

    plt.tight_layout()

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
    plt.close(fig)

# Agrupar por categoría de producto y sumar la cantidad de productos vendidos
productos_vendidos = df_datos_facturas.groupby('categorias').agg({
    'cantidadProductos': 'sum'
}).reset_index()

# Ordenar los productos de mayor a menor cantidad vendida
productos_vendidos = productos_vendidos.sort_values('cantidadProductos', ascending=False)

# Configurar el tamaño de la figura
f, ax = plt.subplots(figsize=(8, 6))

# Gráfico de barras horizontales para mostrar los productos más vendidos
sns.set_color_codes("pastel")
sns.barplot(x="cantidadProductos", y="categorias", data=productos_vendidos, color="b")

# Añadir etiquetas y título
ax.set(xlabel="Cantidad de Productos Vendidos", ylabel="Productos", title="Productos Más Vendidos")
sns.despine(left=True, bottom=True)

# Mostrar el gráfico en Streamlit
st.pyplot(f)
plt.close(f)


# Gráfica de Dona para Productos Vendidos por Ciudad
if not df_datos_facturas.empty:
    # Agrupar por ciudad y calcular la cantidad total de productos vendidos
    productos_por_ciudad = df_datos_facturas.groupby('ciudad').agg({
        'cantidadProductos': 'sum'
    }).reset_index()

    # Ordenar por la cantidad de productos vendidos en orden descendente
    productos_por_ciudad = productos_por_ciudad.sort_values(by='cantidadProductos', ascending=False)

    # Crear el gráfico de dona
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        productos_por_ciudad['cantidadProductos'], 
        labels=productos_por_ciudad['ciudad'], 
        autopct='%1.1f%%', 
        startangle=90, 
        wedgeprops={'width': 0.3},  # Esto crea el efecto de dona
        colors=sns.color_palette("pastel", len(productos_por_ciudad)),  # Paleta de colores clara
        pctdistance=0.85  # Controla la distancia de los porcentajes respecto al centro
    )

    # Configurar el estilo de los porcentajes para que sean más grandes y visibles
    plt.setp(autotexts, size=12, weight="bold", color="black")

    # Título del gráfico
    ax.set_title('Distribución de Unidades Vendidas por Ciudad')

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
    plt.close(fig)

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
with tab_Filtro_Final_Dinámico:
        st.title("Filtro Final Dinámico")
        st.markdown("""
        * Muestra un resumen dinámico del DataFrame filtrado. 
        * Incluye información como los criterios de filtrado aplicados, la tabla de datos filtrados, gráficos y estadísticas relevantes.
        * Se actualiza automáticamente cada vez que se realiza un filtro en las pestañas anteriores. 
        """)


