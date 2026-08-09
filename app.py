import streamlit as st

st.title("🍃 ZeroWaste Chef")

st.write("Convierte lo que tienes en lo que puedes cocinar.")

texto_ingredientes = st.text_input(
    "¿Qué ingredientes tienes?",
    placeholder="Ejemplo: huevo, tomate, queso"
)

if texto_ingredientes:

    ingredientes = texto_ingredientes.lower().split(",")

    ingredientes = [ingrediente.strip() for ingrediente in ingredientes]

    st.write("Tus ingredientes son:")

    for ingrediente in ingredientes:
        st.write("🥕", ingrediente)

else:
    st.warning("Por favor, introduce al menos un ingrediente.")
