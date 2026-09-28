import streamlit as st
import streamlit.components.v1 as components
import recetas as modulo_recetas
import os
import json

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

# Inicializar estados de la sesión
if "favoritos" not in st.session_state or not isinstance(st.session_state.favoritos, list):
    st.session_state.favoritos = []

if "favoritos_cargados" not in st.session_state:
    st.session_state.favoritos_cargados = False

if "receta_modal" not in st.session_state:
    st.session_state.receta_modal = None


# ============================================================
# PERSISTENCIA CON LOCALSTORAGE (GUARDAR FAVORITOS)
# ============================================================

def sincronizar_localstorage():
    """Maneja la lectura y escritura de favoritos en el navegador."""
    if not st.session_state.favoritos_cargados:
        html_code = """
        <script>
            const favs = localStorage.getItem('favoritos_chef');
            if (favs) {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: JSON.parse(favs)
                }, '*');
            } else {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: []
                }, '*');
            }
        </script>
        """
        favs_recuperados = components.html(html_code, height=0, width=0)
        if favs_recuperados is not None and isinstance(favs_recuperados, list):
            st.session_state.favoritos = favs_recuperados
            st.session_state.favoritos_cargados = True


def guardar_favorito_localstorage(lista_favoritos):
    """Guarda la lista de favoritos en el navegador."""
    json_favs = json.dumps(lista_favoritos)
    html_code = f"""
    <script>
        localStorage.setItem('favoritos_chef', '{json_favs}');
    </script>
    """
    components.html(html_code, height=0, width=0)


