import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Configuración de la página
st.set_page_config(layout="wide")

st.subheader("Analizador de Datos de Google Sheets")

# Descripción para el usuario
st.markdown("""
Este programa lee datos de "Hoja 1" de una hoja de cálculo de Google Sheets y transfiere el análisis a "Hoja 2".
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

# Función para analizar los datos y encontrar la ciudad con más ventas
def analyze_data(df):
    try:
        # Convertir columna de ventas a numérico (si no lo está)
        df["Ventas"] = pd.to_numeric(df["Ventas"], errors="coerce")
        # Agrupar por Ciudad y sumar las ventas
        city_sales = df.groupby("Ciudad")["Ventas"].sum().reset_index()
        city_sales = city_sales.sort_values(by="Ventas", ascending=False)
        # Encontrar la ciudad con más ventas
        top_city = city_sales.iloc[0:1]  # Tomar la primera fila como la ciudad con más ventas
        return top_city
    except KeyError as e:
        st.error(f"Error al analizar los datos: Falta la columna {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error inesperado al analizar los datos: {e}")
        return pd.DataFrame()

# Botón para procesar los datos
if st.button("Procesar datos y transferir análisis a Hoja 2"):
    if not SPREADSHEET_ID:
        st.error("Por favor, introduce el ID de la hoja de cálculo.")
    else:
        # Leer datos de la Hoja 1
        df = read_sheet()
        if not df.empty:
            st.header("Datos en Hoja 1")
            st.dataframe(df)

            # Analizar los datos
            top_city = analyze_data(df)
            if not top_city.empty:
                st.header("Ciudad con más ventas")
                st.dataframe(top_city)

                # Transferir el análisis a la Hoja 2
                result = update_sheet(top_city)
                if result:
                    st.success(f"Análisis transferido a Hoja 2. {result.get('updatedCells', 0)} celdas actualizadas.")
            else:
                st.warning("No se pudo analizar los datos.")
        else:
            st.warning("No se encontraron datos en la Hoja 1.")
