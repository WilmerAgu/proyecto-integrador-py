import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Configuración de la página
st.set_page_config(layout="wide")

st.subheader("Analizador de Datos de Google Sheets")

# Descripción para el usuario
st.markdown("""
Este programa lee datos de "Hoja 1" de una hoja de cálculo de Google Sheets y los transfiere a "Hoja 2".
""")

# Configuración de acceso a Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = st.text_input("Introduce el ID de la hoja de cálculo")
RANGE1 = "Hoja 1!A:F"  # Rango de la Hoja 1
RANGE2 = "Hoja 2!A:F"  # Rango de la Hoja 2

# Cargar credenciales de Streamlit Secrets
google_sheet_credentials = st.secrets["GOOGLE_SHEET_CREDENTIALS"]
secrets_dict = google_sheet_credentials.to_dict()
creds = service_account.Credentials.from_service_account_info(secrets_dict, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Función para leer los datos de la Hoja 1
def read_sheet():
    try:
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE1).execute()
        values = result.get('values', [])
        if not values:
            st.warning("La Hoja 1 está vacía o no tiene datos.")
            return pd.DataFrame()  # Retornar un DataFrame vacío si no hay datos
        # Convertir los datos en un DataFrame de Pandas
        df = pd.DataFrame(values[1:], columns=values[0])  # La primera fila como encabezado
        return df
    except Exception as e:
        st.error(f"Error al leer la Hoja 1: {e}")
        return pd.DataFrame()

# Función para actualizar los datos en la Hoja 2
def update_sheet(df):
    try:
        # Convertir el DataFrame en una lista de listas
        body = {'values': [df.columns.tolist()] + df.values.tolist()}
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE2,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        return result
    except Exception as e:
        st.error(f"Error al actualizar la Hoja 2: {e}")
        return None

# Botón para procesar los datos
if st.button("Transferir datos de Hoja 1 a Hoja 2"):
    if not SPREADSHEET_ID:
        st.error("Por favor, introduce el ID de la hoja de cálculo.")
    else:
        # Leer datos de la Hoja 1
        df = read_sheet()
        if not df.empty:
            st.header("Datos en Hoja 1")
            st.dataframe(df)

            # Transferir los datos a la Hoja 2
            result = update_sheet(df)
            if result:
                st.success(f"Hoja 2 actualizada. {result.get('updatedCells', 0)} celdas actualizadas.")
        else:
            st.warning("No se encontraron datos en la Hoja 1.")
