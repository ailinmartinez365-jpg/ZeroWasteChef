
import streamlit as st
import os

import recetas as modulo_recetas
import recetas_familia
import recetas_temporada

recetas = modulo_recetas.recetas
familia = recetas_familia.familia
temporada = recetas_temporada.temporada

# ENCABEZADO PRINCIPAL
ruta_banner = os.path.join(
    os.path.dirname(__file__),
    "banner.png"
)

if os.path.exists(ruta_banner):
    st.image(
        ruta_banner,
        use_container_width=True
    )
else:
    st.warning("No se encontró la imagen banner.png")
# CONTROL DE PANTALLAS
if "entrar_app" not in st.session_state:
    st.session_state.entrar_app = False

# PANTALLA DE PORTADA
if not st.session_state.entrar_app:

    ruta_portada = os.path.join(
        os.path.dirname(__file__),
        "portada.png"
    )

    if os.path.exists(ruta_portada):
        st.image(
            ruta_portada,
            use_container_width=True
        )
    else:
        st.error("No se encontró el archivo portada.png")

    if st.button("Entrar", use_container_width=True):
        st.session_state.entrar_app = True
        st.rerun()

    st.stop()


# NIVELES DE DIFICULTAD
niveles = [
    "Principiante",
    "Explorador",
    "Intermedio",
    "Experto"
]

# MOSTRAR RECETAS EN CARRUSELES
def mostrar_carruseles_por_nivel(lista_recetas, seccion):

    descripciones = {
        "Principiante": "Recetas rápidas y sencillas",
        "Explorador": "Descubre nuevas combinaciones",
        "Intermedio": "Recetas para desarrollar tus habilidades",
        "Experto": "Preparaciones para poner a prueba tu experiencia"
    }

    for nivel in niveles:

        recetas_nivel = [
            receta for receta in lista_recetas
            if receta.get("nivel") == nivel
        ]

        st.markdown(f"### {nivel}")
        st.caption(descripciones[nivel])

        if not recetas_nivel:
            st.info("Todavía no hay recetas en este nivel.")
            continue

        # CONFIGURAR POSICIÓN DEL CARRUSEL
        clave = f"carrusel_{seccion}_{nivel}"

        if clave not in st.session_state:
            st.session_state[clave] = 0

        inicio = st.session_state[clave]

        # BOTONES Y TARJETAS
        anterior, centro, siguiente = st.columns([0.5, 6, 0.5])

        with anterior:
            if inicio > 0:
                if st.button("‹", key=f"{clave}_anterior"):
                    st.session_state[clave] = max(0, inicio - 3)
                    st.rerun()

        with siguiente:
            if inicio + 3 < len(recetas_nivel):
                if st.button("›", key=f"{clave}_siguiente"):
                    st.session_state[clave] = inicio + 3
                    st.rerun()

        with centro:

            columnas = st.columns(3)

            for posicion, receta in enumerate(
                recetas_nivel[inicio:inicio + 3]
            ):

                with columnas[posicion]:

                    with st.container(border=True):

                        imagen = receta.get("imagen")

                        if imagen:
                            ruta_imagen = os.path.join(
                                os.path.dirname(__file__),
                                imagen
                            )

                            if os.path.exists(ruta_imagen):
                                st.image(
                                    ruta_imagen,
                                    use_container_width=True
                                )
                            else:
                                st.info("Imagen próximamente")
                        else:
                            st.info("Imagen próximamente")

                        st.markdown(f"**{receta['nombre']}**")

                        st.caption(
                            f"{receta.get('tiempo', 'No especificado')} minutos"
                        )

                        with st.expander("Ver receta"):

                            st.write("**Ingredientes**")

                            for ingrediente in receta["ingredientes"]:
                                st.write(f"- {ingrediente}")

                            st.write("**Preparación**")

                            for numero, instruccion in enumerate(
                                receta["instrucciones"],
                                start=1
                            ):
                                st.write(f"{numero}. {instruccion}")

        st.divider()
        
# NAVEGACIÓN
pestaña_menu, pestaña_buscador, pestaña_familia, pestaña_temporada = st.tabs([
    "Menú",
    "Buscador",
    "Familia",
    "Temporada"
])

# BUSCADOR

with pestaña_buscador:
    todas_las_recetas = recetas + familia + temporada

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

    # EQUIVALENCIAS DE INGREDIENTES
    equivalencias = {
        "jitomate": "tomate",
        "jitomates": "tomate",
        "tomates": "tomate",
        "papas": "papa",
        "patata": "papa",
        "patatas": "papa",
        "grenetina": "gelatina",
        "gelatinas": "gelatina",
        "gelatina sin sabor": "gelatina",
        "fresas": "fresa",
        "espinacas": "espinaca",
        "uvas": "uva",
        "limones": "limón",
        "zanahorias": "zanahoria",
        "naranjas": "naranja",
        "mangos": "mango",
        "cebollas": "cebolla",
        "huevos": "huevo",
        "ajos": "ajo"
    }

    # ALIMENTOS QUE PUEDE RECONOCER EL BUSCADOR
    alimentos_reconocidos = [
        "mantequilla", "azúcar", "harina", "vainilla",
        "tomate", "papa", "limón", "sandía", "gelatina",
        "fresa", "betabel", "naranja", "espinaca", "uva",
        "zanahoria", "mango", "huevo", "queso", "cebolla",
        "ajo", "carne", "tocino", "aceite", "orégano",
        "canela", "sal", "pimienta", "pollo", "res",
        "cerdo", "leche", "crema", "yogur", "arroz",
        "pasta", "frijol", "chile", "cilantro", "perejil",
        "albahaca", "soya", "salsa", "agua", "avena",
        "chocolate", "miel", "manzana", "plátano",
        "nuez", "almendra", "elote", "pepino", "lechuga",
        "brócoli", "calabaza", "champiñón", "pimiento"
    ]

    # NORMALIZAR INGREDIENTES
    def normalizar_ingrediente_receta(ingrediente):
        texto = ingrediente.lower().strip()

        for palabra, equivalente in equivalencias.items():
            texto = texto.replace(palabra, equivalente)

        return texto

    # EXTRAER ALIMENTOS DE UNA DESCRIPCIÓN
    def extraer_alimentos(ingrediente):
        texto = normalizar_ingrediente_receta(ingrediente)
        alimentos_encontrados = []

        palabras = [
            palabra.strip(".,:;()[]{}¡!¿?\"'")
            for palabra in texto.split()
        ]

        for alimento in alimentos_reconocidos:
            if alimento in palabras:
                alimentos_encontrados.append(alimento)

        return alimentos_encontrados

    # OBTENER INGREDIENTES NORMALIZADOS DE UNA RECETA
    def obtener_ingredientes_normalizados(receta):
        ingredientes_normalizados = []

        for ingrediente in receta["ingredientes"]:

            texto = ingrediente.strip().lower()

            # Ignorar encabezados de secciones
            if texto.startswith("para ") and texto.endswith(":"):
                continue

            alimentos = extraer_alimentos(ingrediente)

            for alimento in alimentos:
                if alimento not in ingredientes_normalizados:
                    ingredientes_normalizados.append(alimento)

        return ingredientes_normalizados

    # NORMALIZAR INGREDIENTES DEL USUARIO
    ingredientes_usuario = []

    if entrada:
        for ingrediente in entrada.split(","):
            ingrediente = normalizar_ingrediente_receta(ingrediente)
            alimentos = extraer_alimentos(ingrediente)

            for alimento in alimentos:
                if alimento not in ingredientes_usuario:
                    ingredientes_usuario.append(alimento)

    # BUSCAR RECETAS COINCIDENTES
    recetas_coincidentes = []

    if entrada and ingredientes_usuario:

        for receta in todas_las_recetas:

            ingredientes_receta = obtener_ingredientes_normalizados(receta)

            if not ingredientes_receta:
                continue

            coincidencias = [
                ingrediente
                for ingrediente in ingredientes_receta
                if ingrediente in ingredientes_usuario
            ]

            faltantes = [
                ingrediente
                for ingrediente in ingredientes_receta
                if ingrediente not in ingredientes_usuario
            ]

            porcentaje = round(
                len(coincidencias) / len(ingredientes_receta) * 100
            )

            # FILTRO DE TIEMPO
            tiempo = receta.get("tiempo", 0)

            if filtro_tiempo == "10 minutos" and tiempo > 10:
                continue

            if filtro_tiempo == "20 minutos" and tiempo > 20:
                continue

            if filtro_tiempo == "30+ minutos" and tiempo < 30:
                continue

            # FILTRO DE NIVEL
            if (
                filtro_nivel != "Todos"
                and receta.get("nivel") != filtro_nivel
            ):
                continue

            if coincidencias:
                recetas_coincidentes.append({
                    "receta": receta,
                    "porcentaje": porcentaje,
                    "coincidencias": coincidencias,
                    "faltantes": faltantes
                })

        # ORDENAR DE MAYOR A MENOR COINCIDENCIA
        recetas_coincidentes.sort(
            key=lambda resultado: resultado["porcentaje"],
            reverse=True
        )

    # MOSTRAR RESULTADOS
    if entrada:

        if not ingredientes_usuario:
            st.warning(
                "No reconocí alimentos en tu búsqueda. "
                "Intenta escribir ingredientes como huevo, tomate o papa."
            )

        elif not recetas_coincidentes:
            st.info(
                "No encontramos recetas con esos ingredientes "
                "y filtros. Intenta cambiar tu búsqueda."
            )

        else:
            st.subheader("Recetas que puedes preparar")

            columnas = st.columns(3)

            for indice, resultado in enumerate(recetas_coincidentes):

                receta = resultado["receta"]
                porcentaje = resultado["porcentaje"]

                with columnas[indice % 3]:

                    st.markdown(f"**{receta['nombre']}**")

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

                    st.metric(
                        "Coincidencia",
                        f"{porcentaje}%"
                    )

                    st.write(
                        f"Tiempo: {receta.get('tiempo', 'No especificado')} minutos"
                    )

                    st.write(
                        f"Nivel: {receta.get('nivel', 'No especificado')}"
                    )

                    st.write(
                        f"Ingredientes encontrados: "
                        f"{len(resultado['coincidencias'])}"
                    )

                    if resultado["faltantes"]:
                        st.write("**Ingredientes que te faltan:**")
                        st.write(", ".join(resultado["faltantes"]))
                    else:
                        st.success("¡Tienes todos los ingredientes reconocidos!")

                    with st.expander("Ver receta"):

                        st.write("**Descripción:**")
                        st.write(
                            receta.get("descripcion", "Sin descripción")
                        )

                        st.write("**Ingredientes:**")
                        for ingrediente in receta["ingredientes"]:
                            st.write(f"- {ingrediente}")

                        st.write("**Instrucciones:**")
                        for paso, instruccion in enumerate(
                            receta["instrucciones"], start=1
                        ):
                            st.write(f"{paso}. {instruccion}")
    
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

                                if os.path.exists(ruta_imagen):
                                    st.image(
                                        ruta_imagen,
                                        use_container_width=True
                                    )
                                else:
                                    st.info("Imagen próximamente")

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

    st.divider()

    mostrar_carruseles_por_nivel(
        recetas_filtradas,
        "menu"
    )
    
# SECCIÓN FAMILIA
with pestaña_familia:

    st.subheader("Recetas para compartir")

    categoria_familia = st.radio(
        "Selecciona una categoría:",
        ["En familia", "Niños", "Lonche"],
        horizontal=True,
        key="categoria_familia"
    )

    recetas_familia_filtradas = [
        receta for receta in familia
        if receta.get("categoria") == categoria_familia
        or receta.get("subcategoria") == categoria_familia
    ]

    st.divider()

    mostrar_carruseles_por_nivel(
        recetas_familia_filtradas,
        f"familia_{categoria_familia}"
    )
with pestaña_temporada:

    st.subheader("Recetas de temporada")

    temporada_seleccionada = st.radio(
        "Selecciona una temporada:",
        ["Primavera", "Verano", "Otoño", "Invierno"],
        horizontal=True,
        key="temporada_seleccionada"
    )

    recetas_temporada_filtradas = [
        receta for receta in temporada
        if receta.get("categoria") == temporada_seleccionada
        or receta.get("subcategoria") == temporada_seleccionada
    ]

    st.divider()

    mostrar_carruseles_por_nivel(
        recetas_temporada_filtradas,
        f"temporada_{temporada_seleccionada}"
    )
