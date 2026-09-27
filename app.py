import streamlit as st
import recetas as modulo_recetas
import os

# Configuración de página
st.set_page_config(
    page_title="Chef Cero Residuos",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cargar base de datos
recetas = modulo_recetas.recetas

# Inicializar estado para Favoritos y Receta Seleccionada
if "favoritos" not in st.session_state:
    st.session_state.favoritos = []

if "receta_seleccionada" not in st.session_state:
    st.session_state.receta_seleccionada = None

# ============================================================
# NORMALIZAR INGREDIENTES (CON CACHÉ)
# ============================================================

@st.cache_data
def normalizar_ingrediente(ingrediente):
    ingrediente = ingrediente.strip().lower()
    ingrediente = ingrediente.replace(",", "").replace(".", "")

    palabras = ingrediente.split()
    palabras_ignoradas = [
        "un", "una", "unos", "unas", "el", "la", "los", "las", "de", "del",
        "gramos", "gramo", "kg", "kilo", "kilos", "g", "ml", "litro", "litros",
        "taza", "tazas", "cucharada", "cucharadas", "cucharadita", "cucharaditas",
        "barra", "barras", "paquete", "paquetes", "lata", "latas", "sobre", "sobres", "pieza", "piezas"
    ]

    palabras_limpias = []
    for palabra in palabras:
        palabra_limpia = palabra.strip(".,;:()")
        if palabra_limpia.isdigit() or "/" in palabra_limpia:
            continue
        if palabra_limpia not in palabras_ignoradas:
            palabras_limpias.append(palabra_limpia)

    ingrediente = " ".join(palabras_limpias)

    equivalencias = {
        "jitomate": "tomate", "jitomates": "tomate", "tomates": "tomate",
        "huevos": "huevo", "tortillas": "tortilla", "quesos": "queso",
        "cebollas": "cebolla", "papas": "papa", "patatas": "papa",
        "zanahorias": "zanahoria", "aceites": "aceite", "chiles": "chile",
        "limones": "limon", "limón": "limon", "ajos": "ajo",
        "mangos": "mango", "fresas": "fresa", "peras": "pera",
        "duraznos": "durazno", "cerezas": "cereza", "nueces": "nuez",
        "almendras": "almendra", "galletas": "galleta"
    }

    if ingrediente in equivalencias:
        return equivalencias[ingrediente]

    if ingrediente.endswith("s") and len(ingrediente) > 3:
        ingrediente = ingrediente[:-1]

    return ingrediente


# ============================================================
# ESTILOS Y CURSOR PERSONALIZADO
# ============================================================

st.markdown(
    """
    <style>
    body {
        cursor: url('https://img.icons8.com/emoji/32/pizza-emoji.png'), auto !important;
    }

    .stApp {
        background-color: #F5F1E8;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 35px;
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
        margin: 25px 0;
    }

    .seccion-busqueda {
        text-align: center;
        margin-bottom: 25px;
    }

    .seccion-busqueda h2 {
        font-size: 28px;
        color: #26352B;
        margin-bottom: 8px;
    }

    div[data-testid="stTextInput"] input {
        border: 1px solid #C9C2B5;
        border-radius: 12px;
        background-color: #FFFFFF;
        padding: 14px;
        font-size: 16px;
    }

    .stButton > button {
        border-radius: 10px;
        background-color: #536B59;
        color: white;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #3F5545;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# MODAL/POPUP PARA VER RECETA DETALLADA
# ============================================================

@st.dialog("Detalles de la Receta")
def mostrar_modal_receta(receta):
    ruta_imagen = os.path.join(os.path.dirname(__file__), receta["imagen"])
    if os.path.exists(ruta_imagen):
        st.image(ruta_imagen, use_container_width=True)
    
    st.title(receta["nombre"])
    st.write(f"⏱️ **Tiempo:** {receta['tiempo']} minutos | 📊 **Nivel:** {receta['nivel']}")
    st.caption(receta.get("descripcion", ""))

    st.divider()

    st.subheader("🛒 Ingredientes")
    for ing in receta["ingredientes"]:
        st.write(f"• {ing.capitalize()}")

    st.divider()

    st.subheader("👩‍🍳 Instrucciones de Preparación")
    for i, paso in enumerate(receta.get("instrucciones", []), start=1):
        st.write(f"**{i}.** {paso}")

    es_favorito = receta["nombre"] in st.session_state.favoritos
    if es_favorito:
        if st.button("❤️ Quitar de Favoritos"):
            st.session_state.favoritos.remove(receta["nombre"])
            st.rerun()
    else:
        if st.button("🤍 Guardar en Favoritos"):
            st.session_state.favoritos.append(receta["nombre"])
            st.rerun()


# Abrir modal si hay una receta seleccionada en el session_state
if st.session_state.receta_seleccionada:
    mostrar_modal_receta(st.session_state.receta_seleccionada)
    st.session_state.receta_seleccionada = None


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

st.markdown('<div class="linea"></div>', unsafe_allow_html=True)

tab_buscador, tab_favoritos = st.tabs(["🔍 Buscador Inteligente", f"❤️ Mis Favoritos ({len(st.session_state.favoritos)})"])

with tab_buscador:
    st.markdown(
        """
        <div class="seccion-busqueda">
            <h2>Busca una receta</h2>
            <p>Escribe los ingredientes que tienes disponibles separados por comas.</p>
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
            ["Todos", "10 minutos", "20 minutos", "30+ minutos"]
        )

    with columna_nivel:
        filtro_nivel = st.selectbox(
            "Nivel de dificultad",
            ["Todos", "Principiante", "Intermedio", "Explorador", "Experto"]
        )

    ingredientes_usuario = []
    if entrada:
        ingredientes_usuario = [
            normalizar_ingrediente(ing)
            for ing in entrada.split(",") if ing.strip()
        ]
        ingredientes_usuario = list(dict.fromkeys(ingredientes_usuario))

    resultados = []

    if ingredientes_usuario:
        for receta in recetas:
            if filtro_tiempo == "10 minutos" and receta["tiempo"] > 10:
                continue
            elif filtro_tiempo == "20 minutos" and receta["tiempo"] > 20:
                continue
            elif filtro_tiempo == "30+ minutos" and receta["tiempo"] < 30:
                continue

            if filtro_nivel != "Todos" and receta["nivel"] != filtro_nivel:
                continue

            ingredientes_receta = [normalizar_ingrediente(ing) for ing in receta["ingredientes"]]
            ingredientes_receta = list(dict.fromkeys(ingredientes_receta))

            coincidencias = 0
            for ing_user in ingredientes_usuario:
                for ing_receta in ingredientes_receta:
                    if ing_user == ing_receta or ing_user in ing_receta.split():
                        coincidencias += 1
                        break

            if not ingredientes_receta or coincidencias == 0:
                continue

            porcentaje = (coincidencias / len(ingredientes_receta)) * 100
            faltantes = [ing for ing in ingredientes_receta if ing not in ingredientes_usuario]

            puntos_coincidencia = porcentaje * 0.65
            puntos_faltantes = max(0, 20 - (len(faltantes) * 5))
            puntos_tiempo = 10 if receta["tiempo"] <= 10 else (8 if receta["tiempo"] <= 20 else 5)
            puntos_nivel = 5 if receta["nivel"] == "Principiante" else 4

            puntuacion = min(100, round(puntos_coincidencia + puntos_faltantes + puntos_tiempo + puntos_nivel))

            resultados.append({
                "receta": receta,
                "porcentaje": porcentaje,
                "faltantes": faltantes,
                "coincidencias": coincidencias,
                "puntuacion": puntuacion
            })

        resultados.sort(
            key=lambda r: (r["puntuacion"], r["porcentaje"], r["coincidencias"], -r["receta"]["tiempo"]),
            reverse=True
        )

        st.markdown('<div class="linea"></div>', unsafe_allow_html=True)
        st.markdown(f"### 🍽️ Recetas encontradas ({len(resultados)})")

        if resultados:
            niveles = ["Principiante", "Intermedio", "Explorador", "Experto"]

            for nivel in niveles:
                recetas_nivel = [res for res in resultados if res["receta"]["nivel"] == nivel]

                if recetas_nivel:
                    st.markdown('<div class="linea"></div>', unsafe_allow_html=True)
                    st.subheader(f"📌 {nivel}")

                    # Crear el carrusel horizontal mediante contenedor expandible/deslizable
                    carrusel_cols = st.columns(len(recetas_nivel))

                    # Para evitar que se comprima si hay muchas, usamos columnas de ancho controlado
                    with st.container():
                        cols = st.columns(min(len(recetas_nivel), 4))
                        for idx, res in enumerate(recetas_nivel):
                            receta = res["receta"]
                            porcentaje = res["porcentaje"]
                            faltantes = res["faltantes"]

                            with cols[idx % len(cols)]:
                                with st.container(border=True):
                                    ruta_imagen = os.path.join(os.path.dirname(__file__), receta["imagen"])
                                    if os.path.exists(ruta_imagen):
                                        st.image(ruta_imagen, use_container_width=True)

                                    st.subheader(receta["nombre"])
                                    
                                    if porcentaje == 100:
                                        st.success("🟢 100% Match")
                                    elif porcentaje >= 75:
                                        st.info(f"🟡 {round(porcentaje)}% Match")
                                    else:
                                        st.warning(f"🟠 {round(porcentaje)}% Match")

                                    st.caption(f"⏱️ {receta['tiempo']} min")

                                    if faltantes:
                                        st.caption(f"**Te falta:** {', '.join(faltantes)}")
                                    else:
                                        st.caption("✨ **¡Tienes todo!**")

                                    if st.button("Ver receta", key=f"btn_{nivel}_{receta['nombre']}"):
                                        st.session_state.receta_seleccionada = receta
                                        st.rerun()
        else:
            st.info("No se encontraron recetas con esos ingredientes y filtros.")


# ============================================================
# TAB DE FAVORITOS
# ============================================================

with tab_favoritos:
    st.subheader("❤️ Tus Recetas Guardadas")
    if st.session_state.favoritos:
        fav_recetas = [r for r in recetas if r["nombre"] in st.session_state.favoritos]
        
        cols_fav = st.columns(3)
        for idx, receta in enumerate(fav_recetas):
            with cols_fav[idx % 3]:
                with st.container(border=True):
                    ruta_imagen = os.path.join(os.path.dirname(__file__), receta["imagen"])
                    if os.path.exists(ruta_imagen):
                        st.image(ruta_imagen, use_container_width=True)
                    st.subheader(receta["nombre"])
                    st.caption(f"⏱️ {receta['tiempo']} min | 📈 {receta['nivel']}")
                    
                    if st.button("Ver receta", key=f"fav_btn_{receta['nombre']}"):
                        st.session_state.receta_seleccionada = receta
                        st.rerun()
    else:
        st.info("Aún no has guardado recetas favoritas. ¡Explora en el buscador y haz clic en 'Guardar en Favoritos'!")
    
