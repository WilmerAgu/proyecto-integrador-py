import random
from faker import Faker
import streamlit as st 
import pandas as pd  
import firebase_admin  
from firebase_admin import credentials, firestore  

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

# Tabs para las diferentes secciones de la aplicación
tab_descripcion, tab_Generador, tab_datos, tab_Análisis_Exploratorio, tab_Filtrado_Básico, tab_Filtro_Final_Dinámico = st.tabs(["Descripción", "Generador de datos", "Datos", "Análisis Exploratorio", "Filtrado Básico", "Filtro Final Dinámico"])

#----------------------------------------------------------
# Descripción del proyecto
#----------------------------------------------------------
with tab_descripcion:      
    st.markdown('''   
    ### Introducción

    - ¿Qué es el proyecto?
    - ¿Cuál es el objetivo principal?
    - ¿Por qué es importante?

    ### Desarrollo

    - Explicación detallada del proyecto
    - Procedimiento utilizado
    - Resultados obtenidos

    ### Conclusión

    - Resumen de los resultados
    - Logros alcanzados
    - Dificultades encontradas
    - Aportes personales
    ''')

#----------------------------------------------------------
# Generador de datos
#----------------------------------------------------------
with tab_Generador:
    st.write('Esta función genera datos ficticios de usuarios y productos y los carga en una base de datos Firestore, proporcionando una interfaz sencilla para controlar la cantidad de datos generados y visualizar los resultados.')
    
    # Inicializar Faker para Colombia
    fake = Faker('es_CO')

    # Lista de ciudades colombianas
    ciudades_colombianas = [
        'Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena', 
        'Cúcuta', 'Bucaramanga', 'Pereira', 'Santa Marta', 'Ibagué',
        'Pasto', 'Manizales', 'Neiva', 'Villavicencio', 'Armenia'
    ]

    # Función para generar usuarios ficticios
    def generate_fake_users(n):
        users = []
        for _ in range(n):
            user = {
                'nombre': fake.name(),
                'email': fake.email(),
                'edad': random.randint(18, 80),
                'ciudad': random.choice(ciudades_colombianas)
            }
            users.append(user)
        return users

    # Función para generar productos ficticios
    def generate_fake_products(n):
        categories = {
            'Electrónica': [
                'Celular', 'Portátil', 'Tablet', 'Audífonos', 'Reloj inteligente', 
                'Cámara digital', 'Parlante Bluetooth', 'Batería portátil', 
                'Monitor', 'Teclado inalámbrico'
            ],
            'Ropa': [
                'Camiseta', 'Jean', 'Vestido', 'Chaqueta', 'Zapatos', 
                'Sudadera', 'Medias', 'Ruana', 'Gorra', 'Falda'
            ],
            'Hogar': [
                'Lámpara', 'Cojín', 'Cortinas', 'Olla', 'Juego de sábanas', 
                'Toallas', 'Espejo', 'Reloj de pared', 'Tapete', 'Florero'
            ],
            'Deportes': [
                'Balón de fútbol', 'Raqueta de tenis', 'Pesas', 
                'Colchoneta de yoga', 'Bicicleta', 'Tenis para correr', 
                'Maletín deportivo', 'Termo', 'Guantes de boxeo', 'Lazo para saltar'
            ]
        }

        products = []
        for _ in range(n):
            category = random.choice(list(categories.keys()))
            product_type = random.choice(categories[category])
            
            product = {
                'nombre': product_type,
                'precio': round(random.uniform(10000, 1000000), -3),  # Precios en pesos colombianos
                'categoria': category,
                'stock': random.randint(0, 100)
            }
            products.append(product)
        return products

    # Función para eliminar una colección de Firestore
    def delete_collection(collection_name):
        docs = db.collection(collection_name).get()
        for doc in docs:
            doc.reference.delete()

    # Función para añadir datos a Firestore
    def add_data_to_firestore(collection, data):
        for item in data:
            db.collection(collection).add(item)
    
    col1, col2 = st.columns(2)

    # Generación de usuarios
    with col1:
        st.subheader('Usuarios')
        num_users = st.number_input('Número de usuarios a generar', min_value=1, max_value=100, value=10)
        if st.button('Generar y Añadir Usuarios'):
            with st.spinner('Eliminando usuarios existentes...'):
                delete_collection('usuarios')
            with st.spinner('Generando y añadiendo nuevos usuarios...'):
                users = generate_fake_users(num_users)
                add_data_to_firestore('usuarios', users)
            st.success(f'{num_users} usuarios añadidos a Firestore')
            st.dataframe(pd.DataFrame(users))

    # Generación de productos
    with col2:
        st.subheader('Productos')
        num_products = st.number_input('Número de productos a generar', min_value=1, max_value=100, value=10)
        if st.button('Generar y Añadir Productos'):
            with st.spinner('Eliminando productos existentes...'):
                delete_collection('productos')
            with st.spinner('Generando y añadiendo nuevos productos...'):
                products = generate_fake_products(num_products)
                add_data_to_firestore('productos', products)
            st.success(f'{num_products} productos añadidos a Firestore')
            st.dataframe(pd.DataFrame(products))

