import streamlit as st

st.title("🍃 ZeroWaste Chef")

st.write("Convierte lo que tienes en lo que puedes cocinar.")

ingredientes = st.text_input(
    "¿Qué ingredientes tienes?",
    placeholder="Ejemplo: huevo, tomate, queso"
)

if ingredientes:
    st.write("Tus ingredientes son:", ingredientes)
else:
    st.warning("Por favor, introduce al menos un ingrediente.")
