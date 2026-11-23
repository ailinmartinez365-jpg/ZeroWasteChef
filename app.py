
import streamlit as st
from recetas import recetas
from recetas_familia import familia
from recetas_temporada import temporada
import os

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Chef Cero Residuos",
    page_icon="🍃",
    layout="wide"
)

# ENCABEZADO
st.title("Chef Cero Residuos")
st.write("Convierte lo que tienes en lo que puedes cocinar.")

# NAVEGACIÓN
pestaña_menu, pestaña_buscador, pestaña_familia, pestaña_temporada = st.tabs([
    "Menú",
    "Buscador",
    "Familia",
    "Temporada"
])

# BUSCADOR
with pestaña_buscador:

    st.subheader("¿Qué ingredientes tienes?")

    entrada = st.text_input(
        "Escribe tus ingredientes separados por comas",
        placeholder="Ejemplo: huevo, tomate, queso"
    )

    filtro_tiempo = st.selectbox(
        "¿Cuánto tiempo tienes?",
        ["Todos", "10 minutos", "20 minutos", "30+ minutos"]
    )

    filtro_nivel = st.selectbox(
        "¿Qué nivel buscas?",
        ["Todos", "Principiante", "Explorador", "Intermedio", "Experto"]
    )

    # NORMALIZAR INGREDIENTES
    ingredientes_usuario = []

    if entrada:
        ingredientes_usuario = [
            ingrediente.strip().lower()
            for ingrediente in entrada.split(",")
            if ingrediente.strip()
        ]

    # BUSCAR RECETAS
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
        if ingredientes_usuario:
            porcentaje = (
                coincidencias / len(ingredientes_receta)
            ) * 100
        else:
            porcentaje = 0

        # IDENTIFICAR INGREDIENTES FALTANTES
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

    # ORDENAR RESULTADOS
    resultados.sort(
        key=lambda resultado: resultado["porcentaje"],
        reverse=True
    )

    # MOSTRAR RESULTADOS
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

                    if nivel == "Principiante":
                        st.header("Principiante")
                        st.write("Recetas rápidas y sencillas")

                    elif nivel == "Explorador":
                        st.header("Explorador")
                        st.write("Recetas para descubrir nuevas combinaciones")

                    elif nivel == "Intermedio":
                        st.header("Intermedio")
                        st.write("Recetas que requieren un poco más de práctica")

                    elif nivel == "Experto":
                        st.header("Experto")
                        st.write("Recetas para impresionar")

                    columnas = st.columns(3)

                    for posicion, resultado in enumerate(recetas_nivel):

                        receta = resultado["receta"]
                        porcentaje = resultado["porcentaje"]
                        faltantes = resultado["faltantes"]
                        ingredientes_receta = receta["ingredientes"]

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

                                st.subheader(receta["nombre"])

                                st.write(
                                    "✓",
                                    round(porcentaje),
                                    "% de coincidencia"
                                )

                                tienes = len(ingredientes_receta) - len(faltantes)

                                st.write(
                                    "Tienes",
                                    tienes,
                                    "de",
                                    len(ingredientes_receta),
                                    "ingredientes"
                                )

                                if porcentaje == 100:
                                    st.success("¡Tienes todos los ingredientes!")

                                elif porcentaje >= 75:
                                    st.info("¡Casi tienes todo!")

                                elif porcentaje >= 50:
                                    st.warning("Te faltan algunos ingredientes.")

                                else:
                                    st.write("Necesitas varios ingredientes.")

                                if faltantes:
                                    st.write(
                                        "Te faltan:",
                                        ", ".join(faltantes)
                                    )
                                else:
                                    st.write("¡Tienes todos los ingredientes!")

                                st.write(
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

                                    st.divider()

                                    st.subheader(receta["nombre"])

                                    st.write("### Ingredientes")

                                    for ingrediente in receta["ingredientes"]:
                                        st.write("•", ingrediente)

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
        st.info("Escribe algunos ingredientes para comenzar.")

# CONTENIDO PROVISIONAL DE LAS OTRAS PESTAÑAS
with pestaña_menu:
    st.subheader("Menú")

    categoria = st.radio(
        "Selecciona una categoría:",
        ["Comida", "Postres", "Extras", "Bebidas"],
        horizontal=True
    )

    subcategoria = None

    if categoria == "Comida":
        subcategoria = st.radio(
            "Selecciona el horario:",
            ["Desayuno", "Almuerzo", "Cena"],
            horizontal=True
        )

    elif categoria == "Extras":
        subcategoria = st.radio(
            "Selecciona una categoría:",
            ["Botanas", "Fit", "Otros"],
            horizontal=True
        )

    recetas_filtradas = []

    for receta in recetas:
        if receta["categoria"] == categoria:

            if subcategoria is None:
                recetas_filtradas.append(receta)

            elif receta.get("subcategoria", "") == subcategoria:
                recetas_filtradas.append(receta)

    if recetas_filtradas:
        st.subheader("Recetas disponibles")

        columnas = st.columns(3)

        for posicion, receta in enumerate(recetas_filtradas):
            with columnas[posicion % 3]:
                with st.container(border=True):

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
                        st.info("Imagen próximamente")

                    st.subheader(receta["nombre"])
                    st.write(receta["tiempo"], "minutos")
                    st.write("Nivel:", receta["nivel"])

                    if st.button(
                        "Ver receta",
                        key="menu_" + receta["nombre"]
                    ):
                        st.subheader(receta["nombre"])

                        st.write("### Ingredientes")
                        for ingrediente in receta["ingredientes"]:
                            st.write("•", ingrediente)

                        st.write("### Preparación")
                        for numero, instruccion in enumerate(
                            receta["instrucciones"],
                            start=1
                        ):
                            st.write(str(numero) + ".", instruccion)

    else:
        st.info("Todavía no hay recetas en esta categoría.")
# SECCIÓN FAMILIA
with pestaña_familia:
    st.subheader("Familia")
    categoria_familia = st.radio(
        "Selecciona una categoría:",
        ["En familia", "Niños", "Lonche"],
        horizontal=True
    )
    recetas_familia_filtradas = []

    for receta in familia:
        if receta["categoria"] == categoria_familia:
            recetas_familia_filtradas.append(receta)
    
    if recetas_familia_filtradas:
        st.subheader("Recetas disponibles")

    else:
        st.info("Todavía no hay recetas en esta categoría.")
    
    columnas = st.columns(3)

    for posicion, receta in enumerate(recetas_familia_filtradas):

        with columnas[posicion % 3]:

            with st.container(border=True):

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
                    st.info("Imagen próximamente")

                st.subheader(receta["nombre"])

                st.write(receta["tiempo"], "minutos")
                st.write("Nivel:", receta["nivel"])
                if st.button(
                    "Ver receta",
                    key="familia_" + receta["nombre"]
                ):

                    st.subheader(receta["nombre"])

                    st.write("### Ingredientes")

                    for ingrediente in receta["ingredientes"]:
                        st.write("•", ingrediente)

                    st.write("### Preparación")

                    for numero, instruccion in enumerate(
                        receta["instrucciones"],
                        start=1
                    ):
                        st.write(
                            str(numero) + ".",
                            instruccion
                        )
# SECCIÓN TEMPORADA
with pestaña_temporada:
    st.subheader("Temporada")
    categoria_temporada = st.radio(
        "Selecciona una temporada:",
        ["Primavera", "Verano", "Otoño", "Invierno"],
        horizontal=True
    )
    recetas_temporada_filtradas = []

    for receta in temporada:
        if receta["categoria"] == categoria_temporada:
            recetas_temporada_filtradas.append(receta)
    if recetas_temporada_filtradas:
        st.subheader("Recetas disponibles")

        columnas = st.columns(3)

        for posicion, receta in enumerate(recetas_temporada_filtradas):
            with columnas[posicion % 3]:
                with st.container(border=True):

                    ruta_imagen = os.path.join(
                        os.path.dirname(__file__),
                        receta["imagen"]
                    )

                    if os.path.exists(ruta_imagen):
                        st.image(ruta_imagen, use_container_width=True)
                    else:
                        st.info("Imagen próximamente")

                    st.subheader(receta["nombre"])
                    st.write(receta["tiempo"], "minutos")
                    st.write("Nivel:", receta["nivel"])

                    if st.button(
                        "Ver receta",
                        key="temporada_" + receta["nombre"]
                    ):
                        st.subheader(receta["nombre"])

                        st.write("### Ingredientes")
                        for ingrediente in receta["ingredientes"]:
                            st.write("•", ingrediente)

                        st.write("### Preparación")
                        for numero, instruccion in enumerate(
                            receta["instrucciones"],
                            start=1
                        ):
                            st.write(str(numero) + ".", instruccion)

    else:
        st.info("Todavía no hay recetas en esta temporada.")
