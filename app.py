import streamlit as st
import pandas as pd

# Título
st.title("Mi primera app con Streamlit")

# Texto simple
st.write("Hola Paula 👋, esto es tu primer dashboard.")

# Input de usuario
nombre = st.text_input("¿Cómo te llamás?")
if nombre:
    st.success(f"Bienvenida {nombre}, ¡ya estás usando Streamlit!")

# Slider
edad = st.slider("Elegí tu edad:", 0, 100, 30)
st.write(f"Tu edad es: {edad}")

# Mini DataFrame
df = pd.DataFrame({
    "col1": [1, 2, 3],
    "col2": [10, 20, 30]
})
st.dataframe(df)

if st.button("¡Decime hola!"):
    st.write("👋 Hola desde el botón")
    st.balloons()
    st.snow()
    st.success("¡Felicidades! 🎉"
               " Has presionado el botón."
               " Ahora podés seguir explorando Streamlit."
               )

import numpy as np

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"]
)
st.line_chart(chart_data)

st.sidebar.title("Opciones")
opcion = st.sidebar.selectbox("Elegí una opción", ["Inicio", "EDA", "Sobre mí"])
st.write(f"Elegiste: {opcion}")

archivo = st.file_uploader("Subí un CSV", type=["csv"])
if archivo is not None:
    df = pd.read_csv(archivo)
    st.write("Vista previa del dataset:")
    st.dataframe(df.head())

    # Selectbox con columnas
    columna = st.selectbox("Elegí una columna", df.columns)
    st.write("Valores únicos:", df[columna].unique())

# Uso de session_state

st.title("Ejemplo con session_state")

if "contador" not in st.session_state:
    st.session_state.contador = 0

if st.button("Sumar 1"):
    st.session_state.contador += 1

st.write("Contador:", st.session_state.contador)


# Formulario
st.title("Formulario de ejemplo")
with st.form("formulario"):
    nombre = st.text_input("Nombre")
    edad = st.number_input("Edad", 0, 120)
    enviado = st.form_submit_button("Enviar")

if enviado:
    st.success(f"Hola {nombre}, tenés {edad} años.")
