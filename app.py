import streamlit as st
import recetas as modulo_recetas
import os

recetas = modulo_recetas.recetas

st.set_page_config(
    page_title="Chef Cero Residuos",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# NORMALIZAR INGREDIENTES
# ============================================================

def normalizar_ingrediente(ingrediente):

    ingrediente = ingrediente.strip().lower()

    # Quitar signos básicos
    ingrediente = ingrediente.replace(",", "")
    ingrediente = ingrediente.replace(".", "")

    palabras = ingrediente.split()

    palabras_ignoradas = [
        "un", "una", "unos", "unas",
        "el", "la", "los", "las",
        "de", "del",
        "gramos", "gramo",
        "kg", "kilo", "kilos",
        "g",
        "ml",
        "litro", "litros",
        "taza", "tazas",
        "cucharada", "cucharadas",
        "cucharadita", "cucharaditas",
        "barra", "barras",
        "paquete", "paquetes",
        "lata", "latas",
        "sobre", "sobres",
        "pieza", "piezas"
    ]

    palabras_limpias = []

    for palabra in palabras:

        palabra_limpia = palabra.strip(".,;:()")

        # Eliminar cantidades como:
        # 1, 2, 3
        # 1/2, 1/4
        if palabra_limpia.isdigit():
            continue

        if "/" in palabra_limpia:
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

        "ajos": "ajo",

        "mangos": "mango",
        "fresas": "fresa",
        "peras": "pera",
        "duraznos": "durazno",
        "cerezas": "cereza",
        "nueces": "nuez",
        "almendras": "almendra",
        "galletas": "galleta"
    }

    if ingrediente in equivalencias:
        return equivalencias[ingrediente]

    # Plural simple
    if ingrediente.endswith("s") and len(ingrediente) > 3:
        ingrediente = ingrediente[:-1]

    return ingrediente


# ============================================================
# ESTILOS
# ============================================================

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


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    """
    <div class="marca">
        <h1>CHEF CERO RESIDUOS</h1>
        <p>No solo cocines. Aprovecha, descubre y comparte.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="linea"></div>',
    unsafe_allow_html=True
)


# ============================================================
# SECCIÓN DE BÚSQUEDA
# ============================================================

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


# ============================================================
# FILTROS
# ============================================================

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
            "Intermedio",
            "Explorador",
            "Experto"
        ]
    )


# ============================================================
# INGREDIENTES DEL USUARIO
# ============================================================

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


# ============================================================
# BUSCAR RECETAS
# ============================================================

resultados = []


if ingredientes_usuario:

    for receta in recetas:

        # ----------------------------------------------------
        # FILTRO DE TIEMPO
        # ----------------------------------------------------

        if filtro_tiempo == "10 minutos":

            if receta["tiempo"] > 10:
                continue

        elif filtro_tiempo == "20 minutos":

            if receta["tiempo"] > 20:
