import streamlit as st
from recetas import recetas
import os



st.set_page_config(
    page_title="Chef Cero Residuos",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

def normalizar_ingrediente(ingrediente):

    ingrediente = ingrediente.strip().lower()

    # Eliminar cantidades comunes

    palabras = ingrediente.split()

    palabras_ignoradas = [
        "un",
        "una",
        "unos",
        "unas",
        "el",
        "la",
        "los",
        "las",
        "de",
        "del",
        "gramos",
        "gramo",
        "kg",
        "kilo",
        "kilos",
        "ml",
        "litro",
        "litros",
        "taza",
        "tazas",
        "cucharada",
        "cucharadas",
        "cucharadita",
        "cucharaditas"
    ]

    palabras_limpias = []

    for palabra in palabras:

        palabra_limpia = palabra.strip(".,;:")

        if palabra_limpia.isdigit():
            continue

        if palabra_limpia not in palabras_ignoradas:
            palabras_limpias.append(palabra_limpia)


    ingrediente = " ".join(palabras_limpias)


    # Equivalencias

    equivalencias = {

        "jitomate": "tomate",
        "jitomates": "tomate",
        "tomates": "tomate",

        "huevos": "huevo",

        "tortillas": "tortilla",

        "quesos": "queso",

        "cebollas": "cebolla",

        "papas": "papa",
        "patatas": "papa",

        "zanahorias": "zanahoria",

        "aceites": "aceite",

        "chiles": "chile",

        "limones": "limon",
        "limón": "limon",

        "ajos": "ajo"
    }


    if ingrediente in equivalencias:

        return equivalencias[ingrediente]


    # Plural simple

    if ingrediente.endswith("s") and len(ingrediente) > 3:

        ingrediente = ingrediente[:-1]


    return ingrediente

st.markdown(
    """
    <style>


    .stApp {
        background-color: #F5F1E8;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 45px;
        padding-bottom: 60px;
    }



    .marca {
        text-align: center;
        margin-bottom: 8px;
    }

    .marca h1 {
        font-size: 46px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 5px;
        color: #26352B;
    }

    .marca p {
        font-size: 18px;
        color: #59645C;
        margin-top: 0;
        letter-spacing: 0.3px;
    }



    .linea {
        height: 1px;
        background-color: #D7D0C2;
        margin: 35px 0;
    }



    .seccion-busqueda {
        text-align: center;
        margin-bottom: 25px;
    }

    .seccion-busqueda h2 {
        font-size: 30px;
        color: #26352B;
        margin-bottom: 8px;
    }

    .seccion-busqueda p {
        font-size: 16px;
        color: #687168;
        margin-top: 0;
    }



    div[data-testid="stTextInput"] input {
        border: 1px solid #C9C2B5;
        border-radius: 12px;
        background-color: #FFFFFF;
        padding: 14px;
        font-size: 16px;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #536B59;
        box-shadow: 0 0 0 1px #536B59;
    }



    div[data-baseweb="select"] > div {
        border-radius: 10px;
        border: 1px solid #C9C2B5;
        background-color: #FFFFFF;
    }



    .titulo-resultados {
        font-size: 30px;
        font-weight: 700;
        color: #26352B;
        margin-bottom: 4px;
    }

    .descripcion-resultados {
        color: #687168;
        font-size: 16px;
        margin-bottom: 25px;
    }



    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border: 1px solid #DED8CC;
        border-radius: 18px;
        padding: 4px;
    }



    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #536B59;
        background-color: #536B59;
        color: white;
        font-weight: 600;
        padding: 10px;
    }

    .stButton > button:hover {
        border-color: #3F5545;
        background-color: #3F5545;
        color: white;
    }



    .informacion-receta {
        color: #687168;
        font-size: 14px;
    }



    .footer {
        text-align: center;
        color: #7A817B;
        font-size: 13px;
        margin-top: 50px;
    }

    </style>
    """,
    unsafe_allow_html=True
)



st.markdown(
    """
    <div class="marca">
        <h1>CHEF CERO RESIDUOS</h1>
        <p>No solo cocines. Aprovecha, descubre y comparte.</p>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown('<div class="linea"></div>', unsafe_allow_html=True)



st.markdown(
    """
    <div class="seccion-busqueda">
        <h2>Busca una receta</h2>
        <p>
            Escribe los ingredientes que tienes disponibles
            y descubre qué puedes preparar.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


entrada = st.text_input(
    "Ingredientes",
    placeholder="Ejemplo: huevo, tomate, queso",
    label_visibility="collapsed"
)



columna_tiempo, columna_nivel = st.columns(2)


with columna_tiempo:

    filtro_tiempo = st.selectbox(
        "Tiempo disponible",
        [
            "Todos",
            "10 minutos",
            "20 minutos",
            "30+ minutos"
        ]
    )


with columna_nivel:

    filtro_nivel = st.selectbox(
        "Nivel de dificultad",
        [
            "Todos",
            "Principiante",
            "Explorador",
            "Experto"
        ]
    )

ingredientes_usuario = []

if entrada:

    ingredientes_usuario = [
        normalizar_ingrediente(ingrediente)
        for ingrediente in entrada.split(",")
        if ingrediente.strip()
    ]

    ingredientes_usuario = list(
        dict.fromkeys(ingredientes_usuario)
    )
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


    # NORMALIZAR INGREDIENTES DE LA RECETA

    ingredientes_receta = [
        normalizar_ingrediente(ingrediente)
        for ingrediente in receta["ingredientes"]
    ]

    ingredientes_receta = list(
        dict.fromkeys(ingredientes_receta)
    )


    # CALCULAR COINCIDENCIAS

    coincidencias = 0

    for ingrediente in ingredientes_usuario:

        if ingrediente in ingredientes_receta:

            coincidencias += 1


    # SI NO HAY INGREDIENTES, NO CONTINUAR

    if not ingredientes_receta:
        continue


    # PORCENTAJE DE INGREDIENTES QUE TIENE EL USUARIO

    porcentaje = (
        coincidencias / len(ingredientes_receta)
    ) * 100


    # INGREDIENTES FALTANTES

    faltantes = []

    for ingrediente in ingredientes_receta:

        if ingrediente not in ingredientes_usuario:

            faltantes.append(ingrediente)


    # SOLO MOSTRAR RECETAS CON COINCIDENCIAS

    if coincidencias > 0:


        # 1. COINCIDENCIA DE INGREDIENTES
        puntos_coincidencia = porcentaje * 0.65


        # 2. CANTIDAD DE INGREDIENTES FALTANTES
        if len(faltantes) == 0:

            puntos_faltantes = 20

        elif len(faltantes) == 1:

            puntos_faltantes = 15

        elif len(faltantes) == 2:

            puntos_faltantes = 10

        elif len(faltantes) == 3:

            puntos_faltantes = 5

        else:

            puntos_faltantes = 0


        # 3. TIEMPO DE PREPARACIÓN

        if receta["tiempo"] <= 10:

            puntos_tiempo = 10

        elif receta["tiempo"] <= 20:

            puntos_tiempo = 8

        elif receta["tiempo"] <= 30:

            puntos_tiempo = 5

        else:

            puntos_tiempo = 2


        # 4. NIVEL DE DIFICULTAD

        if receta["nivel"] == "Principiante":

            puntos_nivel = 5

        elif receta["nivel"] == "Explorador":

            puntos_nivel = 4

        else:

            puntos_nivel = 3


        # PUNTUACIÓN TOTAL

        puntuacion = (
            puntos_coincidencia
            + puntos_faltantes
            + puntos_tiempo
            + puntos_nivel
        )


        # ASEGURAR QUE ESTÉ ENTRE 0 Y 100

        puntuacion = max(
            0,
            min(100, round(puntuacion))
        )


        # GUARDAR RESULTADO

        resultados.append(
            {
                "receta": receta,
                "porcentaje": porcentaje,
                "faltantes": faltantes,
                "coincidencias": coincidencias,
                "puntuacion": puntuacion
            }
        )



resultados.sort(
    key=lambda resultado: (
        resultado["puntuacion"],
        resultado["porcentaje"],
        resultado["coincidencias"],
        -resultado["receta"]["tiempo"]
    ),
    reverse=True
)





if ingredientes_usuario:

    st.markdown('<div class="linea"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="titulo-resultados">Recetas encontradas</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="descripcion-resultados">'
        'Resultados ordenados según los ingredientes disponibles.'
        '</div>',
        unsafe_allow_html=True
    )


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

                st.markdown('<div class="linea"></div>',
                            unsafe_allow_html=True)


                if nivel == "Principiante":

                    st.subheader("Principiante")

                    st.write(
                        "Recetas sencillas para comenzar."
                    )


                elif nivel == "Explorador":

                    st.subheader("Explorador")

                    st.write(
                        "Recetas para descubrir nuevas combinaciones."
                    )


                elif nivel == "Experto":

                    st.subheader("Experto")

                    st.write(
                        "Recetas para experimentar y crear."
                    )


                columnas = st.columns(3)



                for posicion, resultado in enumerate(
                    recetas_nivel
                ):

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



                            st.subheader(
                                receta["nombre"]
                            )



                            st.write(
                                round(porcentaje),
                                "% de coincidencia"
                            )


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



                            if porcentaje == 100:

                                st.success(
                                    "Tienes todos los ingredientes."
                                )


                            elif porcentaje >= 75:

                                st.info(
                                    "Casi tienes todo."
                                )


                            elif porcentaje >= 50:

                                st.warning(
                                    "Faltan algunos ingredientes."
                                )


                            else:

                                st.write(
                                    "Necesitas varios ingredientes."
                                )



                            if faltantes:

                                st.write(
                                    "Te faltan:",
                                    ", ".join(faltantes)
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
                                key="ver_" + receta["nombre"]
                            ):

                                st.divider()


                                st.subheader(
                                    receta["nombre"]
                                )


                                st.write(
                                    "Ingredientes"
                                )


                                for ingrediente in receta["ingredientes"]:

                                    st.write(
                                        "•",
                                        ingrediente
                                    )


                                st.write(
                                    "Preparación"
                                )


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
            "No encontramos recetas que coincidan "
            "con tus ingredientes."
        )



else:

    st.info(
        "Escribe algunos ingredientes para comenzar."
    )



st.markdown(
    """
    <div class="footer">
        CHEF CERO RESIDUOS · Aprovechamiento de alimentos
    </div>
    """,
    unsafe_allow_html=True
)
