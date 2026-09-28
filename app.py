import streamlit as st
import recetas as modulo_recetas
import os

# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================

st.set_page_config(
    page_title="Chef Cero Residuos",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

recetas = modulo_recetas.recetas

if "favoritos" not in st.session_state:
    st.session_state.favoritos = []

if "receta_modal" not in st.session_state:
    st.session_state.receta_modal = None


# ============================================================
# NORMALIZAR INGREDIENTES
# ============================================================

@st.cache_data
def normalizar_ingrediente(ingrediente):
    ingrediente = ingrediente.strip().lower().replace(",", "").replace(".", "")
    palabras = ingrediente.split()
    ignoradas = [
        "un", "una", "unos", "unas", "el", "la", "los", "las", "de", "del",
        "gramos", "gramo", "kg", "kilo", "kilos", "g", "ml", "litro", "litros",
        "taza", "tazas", "cucharada", "cucharadas", "cucharadita", "cucharaditas",
        "barra", "barras", "paquete", "paquetes", "lata", "latas", "sobre", "sobres", "pieza", "piezas"
    ]
    limpias = [p.strip(".,;:()") for p in palabras if not p.isdigit() and "/" not in p and p not in ignoradas]
    ingrediente = " ".join(limpias)

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
        return ingrediente[:-1]
    return ingrediente


# ============================================================
# ESTILOS CSS GENERALES Y CORRECCIÓN DE COLORES
# ============================================================

st.markdown(
    """
    <style>
    .stApp { background-color: #F5F1E8; }
    .block-container { max-width: 1200px; padding-top: 30px; padding-bottom: 60px; }
    .marca { text-align: center; margin-bottom: 8px; }
    .marca h1 { font-size: 42px; font-weight: 800; letter-spacing: 2px; margin-bottom: 5px; color: #26352B; }
    .marca p { font-size: 16px; color: #59645C; margin-top: 0; }
    .linea { height: 1px; background-color: #D7D0C2; margin: 20px 0; }
    
    /* Estilos para las tarjetas de la grilla */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #DED8CC !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.04);
    }
    
    .badge-match {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
        color: white;
        margin-bottom: 8px;
    }

    .stButton > button {
        border-radius: 8px;
        background-color: #536B59;
        color: white;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover { background-color: #3F5545; color: white; }

    /* RESETEAR COLORES DE LAS PESTAÑAS (TABS) PARA EVITAR TEXTO EN ROJO */
    button[data-baseweb="tab"] {
        color: #26352B !important;
        font-weight: 600;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #536B59 !important;
        border-bottom-color: #536B59 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# RENDERIZADOR EN REJILLA/GRILLA (3 COLUMNAS)
# ============================================================

def mostrar_grilla_recetas(lista_items, prefijo_key):
    cols = st.columns(3) # 3 tarjetas por fila
    
    for idx, item in enumerate(lista_items):
        receta = item["receta"]
        porcentaje = round(item["porcentaje"])
        badge_color = "#28a745" if porcentaje == 100 else ("#17a2b8" if porcentaje >= 75 else "#ffc107")

        with cols[idx % 3]:
            with st.container(border=True):
                # Imagen
                ruta_imagen = os.path.join(os.path.dirname(__file__), receta.get("imagen", ""))
                if os.path.exists(ruta_imagen):
                    st.image(ruta_imagen, use_container_width=True)
                else:
                    st.write("🍳")

                # Match
                st.markdown(
                    f'<span class="badge-match" style="background-color: {badge_color};">{porcentaje}% Match</span>',
                    unsafe_allow_html=True
                )

                st.subheader(receta["nombre"])
                st.caption(f"⏱️ {receta['tiempo']} min | 📊 {receta['nivel']}")

                # Botón ver receta nativo
                if st.button("Ver receta", key=f"btn_{prefijo_key}_{idx}_{receta['nombre']}"):
                    st.session_state.receta_modal = receta
                    st.rerun()


# ============================================================
# MODAL DE RECETA
# ============================================================

@st.dialog("Detalles de la Receta")
def mostrar_modal_receta(receta):
    ruta_imagen = os.path.join(os.path.dirname(__file__), receta.get("imagen", ""))
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


if st.session_state.receta_modal:
    mostrar_modal_receta(st.session_state.receta_modal)
    st.session_state.receta_modal = None


# ============================================================
# INTERFAZ PRINCIPAL
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
    entrada = st.text_input(
        "Ingredientes disponibles",
        placeholder="Ejemplo: huevo, tomate, queso",
        key="input_ingredientes"
    )

    col1, col2 = st.columns(2)
    with col1:
        filtro_tiempo = st.selectbox("Tiempo disponible", ["Todos", "10 minutos", "20 minutos", "30+ minutos"])
    with col2:
        filtro_nivel = st.selectbox("Nivel de dificultad", ["Todos", "Principiante", "Explorador", "Intermedio", "Experto"])

    ingredientes_usuario = []
    if entrada:
        ingredientes_usuario = [normalizar_ingrediente(ing) for ing in entrada.split(",") if ing.strip()]
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

            coincidencias = sum(1 for ing_user in ingredientes_usuario if any(ing_user == ing_receta or ing_user in ing_receta.split() for ing_receta in ingredientes_receta))

            if not ingredientes_receta or coincidencias == 0:
                continue

            porcentaje = (coincidencias / len(ingredientes_receta)) * 100
            resultados.append({"receta": receta, "porcentaje": porcentaje})

        resultados.sort(key=lambda r: r["porcentaje"], reverse=True)

        st.markdown('<div class="linea"></div>', unsafe_allow_html=True)
        st.markdown(f"### 🍽️ Recetas Recomendadas ({len(resultados)})")

        if resultados:
            # Orden estricto definido por el usuario
            orden_niveles = ["Principiante", "Explorador", "Intermedio", "Experto"]
            niveles_disponibles = [n for n in orden_niveles if any(r["receta"]["nivel"] == n for r in resultados)]

            tabs_niveles = st.tabs([f"📌 {n}" for n in niveles_disponibles])

            for idx, nivel in enumerate(niveles_disponibles):
                with tabs_niveles[idx]:
                    recetas_sub = [r for r in resultados if r["receta"]["nivel"] == nivel]
                    mostrar_grilla_recetas(recetas_sub, f"grilla_{idx}")
        else:
            st.info("No se encontraron recetas con esos filtros.")


with tab_favoritos:
    st.subheader("❤️ Tus Recetas Guardadas")
    if st.session_state.favoritos:
        fav_recetas = [{"receta": r, "porcentaje": 100} for r in recetas if r["nombre"] in st.session_state.favoritos]
        mostrar_grilla_recetas(fav_recetas, "favs")
    else:
        st.info("Aún no has guardado recetas favoritas.")
                
