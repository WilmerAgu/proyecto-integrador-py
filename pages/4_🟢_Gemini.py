import streamlit as st
import google.generativeai as genai
import pandas as pd
from fpdf import FPDF
from datetime import datetime

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
        st.write("Factura generada:")
        st.write(df)

        # Opción para descargar la factura como Excel
        excel_file = df.to_excel(index=False)
        st.download_button(
            label="Descargar como Excel",
            data=excel_file,
            file_name="factura.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Opción para generar y descargar el PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Número de Factura: {numero_factura}", ln=True)
        pdf.cell(200, 10, txt=f"Monto Total: ${monto:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Categoría: {categoria}", ln=True)
        pdf.cell(200, 10, txt=f"Vendedor: {vendedor}", ln=True)
        pdf.cell(200, 10, txt=f"Ciudad: {ciudad}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha: {fecha.strftime('%d/%m/%Y')}", ln=True)

        # Guardar PDF en un archivo
        pdf_output = pdf.output(dest="S").encode("latin1")

        # Opción para descargar el PDF
        st.download_button(
            label="Descargar como PDF",
            data=pdf_output,
            file_name="factura.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Por favor completa todos los campos antes de generar la factura.")
