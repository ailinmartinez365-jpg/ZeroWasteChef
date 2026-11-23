
import streamlit as st
from recetas import recetas
import os

# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Kitchen Help",
    page_icon="🍳",
    layout="wide"
)

# ============================================================
# TÍTULO PRINCIPAL
# ============================================================

st.title("Kitchen Help")

st.write(
    "Convierte lo que tienes en lo que puedes cocinar."
)

# ============================================================
# NAVEGACIÓN PRINCIPAL
# ============================================================

tab_menu, tab_buscador, tab_familia, tab_temporada = st.tabs([
    "Menú",
    "Buscador",
    "Familia",
    "Temporada"
])

# ============================================================
# 1. BUSCADOR
# ============================================================

with tab_buscador:

    st.subheader("¿Qué ingredientes tienes?")

    entrada = st.text_input(
        "Escribe tus ingredientes separados por comas",
        placeholder="Ejemplo: huevo, tomate, queso"
    )

    # FILTROS

    col1, col2 = st.columns(2)

    with col1:
        filtro_tiempo = st.selectbox(
            "¿Cuánto tiempo tienes?",
            [
                "Todos",
                "10 minutos",
                "20 minutos",
                "30+ minutos"
            ]
        )

    with col2:
        filtro_nivel = st.selectbox(
            "¿Qué nivel buscas?",
            [
                "Todos",
                "Principiante",
                "Explorador",
                "Intermedio",
                "Experto"
            ]
        )

    # ========================================================
    # INGREDIENTES DEL USUARIO
    # ========================================================

    ingredientes_usuario = []

    if entrada:
        ingredientes_usuario = [
            ingrediente.strip().lower()
            for ingrediente in entrada.split(",")
            if ingrediente.strip()
        ]

    # ========================================================
    # BUSCAR RECETAS
    # ========================================================

    resultados = []

    for receta in recetas:

        # FILTRO DE TIEMPO

        if filtro_tiempo == "10 minutos":

            if receta["tiempo"] > 10:
                continue

        elif filtro_tiempo == "20 minutos":

            if receta["tiempo"] > 20:
                continue

        elif filtro_tiempo == "30+ minutos":

            if receta["tiempo"] < 30:
                continue

        # FILTRO DE NIVEL

        if filtro_nivel != "Todos":

            if receta["nivel"] != filtro_nivel:
                continue

        # INGREDIENTES DE LA RECETA

        ingredientes_receta = [
            ingrediente.lower()
            for ingrediente in receta["ingredientes"]
        ]

        # CONTAR COINCIDENCIAS

        coincidencias = 0

        for ingrediente in ingredientes_usuario:

            if ingrediente in ingredientes_receta:
                coincidencias += 1

        # CALCULAR PORCENTAJE

        if ingredientes_usuario and ingredientes_receta:

            porcentaje = (
                coincidencias / len(ingredientes_receta)
            ) * 100

        else:
            porcentaje = 0

        # CALCULAR INGREDIENTES FALTANTES

        if porcentaje > 0:

            faltantes = []

            for ingrediente in ingredientes_receta:

                if ingrediente not in ingredientes_usuario:
                    faltantes.append(ingrediente)

            resultados.append({
                "receta": receta,
                "porcentaje": porcentaje,
                "faltantes": faltantes
            })

    # ========================================================
    # ORDENAR RESULTADOS
    # ========================================================

    resultados.sort(
        key=lambda resultado: resultado["porcentaje"],
        reverse=True
    )

    # ========================================================
    # MOSTRAR RESULTADOS
    # ========================================================

    if ingredientes_usuario:

        st.subheader("Recetas encontradas")

        if resultados:

            niveles = [
                "Principiante",
                "Explorador",
                "Intermedio",
                "Experto"
            ]

            for nivel in niveles:

                recetas_nivel = []

                for resultado in resultados:

                    receta = resultado["receta"]

                    if receta["nivel"] == nivel:
                        recetas_nivel.append(resultado)

                if recetas_nivel:

                    # TÍTULOS DE LOS NIVELES

                    if nivel == "Principiante":

                        st.header("Principiante")
                        st.write("Recetas rápidas y sencillas")

                    elif nivel == "Explorador":

                        st.header("Explorador")
                        st.write(
                            "Recetas para descubrir nuevas combinaciones"
                        )

                    elif nivel == "Intermedio":

                        st.header("Intermedio")
                        st.write(
                            "Recetas para desarrollar tus habilidades"
                        )

                    elif nivel == "Experto":

                        st.header("Experto")
                        st.write("Recetas para impresionar")

                    # CREAR TRES COLUMNAS

                    columnas = st.columns(3)

                    # MOSTRAR TARJETAS

                    for posicion, resultado in enumerate(recetas_nivel):

                        receta = resultado["receta"]
                        porcentaje = resultado["porcentaje"]
                        faltantes = resultado["faltantes"]

                        ingredientes_receta = receta["ingredientes"]

                        with columnas[posicion % 3]:

                            with st.container(border=True):

                                # IMAGEN

                                ruta_imagen = os.path.join(
                                    os.path.dirname(__file__),
                                    receta["imagen"]
                                )

                                if os.path.exists(ruta_imagen):

                                    st.image(
                                        ruta_imagen,
                                        use_container_width=True
                                    )

                                else:
                                    st.info("Imagen no disponible")

                                # NOMBRE

                                st.subheader(receta["nombre"])

                                # PORCENTAJE

                                st.write(
                                    "✓",
                                    round(porcentaje),
                                    "% de coincidencia"
                                )

                                # INGREDIENTES DISPONIBLES

                                tienes = (
                                    len(ingredientes_receta)
                                    - len(faltantes)
                                )

                                st.write(
                                    "Tienes",
                                    tienes,
                                    "de",
                                    len(ingredientes_receta),
                                    "ingredientes"
                                )

                                # MENSAJE SEGÚN COINCIDENCIA

                                if porcentaje == 100:

                                    st.success(
                                        "¡Tienes todos los ingredientes!"
                                    )

                                elif porcentaje >= 75:

                                    st.info("¡Casi tienes todo!")

                                elif porcentaje >= 50:

                                    st.warning(
                                        "Te faltan algunos ingredientes."
                                    )

                                else:

                                    st.write(
                                        "Necesitas varios ingredientes."
                                    )

                                # INGREDIENTES FALTANTES

                                if faltantes:

                                    st.write(
                                        "🛒 Te faltan:",
                                        ", ".join(faltantes)
                                    )

                                else:

                                    st.write(
                                        "🎉 ¡Tienes todos los ingredientes!"
                                    )

                                # TIEMPO

                                st.write(
                                    "⏱️",
                                    receta["tiempo"],
                                    "minutos"
                                )

                                # NIVEL

                                st.write(
                                    "Nivel:",
                                    receta["nivel"]
                                )

                                # BOTÓN VER RECETA

                                if st.button(
                                    "Ver receta",
                                    key="ver_" + receta["nombre"]
                                ):

                                    st.divider()

                                    st.subheader(
                                        "🍳 " + receta["nombre"]
                                    )

                                    st.write("### Ingredientes")

                                    for ingrediente in receta["ingredientes"]:

                                        st.write(
                                            "•",
                                            ingrediente
                                        )

                                    st.write("### Preparación")

                                    for numero, instruccion in enumerate(
                                        receta["instrucciones"],
                                        start=1
                                    ):

                                        st.write(
                                            str(numero) + ".",
                                            instruccion
                                        )

                                    st.divider()

        else:

            st.warning(
                "No encontramos recetas que coincidan con tus ingredientes."
            )

    else:

        st.info(
            "Escribe algunos ingredientes para comenzar."
        )

# ============================================================
# 2. MENÚ
# ============================================================

with tab_menu:

    st.header("Menú")

    st.info(
        "Aquí organizaremos las recetas de Comida, Postres, Extras y Bebidas."
    )

# ============================================================
# 3. FAMILIA
# ============================================================

with tab_familia:

    st.header("Familia")

    st.info(
        "Aquí estarán las recetas En familia, Niños y Lonche."
    )

# ============================================================
# 4. TEMPORADA
# ============================================================

with tab_temporada:

    st.header("Temporada")

    st.info(
        "Aquí organizaremos las recetas de Primavera, Verano, Otoño e Invierno."
                                    )
    
