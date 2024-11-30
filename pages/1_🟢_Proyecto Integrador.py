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
tab_descripcion, tab_generador, tab_datos, tab_analisis_exploratorio, tab_filtro_final_dinamico = st.tabs(
    ["Descripción", "Generador de datos", "Datos", "Análisis Exploratorio", "Filtro Final Dinámico"])

# ----------------------------------------------------------
# Descripción (Contenido estático)
# ----------------------------------------------------------
with tab_descripcion:
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
    ''')

# ----------------------------------------------------------
# Generador de datos
# ----------------------------------------------------------
with tab_generador:
    st.write('Esta función genera datos ficticios de usuarios y productos y los carga en una base de datos Firestore.')
    fake = Faker('es_CO')

    ciudades_colombianas = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Manizales']
    categorias_productos = ['Celular', 'Laptop', 'Tablet', 'Audífonos', 'SSD']
    vendedores = [
        'Carlos Morales', 'Tatiana Salas', 'Camila Guzman', 'Sergio Torres',
        'Luisa Gomez', 'Daniel Salinas', 'Ana Florez', 'Andres Escobar', 'Juan Quiroz', 'Marcela Ocampo'
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
                'cantidadProductos': random.randint(1, 10)
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

# ----------------------------------------------------------
# Datos
# ----------------------------------------------------------
with tab_datos:
    st.write('Visualización de datos almacenados en Firestore.')
    datos_facturas = db.collection('facturas').stream()
    factura_data = [doc.to_dict() for doc in datos_facturas]
    df_datos_facturas = pd.DataFrame(factura_data)
    column_order = ['numeroFactura', 'monto', 'categorias', 'vendedor', 'ciudad', 'cantidadProductos']
    df_datos_facturas = df_datos_facturas.reindex(columns=column_order)
    st.dataframe(df_datos_facturas)

# ----------------------------------------------------------
# Análisis Exploratorio
# ----------------------------------------------------------
with tab_analisis_exploratorio:
    st.title("Análisis Exploratorio")

    if not df_datos_facturas.empty:
        st.subheader("Primeras 5 filas")
        st.write(df_datos_facturas.head())

        st.subheader("Cantidad de filas y columnas")
        st.write(f"Filas: {df_datos_facturas.shape[0]}, Columnas: {df_datos_facturas.shape[1]}")

        st.subheader("Tipos de datos")
        st.write(df_datos_facturas.dtypes)

        st.subheader("Columnas con valores nulos")
        st.write(df_datos_facturas.isnull().sum())

        st.subheader("Resumen estadístico")
        st.write(df_datos_facturas.describe())

# ----------------------------------------------------------
# Filtro Final Dinámico con Detalles en Gráficas
# ----------------------------------------------------------
with tab_filtro_final_dinamico:
    st.title("Filtros Dinámicos con Gráficas")

    if not df_datos_facturas.empty:
        st.subheader("Productos vendidos por Vendedor")
        
        # Filtro para seleccionar el vendedor
        vendedor_filtro = st.selectbox("Selecciona un vendedor", df_datos_facturas['vendedor'].unique())
        df_vendedor = df_datos_facturas[df_datos_facturas['vendedor'] == vendedor_filtro]
        
        # Agrupar datos por categoría y sumar cantidad de productos
        df_categorias = df_vendedor.groupby("categorias")["cantidadProductos"].sum().reset_index()

        # Mostrar tabla con los datos agrupados
        st.write(df_categorias)

        # Filtro para seleccionar el tipo de gráfica
        tipo_grafico = st.radio("Selecciona el tipo de gráfico", ("Barra", "Pastel", "Línea"))

        st.subheader(f"Gráfico para {vendedor_filtro}")
        
        # Crear y mostrar la gráfica según el tipo seleccionado
        if tipo_grafico == "Barra":
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(
                x='categorias', 
                y='cantidadProductos', 
                data=df_categorias, 
                palette='viridis',
                ax=ax
            )
            ax.set_title(f"Productos vendidos por {vendedor_filtro}")
            ax.set_ylabel("Cantidad Exacta de Productos")
            ax.set_xlabel("Categorías de Productos")
            
            # Añadir números exactos encima de las barras
            for index, row in df_categorias.iterrows():
                ax.text(index, row['cantidadProductos'], int(row['cantidadProductos']), ha='center', va='bottom')
            st.pyplot(fig)

        elif tipo_grafico == "Pastel":
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(
                df_categorias['cantidadProductos'], 
                labels=df_categorias['categorias'], 
                autopct='%1.1f%%', 
                startangle=90,
                colors=sns.color_palette('viridis', len(df_categorias))
            )
            ax.set_title(f"Distribución de productos vendidos por {vendedor_filtro}")
            st.pyplot(fig)

        elif tipo_grafico == "Línea":
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.lineplot(
                x='categorias', 
                y='cantidadProductos', 
                data=df_categorias, 
                marker='o', 
                ax=ax
            )
            ax.set_title(f"Productos vendidos por {vendedor_filtro} (Gráfico de línea)")
            ax.set_ylabel("Cantidad Exacta de Productos")
            ax.set_xlabel("Categorías de Productos")
            st.pyplot(fig)

        # Mostrar detalles adicionales debajo de la gráfica
        st.write(f"**Vendedor**: {vendedor_filtro}")

        # Mostrar información adicional de cada compra
        st.subheader("Detalles de las compras:")
        
        # Seleccionar las columnas relevantes
        detalles = df_vendedor[['numeroFactura', 'categorias', 'ciudad', 'cantidadProductos']].copy()
        
        # Generar fechas ficticias para las compras
        detalles['fecha'] = [datetime(2024, random.randint(1, 12), random.randint(1, 28)).strftime('%Y-%m-%d') for _ in range(len(detalles))]
        
        # Agrupar por ciudad para gráfica
        df_ciudad = detalles.groupby("ciudad")["cantidadProductos"].sum().reset_index()
        st.subheader("Cantidad de productos por ciudad")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(
            x='ciudad', 
            y='cantidadProductos', 
            data=df_ciudad, 
            palette='viridis',
            ax=ax
        )
        ax.set_title("Productos vendidos por ciudad")
        ax.set_ylabel("Cantidad de Productos")
        ax.set_xlabel("Ciudades")
        st.pyplot(fig)

        # Agrupar por fecha para gráfica
        df_fecha = detalles.groupby("fecha")["cantidadProductos"].sum().reset_index()
        st.subheader("Cantidad de productos por fecha")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.lineplot(
            x='fecha', 
            y='cantidadProductos', 
            data=df_fecha, 
            marker='o', 
            ax=ax
        )
        ax.set_title("Productos vendidos por fecha")
        ax.set_ylabel("Cantidad de Productos")
        ax.set_xlabel("Fechas")
        plt.xticks(rotation=45)  # Rotar etiquetas de fechas
        st.pyplot(fig)

        # Mostrar detalles como texto debajo de las gráficas
        st.subheader("Detalles individuales de las compras:")
        for _, row in detalles.iterrows():
            st.markdown(f"""
            - **Número de Factura**: {row['numeroFactura']}
              - Producto: {row['categorias']}
              - Ciudad: {row['ciudad']}
              - Fecha: {row['fecha']}
              - Cantidad: {row['cantidadProductos']}
            """)