#----------------------------------------------------------
# Mostrar Datos
#----------------------------------------------------------
with tab_datos:
    st.write('Esta función muestra datos de usuarios y productos almacenados en una base de datos Firestore.')
    tab_user, tab_productos = st.tabs(["Usuarios", "Productos"])
    
    # Mostrar usuarios almacenados en Firestore
    with tab_user:
        users = db.collection('usuarios').stream()
        users_data = [doc.to_dict() for doc in users]
        df_users = pd.DataFrame(users_data)
        df_users = df_users.reindex(columns=['nombre', 'email', 'edad', 'ciudad'])   
        st.dataframe(df_users)

    # Mostrar productos almacenados en Firestore
    with tab_productos:
        products = db.collection('productos').stream()
        products_data = [doc.to_dict() for doc in products]
        df_products = pd.DataFrame(products_data)
        df_products = df_products.reindex(columns=['nombre', 'categoria', 'precio', 'stock'])
        st.dataframe(df_products)

#----------------------------------------------------------
# Análisis Exploratorio de Datos
#----------------------------------------------------------
with tab_Análisis_Exploratorio:
    st.title("Análisis Exploratorio")

    # Suponiendo que 'df_users' es el DataFrame que quieres analizar
    df = df_users  # Cambia esto a df_products si prefieres analizar productos

    # Mostrar las primeras 5 filas del DataFrame
    st.subheader("Primeras 5 filas del DataFrame")
    st.write(df.head())

    # Mostrar la cantidad de filas y columnas
    st.subheader("Cantidad de filas y columnas")
    st.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

    # Mostrar los tipos de datos de cada columna
    st.subheader("Tipos de datos por columna")
    st.write(df.dtypes)

    # Mostrar las columnas con valores nulos
    st.subheader("Valores nulos por columna")
    st.write(df.isnull().sum())

    # Mostrar un resumen estadístico de las columnas numéricas
    st.subheader("Resumen estadístico de columnas numéricas")
    st.write(df.describe())

    # Mostrar la frecuencia de valores únicos en la columna 'ciudad'
    st.subheader("Frecuencia de valores únicos en la columna 'ciudad'")
    if 'ciudad' in df.columns:
        st.write(df['ciudad'].value_counts())
    else:
        st.write("La columna 'ciudad' no existe en el DataFrame.")

#----------------------------------------------------------
# Filtrado Básico
#----------------------------------------------------------
with tab_Filtrado_Básico:
    st.title("Filtrado Básico")
    
    st.markdown("""
        Esta sección permite filtrar datos básicos en el DataFrame de usuarios.
        Puedes elegir los filtros por ciudad, edad mínima y edad máxima.
    """)

    # Filtro por ciudad
    ciudades = df_users['ciudad'].unique()
    ciudad_seleccionada = st.selectbox("Selecciona una ciudad para filtrar", ciudades, key="ciudad_filtrado_basico")

    # Filtro por edad
    edad_min = st.slider("Edad mínima", min_value=int(df_users['edad'].min()), max_value=int(df_users['edad'].max()), value=int(df_users['edad'].min()), key="edad_min_filtrado_basico")
    edad_max = st.slider("Edad máxima", min_value=int(df_users['edad'].min()), max_value=int(df_users['edad'].max()), value=int(df_users['edad'].max()), key="edad_max_filtrado_basico")

    # Aplicar filtro
    df_filtrado_basico = df_users[(df_users['ciudad'] == ciudad_seleccionada) & (df_users['edad'] >= edad_min) & (df_users['edad'] <= edad_max)]

    # Mostrar resultados del filtro
    st.subheader(f"Usuarios filtrados por ciudad: {ciudad_seleccionada}, Edad: {edad_min}-{edad_max}")
    st.dataframe(df_filtrado_basico)

#----------------------------------------------------------
# Filtro Final Dinámico
#----------------------------------------------------------
with tab_Filtro_Final_Dinámico:
    st.title("Filtro Final Dinámico")
    st.markdown("""
        * Muestra un resumen dinámico del DataFrame filtrado. 
        * Incluye información como los criterios de filtrado aplicados, la tabla de datos filtrados, gráficos y estadísticas relevantes.
        * Se actualiza automáticamente cada vez que se realiza un filtro en las pestañas anteriores. 
    """)

    df = df_users  # Asumiendo que estás trabajando con el DataFrame de usuarios

    # Filtro dinámico por ciudad
    ciudades = df['ciudad'].unique()
    ciudad_seleccionada_dinamico = st.selectbox("Selecciona una ciudad para filtrar", ciudades, key="ciudad_filtrado_dinamico")

    # Aplicar filtro
    df_filtrado = df[df['ciudad'] == ciudad_seleccionada_dinamico]

    # Mostrar tabla filtrada
    st.subheader(f"Datos filtrados por ciudad: {ciudad_seleccionada_dinamico}")
    st.dataframe(df_filtrado)

    # Estadísticas del DataFrame filtrado
    st.subheader("Estadísticas del DataFrame filtrado")
    st.write(df_filtrado.describe())

    # Gráfico de edades
    st.subheader("Distribución de edades")
    st.bar_chart(df_filtrado['edad'].value_counts())

