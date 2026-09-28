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
# ESTILOS CSS GENERALES
# ============================================================

st.markdown(
    """
    <style>
    .stApp { background-color: #F5F1E8; }
    .block-container { max-width: 1000px; padding-top: 30px; padding-bottom: 60px; }
    .marca { text-align: center; margin-bottom: 8px; }
    .marca h1 { font-size: 42px; font-weight: 800; letter-spacing: 2px; margin-bottom: 5px; color: #26352B; }
    .marca p { font-size: 16px; color: #59645C; margin-top: 0; }
    .linea { height: 1px; background-color: #D7D0C2; margin: 20px 0; }
    
    /* Estilo para los bloques desplegables */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF;
        border-radius: 10px;
        border: 1px solid #DED8CC !important;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }

    .stButton > button {
        border-radius: 8px;
        background-color: #536B59;
        color: white;
        font-weight: 600;
    }
    .stButton > button:hover { background-color: #3F5545; color: white; }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# RENDERIZADOR EN ACORDEÓN / DESPLEGABLE
# ============================================================

def mostrar_lista_acordeon(lista_items, prefijo_key):
    for idx, item in enumerate(lista_items):
        receta = item["receta"]
        porcentaje = round(item["porcentaje"])
        
        # Emoji / indicador según porcentaje
        match_str = f"🟢 {porcentaje}% Match" if porcentaje == 100 else (f"🔵 {porcentaje}% Match" if porcentaje >= 75 else f"🟡 {porcentaje}% Match")
        
        # Título formateado para la barra del acordeón
        titulo_expander = f"🍽️ {receta['nombre']}  —  {match_str} | ⏱️ {receta['tiempo']} min | 📊 {receta['nivel']}"

        with st.expander(titulo_expander):
            col_img, col_info = st.columns([1, 2])

            with col_img:
                ruta_imagen = os.path.join(os.path.dirname(__file__), receta.get("imagen", ""))
                if os.path.exists(ruta_imagen):
                    st.image(ruta_imagen, use_container_width=True)
                else:
                    st.write("🍳 (Sin imagen)")

            with col_info:
                st.caption(receta.get("descripcion", ""))
                
                # Botón de Favoritos integrado dentro del mismo desplegable
                es_fav = receta["nombre"] in st.session_state.favoritos
                if es_fav:
                    if st.button("❤️ Quitar de Favoritos", key=f"fav_{prefijo_key}_{idx}_{receta['nombre']}"):
                        st.session_state.favoritos.remove(receta["nombre"])
                        st.rerun()
                else:
                    if st.button("🤍 Guardar en Favoritos", key=f"fav_{prefijo_key}_{idx}_{receta['nombre']}"):
                        st.session_state.favoritos.append(receta["nombre"])
                        st.rerun()

            st.divider()

            col_ing, col_inst = st.columns([1, 2])

            with col_ing:
                st.markdown("#### 🛒 Ingredientes")
                for ing in receta["ingredientes"]:
                    st.write(f"• {ing.capitalize()}")

            with col_inst:
                st.markdown("#### 👩‍🍳 Instrucciones")
                for i, paso in enumerate(receta.get("instrucciones", []), start=1):
                    st.write(f"**{i}.** {paso}")


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
        filtro_nivel = st.selectbox("Nivel de dificultad", ["Todos", "Principiante", "Intermedio", "Explorador", "Experto"])

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
        st.markdown(f"### 🍽️ Recetas Encontradas ({len(resultados)})")

        if resultados:
            niveles = ["Principiante", "Intermedio", "Explorador", "Experto"]

            for idx, nivel in enumerate(niveles):
                recetas_nivel = [r for r in resultados if r["receta"]["nivel"] == nivel]
                if recetas_nivel:
                    st.subheader(f"📌 {nivel}")
                    mostrar_lista_acordeon(recetas_nivel, f"acordeon_{idx}")
        else:
            st.info("No se encontraron recetas con esos filtros.")


with tab_favoritos:
    st.subheader("❤️ Tus Recetas Guardadas")
    if st.session_state.favoritos:
        fav_recetas = [{"receta": r, "porcentaje": 100} for r in recetas if r["nombre"] in st.session_state.favoritos]
        mostrar_lista_acordeon(fav_recetas, "favs")
    else:
        st.info("Aún no has guardado recetas favoritas.")
            