# Ejecutar la sincronización al inicio
sincronizar_localstorage()


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
    /* Fondo general */
    .stApp { background-color: #F5F1E8; }
    
    /* Contenedor principal */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }

    /* PANTALLA DE INICIO EN PANTALLA COMPLETA */
    .hero-fullscreen {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        min-height: calc(85vh - 50px);
        background-color: #26352B;
        border-radius: 16px;
        color: #F5F1E8;
        padding: 40px 20px;
        margin-top: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .hero-title {
        font-family: 'Georgia', serif;
        font-size: 58px;
        font-weight: 700;
        letter-spacing: 4px;
        margin-bottom: 60px;
        color: #F5F1E8;
        text-transform: uppercase;
        line-height: 1.25;
    }
    
    .hero-slogan {
        font-family: 'Georgia', serif;
        font-size: 38px;
        margin-bottom: 60px;
        color: #E2DDD0;
    }
    
    .hero-subtitle {
        font-family: 'Georgia', serif;
        font-size: 34px;
        font-weight: 300;
        letter-spacing: 1px;
        color: #D7D0C2;
    }

    /* ESTILO ENCABEZADO MENÚ */
    .menu-header {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 20px;
    }
    .menu-header h1 {
        font-family: 'Georgia', serif;
        font-size: 40px;
        font-weight: bold;
        letter-spacing: 3px;
        color: #26352B;
        text-transform: uppercase;
        margin: 0;
    }

    /* TARJETAS CON BORDE NEGRO RECTANGULAR PARA EL MENÚ */
    .card-menu {
        border: 3px solid #000000 !important;
        border-radius: 0px !important;
        background-color: #FFFFFF;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 4px 4px 0px #000000;
    }

    /* Estilos para las tarjetas de la grilla del Buscador */
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

    /* RESETEAR COLORES DE LAS PESTAÑAS (TABS) */
    button[data-baseweb="tab"] {
        color: #26352B !important;
        font-weight: 600;
        font-size: 16px;
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
# RENDERIZADORES DE RECURSOS
# ============================================================

def mostrar_grilla_recetas(lista_items, prefijo_key, num_cols=3):
    cols = st.columns(num_cols)
    
    for idx, item in enumerate(lista_items):
        receta = item["receta"]
        porcentaje = item.get("porcentaje", None)

        with cols[idx % num_cols]:
            with st.container(border=True):
                ruta_imagen = os.path.join(os.path.dirname(__file__), receta.get("imagen", ""))
                if os.path.exists(ruta_imagen):
                    st.image(ruta_imagen, use_container_width=True)
                else:
                    st.write("🍳")

                if porcentaje is not None:
                    porcentaje_round = round(porcentaje)
                    badge_color = "#28a745" if porcentaje_round == 100 else ("#17a2b8" if porcentaje_round >= 75 else "#ffc107")
                    st.markdown(
                        f'<span class="badge-match" style="background-color: {badge_color};">{porcentaje_round}% Match</span>',
                        unsafe_allow_html=True
                    )

                st.subheader(receta["nombre"])
                st.caption(f"⏱️ {receta['tiempo']} min | 📊 {receta['nivel']}")

                if st.button("Ver receta", key=f"btn_{prefijo_key}_{idx}_{receta['nombre']}"):
                    st.session_state.receta_modal = receta
                    st.rerun()


def mostrar_menu_categoria(categoria_nombre, subcategoria=None):
    """Muestra las recetas filtrando por categoría principal y opcionalmente por subcategoría."""
    recetas_filtradas = []
    
    for r in recetas:
        cat_match = r.get("categoria", "").lower() == categoria_nombre.lower()
        sub_match = True
        if subcategoria:
            sub_match = r.get("subcategoria", "").lower() == subcategoria.lower()
        
        if cat_match and sub_match:
            recetas_filtradas.append({"receta": r})
    
    if recetas_filtradas:
        mostrar_grilla_recetas(recetas_filtradas, f"menu_{categoria_nombre}_{subcategoria or 'gen'}", num_cols=2)
    else:
        etiqueta = f"{categoria_nombre} > {subcategoria}" if subcategoria else categoria_nombre
        st.info(f"Aún no hay recetas registradas en '{etiqueta}'. Muestrario de prueba:")
        recetas_demo = [{"receta": r} for r in recetas[:6]]
        mostrar_grilla_recetas(recetas_demo, f"menu_demo_{categoria_nombre}_{subcategoria or 'gen'}", num_cols=2)


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
            guardar_favorito_localstorage(st.session_state.favoritos)
            st.rerun()
    else:
        if st.button("🤍 Guardar en Favoritos"):
            st.session_state.favoritos.append(receta["nombre"])
            guardar_favorito_localstorage(st.session_state.favoritos)
            st.rerun()


if st.session_state.receta_modal:
    mostrar_modal_receta(st.session_state.receta_modal)
    st.session_state.receta_modal = None


# ============================================================
# INTERFAZ PRINCIPAL Y NAVEGACIÓN
# ============================================================

num_favoritos = len(st.session_state.favoritos) if isinstance(st.session_state.favoritos, list) else 0

tab_inicio, tab_menu, tab_buscador, tab_favoritos = st.tabs([
    "🏠 Inicio", 
    "📖 Menú",
    "🔍 Buscador", 
    f"❤️ Favoritos ({num_favoritos})"
])

# ------------------------------------------------------------
# 1. PESTAÑA DE INICIO
# ------------------------------------------------------------
with tab_inicio:
    st.markdown(
        """
        <div class="hero-fullscreen">
            <div class="hero-title">CHEF CERO<br>RESIDUOS</div>
            <div class="hero-slogan">No solo cocines.</div>
            <div class="hero-subtitle">Aprovecha, descubre y comparte.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------------------------------------------
# 2. PESTAÑA DE MENÚ (FIEL A LAS DIAPOSITIVAS)
# ------------------------------------------------------------
with tab_menu:
    st.markdown(
        """
        <div class="menu-header">
            <h1>CHEF CERO RESIDUOS</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_comida, tab_postres, tab_extras, tab_bebidas = st.tabs([
        "Comida", "Postres", "Extras", "Bebidas"
    ])

    with tab_comida:
        mostrar_menu_categoria("Comida")

    with tab_postres:
        mostrar_menu_categoria("Postres")

    # SUB-SECCIÓN DE EXTRAS: BOTANAS | FIT | OTROS
    with tab_extras:
        tab_botanas, tab_fit, tab_otros = st.tabs([
            "Botanas", "Fit", "Otros"
        ])
        
        with tab_botanas:
            mostrar_menu_categoria("Extras", "Botanas")
            
        with tab_fit:
            mostrar_menu_categoria("Extras", "Fit")
            
        with tab_otros:
            mostrar_menu_categoria("Extras", "Otros")

    with tab_bebidas:
        mostrar_menu_categoria("Bebidas")

# ------------------------------------------------------------
# 3. PESTAÑA DEL BUSCADOR
# ------------------------------------------------------------
with tab_buscador:
    st.subheader("🔍 Buscador Inteligente de Recetas")
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
            orden_niveles = ["Principiante", "Explorador", "Intermedio", "Experto"]
            niveles_disponibles = [n for n in orden_niveles if any(r["receta"]["nivel"] == n for r in resultados)]

            tabs_niveles = st.tabs([f"📌 {n}" for n in niveles_disponibles])

            for idx, nivel in enumerate(niveles_disponibles):
                with tabs_niveles[idx]:
                    recetas_sub = [r for r in resultados if r["receta"]["nivel"] == nivel]
                    mostrar_grilla_recetas(recetas_sub, f"grilla_{idx}")
        else:
            st.info("No se encontraron recetas con esos filtros.")

# ------------------------------------------------------------
# 4. PESTAÑA DE FAVORITOS
# ------------------------------------------------------------
with tab_favoritos:
    st.subheader("❤️ Tus Recetas Guardadas")
    if st.session_state.favoritos:
        fav_recetas = [{"receta": r, "porcentaje": 100} for r in recetas if r["nombre"] in st.session_state.favoritos]
        mostrar_grilla_recetas(fav_recetas, "favs")
    else:
        st.info("Aún no has guardado recetas favoritas.")
