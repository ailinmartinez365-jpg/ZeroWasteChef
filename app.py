import streamlit as st
import streamlit.components.v1 as components
import recetas as modulo_recetas
import os
import urllib.parse
import base64

# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Chef Cero Residuos",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cargar base de datos
recetas = modulo_recetas.recetas

# Inicializar favoritos
if "favoritos" not in st.session_state:
    st.session_state.favoritos = []


# ============================================================
# DETECTAR CLIC EN UNA RECETA
# ============================================================

query_params = st.query_params

if "receta_clic" in query_params:

    nombre_receta = query_params["receta_clic"]

    st.query_params.clear()

    for r in recetas:

        if r["nombre"] == nombre_receta:

            st.session_state.receta_modal = r

            break


# ============================================================
# IMAGEN A BASE64
# ============================================================

def obtener_base64_imagen(ruta_relativa):

    ruta_abs = os.path.join(
        os.path.dirname(__file__),
        ruta_relativa
    )

    if os.path.exists(ruta_abs):

        try:

            with open(ruta_abs, "rb") as image_file:

                encoded_string = base64.b64encode(
                    image_file.read()
                ).decode()

                ext = ruta_relativa.split(".")[-1].lower()

                if ext in ["jpg", "jpeg"]:
                    mime_type = "jpeg"
                else:
                    mime_type = ext

                return (
                    f"data:image/{mime_type};"
                    f"base64,{encoded_string}"
                )

        except Exception:

            return None

    return None


# ============================================================
# NORMALIZAR INGREDIENTES
# ============================================================

@st.cache_data
def normalizar_ingrediente(ingrediente):

    ingrediente = ingrediente.strip().lower()

    ingrediente = ingrediente.replace(",", "")
    ingrediente = ingrediente.replace(".", "")

    palabras = ingrediente.split()

    palabras_ignoradas = [
        "un", "una", "unos", "unas",
        "el", "la", "los", "las",
        "de", "del",
        "gramos", "gramo",
        "kg", "kilo", "kilos",
        "g", "ml",
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

        palabra_limpia = palabra.strip(
            ".,;:()"
        )

        if palabra_limpia.isdigit():
            continue

        if "/" in palabra_limpia:
            continue

        if palabra_limpia not in palabras_ignoradas:

            palabras_limpias.append(
                palabra_limpia
            )

    ingrediente = " ".join(
        palabras_limpias
    )

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

    if ingrediente.endswith("s") and len(ingrediente) > 3:
