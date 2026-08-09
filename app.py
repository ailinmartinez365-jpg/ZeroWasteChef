import streamlit as st
from recetas import recetas

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
        st.write(ingrediente)

    st.subheader("Recetas encontradas")

    resultados = []

    for receta in recetas:

        coincidencias = 0

        for ingrediente in receta["ingredientes"]:

            if ingrediente in ingredientes:
                coincidencias += 1

        porcentaje = (coincidencias / len(receta["ingredientes"])) * 100

        if porcentaje > 0:
            resultados.append({
                "receta": receta,
                "porcentaje": porcentaje
            })

    resultados.sort(
        key=lambda resultado: resultado["porcentaje"],
        reverse=True
    )
    for resultado in resultados:

    receta = resultado["receta"]
    porcentaje = resultado["porcentaje"]

    with st.container(border=True):

        st.subheader(receta["nombre"])

        st.write("Coincidencia:", round(porcentaje), "%")

        st.write("Tiempo:", receta["tiempo"], "minutos")

        st.write("Nivel:", receta["nivel"])

        st.button("Ver receta", key=receta["nombre"])
    
