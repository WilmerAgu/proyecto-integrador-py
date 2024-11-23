import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", page_title="Mapping Demo", page_icon="🌍")


# Título y subtítulo
st.title("Proyecto Integrador: Factura Pro")
st.subheader("Un Viaje Creativo con [Nombre del Equipo]")

# Imagen de fondo
image = Image.open("./static/proyecto integrador.png") 
st.image(image, width=700, use_column_width=True)  

# Integrantes
st.header("Nuestro Equipo")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.image("./static/Aleja.jpeg", width=200 )  # Reemplaza con la ruta de la foto
    st.write("**[Alejandra Gonzalez]**")
    st.write("[Desarrollador]")

with col2:
    st.image("./static/Wilmer.jpeg", width=200)  # Reemplaza con la ruta de la foto
    st.write("**[Wilmer Agudelo]**")
    st.write("[Desarrollador ]")

with col3:
    st.image("./static/Daniel.jpeg", width=200)  # Reemplaza con la ruta de la foto
    st.write("**[Daniel Sanchez]**")
    st.write("[Desarrollador ]")

with col4:
    st.image("./static/Andres.jpeg", width=200)  # Reemplaza con la ruta de la foto
    st.write("**[Andres Osorio]**")
    st.write("[Desarrollador ]")

with col5:
    st.image("./static/Mauro.jpeg", width=200)  # Reemplaza con la ruta de la foto
    st.write("**[Mauricio Escobar]**")
    st.write("[Desarrollador]")
    
    

# Descripción del proyecto
st.header("Sobre el Proyecto")
st.write("""
Este proyecto busca transformar la gestión financiera de una pequeña empresa mediante el desarrollo de una innovadora aplicación diseñada para optimizar la facturación y el control de gastos. En la actualidad, el Administrador enfrenta el desafío de llevar un registro manual que no solo es propenso a errores, sino que también dificulta un seguimiento efectivo de las finanzas. Con esta nueva herramienta, se facilitará el registro preciso de facturas y gastos, además de generar reportes financieros detallados y alertar sobre pagos próximos a vencer. Así, el Administrador podrá tomar decisiones más informadas y estratégicas, asegurando una gestión más eficiente y organizada de los recursos de la empresa.
""")

# Más información
st.header("Más Información")

# Puedes añadir secciones como:
# - Tecnología utilizada
# - Resultados esperados
# - Presentación de resultados (fecha y formato)
# - Contacto para preguntas

st.write("""
[Agrega la información adicional que consideres relevante.]
""")

# Footer con links
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <a href="https://www.google.com">Google</a> |
        <a href="https://www.facebook.com">Facebook</a> |
        <a href="https://www.linkedin.com">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True,
)