import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

st.set_page_config(layout="wide")

st.subheader("Analizador de Datos de Google Sheets")

# Descripción para el usuario
st.markdown("""
Este código lee datos de una hoja de cálculo de Google Sheets llamada "Hoja1", los procesa con Pandas y actualiza una segunda hoja llamada "Hoja2" con nuevos datos. La interfaz de usuario de Streamlit permite al usuario ingresar el ID de la hoja de cálculo y visualizar los datos procesados.
""")

# Configuración de acceso a Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = st.text_input("ID hoja de cálculo")
RANGE1 = "Hoja 1!A:F"  # Rango extendido para capturar todas las columnas necesarias.
RANGE2 = "Hoja 2!A:F"  # El rango para actualizar la Hoja 2.

google_sheet_credentials = st.secrets["GOOGLE_SHEET_CREDENTIALS"]
secrets_dict = google_sheet_credentials.to_dict()
creds = service_account.Credentials.from_service_account_info(secrets_dict, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Función para leer la Hoja 1
def read_sheet():
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE1).execute()
    values = result.get('values', [])
    # Convertir los datos en un DataFrame de Pandas
    df = pd.DataFrame(values[1:], columns=values[0])  # La primera fila como encabezado
    return df

# Función para actualizar la Hoja 2
def update_sheet(df):
    body = {'values': df.values.tolist()}
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE2,
        valueInputOption="USER_ENTERED", body=body).execute()
    return result

# Botón para leer y procesar los datos
if st.button("Analizar datos de Google Sheet"):
    # Leer datos de la Hoja 1
    df = read_sheet()
    st.header("Datos Hoja 1")
    st.dataframe(df)
    
    # Realizar consulta sobre los datos
    # Ejemplo: Filtrar por ciudad (por ejemplo, "Madrid") y agrupar por Producto
    ciudad = st.selectbox("Seleccionar Ciudad", df['Ciudad'].unique())
    df_filtrado = df[df['Ciudad'] == ciudad]
    
    # Agrupar los datos por Producto y calcular las ventas totales
    df_agrupado = df_filtrado.groupby('Producto').agg({'Ventas': 'sum'}).reset_index()
    st.header(f"Datos agrupados por Producto para {ciudad}")
    st.dataframe(df_agrupado)

    # Actualizar la Hoja 2 con el DataFrame procesado
    result = update_sheet(df_agrupado)
    st.success(f"Hoja 2 actualizada. {result.get('updatedCells')} celdas actualizadas.")
    
    # Mostrar el DataFrame actualizado
    st.header("Datos actualizados en Hoja 2")
    st.dataframe(df_agrupado)