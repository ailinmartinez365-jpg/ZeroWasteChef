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
    niveles = ["Principiante", "Explorador", "Experto"]

    for nivel in niveles:

        recetas_nivel = []

        for resultado in resultados:

            receta = resultado["receta"]

            if receta["nivel"] == nivel:
                recetas_nivel.append(resultado)

        if recetas_nivel:

            st.header(nivel)

            for resultado in recetas_nivel:

                receta = resultado["receta"]
                porcentaje = resultado["porcentaje"]

                with st.container(border=True):

                    st.subheader(receta["nombre"])

                    st.write(
                        "Coincidencia:",
                        round(porcentaje),
                        "%"
                    )

                    st.write(
                        "Tiempo:",
                        receta["tiempo"],
                        "minutos"
                    )

                    st.write(
                        "Nivel:",
                        receta["nivel"]
                    )

                    if st.button(
                        "Ver receta",
                        key=receta["nombre"]
                    ):

                        st.write("### Ingredientes")

                        for ingrediente in receta["ingredientes"]:
                            st.write("-", ingrediente)

                        st.write("### Instrucciones")

                        for numero, instruccion in enumerate(
                            receta["instrucciones"],
                            start=1
                        ):
                            st.write(
                                numero,
                                ".",
                                instruccion
                            )
