import streamlit as st
from recetas import recetas
import os
    
st.set_page_config(
    page_title="Chef Cero Residuos",
    page_icon="🍃",
    layout="wide"
)




st.title("Chef Cero Residuos")

st.write(
    "Convierte lo que tienes en lo que puedes cocinar."
)



st.subheader("¿Qué ingredientes tienes?")

entrada = st.text_input(
    "Escribe tus ingredientes separados por comas",
    placeholder="Ejemplo: huevo, tomate, queso"
)



ingredientes_usuario = []

if entrada:

    ingredientes_usuario = [
        ingrediente.strip().lower()
        for ingrediente in entrada.split(",")
        if ingrediente.strip()
    ]




resultados = []


for receta in recetas:

    ingredientes_receta = [
        ingrediente.lower()
        for ingrediente in receta["ingredientes"]
    ]

    coincidencias = 0

    for ingrediente in ingredientes_usuario:

        if ingrediente in ingredientes_receta:
            coincidencias += 1

    if ingredientes_usuario:

        porcentaje = (
            coincidencias / len(ingredientes_receta)
        ) * 100

    else:

        porcentaje = 0

    if porcentaje > 0:

        resultados.append(
            {
                "receta": receta,
                "porcentaje": porcentaje
            }
        )



resultados.sort(
    key=lambda resultado: resultado["porcentaje"],
    reverse=True
)



if ingredientes_usuario:

    st.subheader("Recetas encontradas")

    if resultados:

        niveles = [
            "Principiante",
            "Explorador",
            "Experto"
        ]


        
        for nivel in niveles:

            recetas_nivel = []


        

            for resultado in resultados:

                receta = resultado["receta"]

                if receta["nivel"] == nivel:

                    recetas_nivel.append(resultado)


            
            if recetas_nivel:

                if nivel == "Principiante":

                    st.header(
                        "Principiante"
                    )

                    st.write(
                        "Recetas rápidas y sencillas"
                    )

                elif nivel == "Explorador":

                    st.header(
                        "Explorador"
                    )

                    st.write(
                        "Recetas para descubrir nuevas combinaciones"
                    )

                elif nivel == "Experto":

                    st.header(
                        "Experto"
                    )

                    st.write(
                        "Recetas para impresionar"
                    )


                
                columnas = st.columns(3)


                for posicion, resultado in enumerate(
                    recetas_nivel
                ):

                    receta = resultado["receta"]

                    porcentaje = resultado["porcentaje"]
                )
                    with columnas[posicion % 3]:

                        with st.container(border=True):

                            ruta_imagen = os.path.join(
                                os.path.dirname(__file__),
                                receta["imagen"]
                            )

                            st.image(
                                ruta_imagen,
                                use_container_width=True
                            )

                            st.subheader(
                                receta["nombre"]
                            )

                            st.write(
                                "✓",
                                round(porcentaje),
                                "% de coincidencia"
                            )

                            st.write(
                                "⏱️",
                                receta["tiempo"],
                                "minutos"
                            )

                            st.write(
                                "Nivel:",
                                receta["nivel"]
                            )

                            if st.button(
                                "Ver receta",
                                key="ver_" + receta["nombre"]
                            ):

                                st.write(
                                    "### Ingredientes"
                                )

                                for ingrediente in receta[
                                    "ingredientes"
                                ]:

                                    st.write(
                                        "-",
                                        ingrediente
                                    )

                                st.write(
                                    "### Instrucciones"
                                )

                                for numero, instruccion in enumerate(
                                    receta["instrucciones"],
                                    start=1
                                ):

                                    st.write(
                                        str(numero) + ".",
                                        instruccion
                        )
        if st.button(
            "Ver receta",
            key="ver_" + receta["nombre"]
        ):

            st.write("### Ingredientes")

            for ingrediente in receta["ingredientes"]:

                st.write(
                    "-",
                    ingrediente
                )

            st.write("### Instrucciones")

            for numero, instruccion in enumerate(
                receta["instrucciones"],
                start=1
            ):

                st.write(
                    str(numero) + ".",
                    instruccion
                )
                    
                            
                            if st.button(
                                "Ver receta",
                                key="ver_" + receta["nombre"]
                            ):

                                st.write(
                                    
                                )


                                for ingrediente in receta[
                                    "ingredientes"
                                ]:

                                    st.write(
                                        "-",
                                        ingrediente
                                    )


                                st.write(
                                    
                                )


                                for numero, instruccion in enumerate(
                                    receta["instrucciones"],
                                    start=1
                                ):

                                    st.write(
                                        str(numero) + ".",
                                        instruccion
                                    )


    else:

        st.warning(
            "No encontramos recetas que coincidan con tus ingredientes."
        )



else:

    st.info(
        "Escribe algunos ingredientes para comenzar."
                            )
