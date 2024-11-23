import streamlit as st
import google.generativeai as genai
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os

# Configura la API Key de Google Generative AI
genai.configure(api_key=st.secrets.GEMINI.api_key)

# Selecciona el modelo
model = genai.GenerativeModel("gemini-1.5-flash")

# Crea la interfaz de usuario con Streamlit
st.title("Generador de Factura con Gemini 1.5")

# Paso 1: Preguntar detalles para la factura
numero_factura = st.text_input("¿Cuál es el número de factura?")
monto = st.number_input("¿Cuál es el monto total de la factura?", min_value=0.01)
categoria = st.selectbox(
    "¿En qué categoría se encuentra el producto?",
    ["Celulares", "Tablets", "DDS", "Audífonos", "Laptops"]
)
vendedor = st.text_input("¿Quién es el vendedor?")
ciudad = st.text_input("¿En qué ciudad se realizó la venta?")
fecha = st.date_input("¿Cuál es la fecha de la factura?", min_value=datetime(2000, 1, 1))

# Paso 2: Generar la factura
if st.button("Generar Factura"):
    if numero_factura and monto and categoria and vendedor and ciudad and fecha:
        # Crear un DataFrame para la factura
        factura_data = {
            "Número de Factura": [numero_factura],
            "Monto Total": [monto],
            "Categoría": [categoria],
            "Vendedor": [vendedor],
            "Ciudad": [ciudad],
            "Fecha": [fecha]
        }
        df = pd.DataFrame(factura_data)

        # Mostrar la factura en Streamlit
        st.write("Factura Pro:")
        st.write(df)

        # Generar el contenido de la factura utilizando el modelo Gemini
        prompt = f"""
        Genera una factura profesional en formato cuadrilla con los siguientes datos.
        - Número de Factura: {numero_factura}
        - Monto Total: {monto}
        - Categoría: {categoria}
        - Vendedor: {vendedor}
        - Ciudad: {ciudad}
        - Fecha: {fecha}

        **Formato requerido**:
        1. Encabezado con título: "Factura Comercial".
        2. Tabla con los detalles de la transacción, como descripción, cantidad, y total.
        3. Resumen con el monto total destacado.
        4. Nota final: "Gracias por su compra. Para cualquier consulta, comuníquese con nosotros."
        """
        respuesta = model.generate_content(prompt)

        # Mostrar el contenido generado
        st.write("Factura generada por Gemini:")
        st.text_area("Contenido de la factura:", respuesta.text, height=300)

        # Crear el PDF de la factura
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Título de la factura
        pdf.cell(200, 10, txt="Factura Pro", ln=True, align="C")
        pdf.ln(10)  # Espacio entre líneas

        # Agregar contenido generado por Gemini al PDF
        for line in respuesta.text.split("\n"):
            pdf.cell(200, 10, txt=line, ln=True)

        # Guardar el PDF en el directorio actual de trabajo
        pdf_output = "factura_Pro.pdf"
        pdf.output(pdf_output)

        # Crear un enlace de descarga en Streamlit
        with open(pdf_output, "rb") as pdf_file:
            btn = st.download_button(
                label="Descargar Factura en PDF",
                data=pdf_file,
                file_name=pdf_output,
                mime="application/pdf"
            )
    else:
        st.warning("Por favor completa todos los campos antes de generar la factura.")
