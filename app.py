import os
import json
import streamlit as st
import streamlit.components.v1 as components
import recetas as modulo_recetas

# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================

st.set_page_config(
    page_title="Kitchen help",
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

# Estado para el cursor seleccionado por el usuario
if "cursor_actual" not in st.session_state:
    st.session_state.cursor_actual = "🍴"


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
# ESTILOS CSS REFORZADOS (COLORES DE LA PALETA)
# ============================================================

emoji_cursor = st.session_state.cursor_actual

st.markdown(
    f"""
    <style>
    /* CURSOR DINÁMICO PERSONALIZADO */
    html, body, .stApp, button, div, a, input {{
        cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><text y="24" font-size="22">{emoji_cursor}</text></svg>'), auto !important;
    }}

    /* FONDO GENERAL: Marfil #FFF8EA */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #FFF8EA !important;
        color: #4A2920 !important;
    }}
    
    /* Contenedor principal */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }}

    /* ENCABEZADOS Y TEXTOS PRINCIPALES: Chocolate #4A2920 */
    h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown {{
        color: #4A2920 !important;
    }}

    /* BANNER RESPONSIVO PARA 'KITCHEN HELP' */
    .kitchen-banner {{
        width: 100%;
        height: 180px;
        background-image: url('https://lh3.googleusercontent.com/d/1000066152.png');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center center;
        margin-bottom: 25px;
    }}

    @media (max-width: 768px) {{
        .kitchen-banner {{
            height: 100px;
        }}
    }}

    /* TARJETAS DE RECETAS Y DISEÑO: Blanco con borde Amarillo Mantequilla #F4C95D */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: #FFFFFF !important;
        border-radius: 14px !important;
        border: 2px solid #F4C95D !important;
        box-shadow: 0 4px 12px rgba(74, 41, 32, 0.08) !important;
    }}

    .icon-card {{
        border: 2px solid #4A2920;
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        font-size: 50px;
        margin-bottom: 10px;
        box-shadow: 4px 4px 0px #C65332;
    }}

    /* BOTONES PRINCIPALES: Terracota #C65332 */
    .stButton > button {{
        border-radius: 8px !important;
        background-color: #C65332 !important;
        color: #FFF8EA !important;
        font-weight: 600 !important;
        border: none !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button:hover {{ 
        background-color: #F4C95D !important; 
        color: #4A2920 !important;
    }}
    .stButton > button * {{
        color: inherit !important;
    }}

    /* PESTAÑAS (TABS): Chocolate y Terracota */
    button[data-baseweb="tab"] {{
        background-color: transparent !important;
        border-radius: 6px 6px 0 0 !important;
    }}
    button[data-baseweb="tab"] p {{
        color: #4A2920 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        border-bottom-color: #C65332 !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] p {{
        color: #C65332 !important;
    }}

    .badge-match {{
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
        color: white !important;
        margin-bottom: 8px;
    }}

    /* CLASE PARA PROTEGER EL NOMBRE DE LA TRADUCCIÓN AUTOMÁTICA */
    .notranslate {{
        translate: no !important;
    }}
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
                    badge_color = "#C65332" if porcentaje_round == 100 else ("#D9822B" if porcentaje_round >= 75 else "#F4C95D")
                    st.markdown(
                        f'<span class="badge-match" style="background-color: {badge_color};">{porcentaje_round}% Match</span>',
                        unsafe_allow_html=True
                    )

                st.subheader(receta["nombre"])
                st.caption(f"⏱️ {receta['tiempo']} min | 📊 {receta['nivel']}")

                if st.button("Ver receta", key=f"btn_{prefijo_key}_{idx}_{receta['nombre']}"):
                    st.session_state.receta_modal = receta
                    st.rerun()


def mostrar_categoria(categoria_nombre, subcategoria=None):
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
        mostrar_grilla_recetas(recetas_filtradas, f"cat_{categoria_nombre}_{subcategoria or 'gen'}", num_cols=2)
    else:
        etiqueta = f"{categoria_nombre} > {subcategoria}" if subcategoria else categoria_nombre
        st.info(f"Aún no hay recetas registradas en '{etiqueta}'. Muestrario de prueba:")
        recetas_demo = [{"receta": r} for r in recetas[:6]]
        mostrar_grilla_recetas(recetas_demo, f"demo_{categoria_nombre}_{subcategoria or 'gen'}", num_cols=2)


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

    st.subheader("👩‍‍🍳 Instrucciones de Preparación")
    for i, paso in enumerate(receta.get("instrucciones", []), start=1):
        st.write(f"**{i}.** {paso}")

    es_favorito = receta["nombre"] in st.session_state.favoritos
    if es_favorito:
        if st.button("❤️️ Quitar de Favoritos"):
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
# INTERFAZ PRINCIPAL Y DEFINICIÓN DE PESTAÑAS
# ============================================================

num_favoritos = len(st.session_state.favoritos) if isinstance(st.session_state.favoritos, list) else 0

tab_inicio, tab_menu, tab_buscador, tab_familia, tab_temporada, tab_diseno, tab_favoritos = st.tabs([
    "🏠 Inicio", 
    "📖 Menú",
    "🔍 Buscador", 
    "👨‍👩‍👧‍👦 Familia",
    "🍂 Temporada",
    "🎨 Diseño",
    f"❤️ Favoritos ({num_favoritos})"
])

# ------------------------------------------------------------
# 1. PESTAÑA DE INICIO
# ------------------------------------------------------------
with tab_inicio:
    # Búsqueda dinámica de la imagen de portada subida
    nombres_posibles = [
        "portada.jpg", "portada.JPG", "portada.jpeg", "portada.png", 
        "Portada.jpg", "PORTADA.JPG"
    ]
    
    imagen_encontrada = None
    dir_actual = os.path.dirname(__file__)

    for nombre in nombres_posibles:
        ruta = os.path.join(dir_actual, nombre)
        if os.path.exists(ruta):
            imagen_encontrada = ruta
            break

    if imagen_encontrada:
        st.image(imagen_encontrada, use_container_width=True)
    else:
        # Enlace externo directo como respaldo
        url_respaldo = "https://lh3.googleusercontent.com/d/1000065722.jpg"
        st.image(url_respaldo, use_container_width=True)

# ------------------------------------------------------------
# 2. PESTAÑA DE MENÚ
# ------------------------------------------------------------
with tab_menu:
    st.markdown('<div class="kitchen-banner notranslate" translate="no"></div>', unsafe_allow_html=True)

    tab_comida, tab_postres, tab_extras, tab_bebidas = st.tabs([
        "Comida", "Postres", "Extras", "Bebidas"
    ])

    with tab_comida:
        mostrar_categoria("Comida")

    with tab_postres:
        mostrar_categoria("Postres")

    with tab_extras:
        tab_botanas, tab_fit, tab_otros = st.tabs([
            "Botanas", "Fit", "Otros"
        ])
        with tab_botanas:
            mostrar_categoria("Extras", "Botanas")
        with tab_fit:
            mostrar_categoria("Extras", "Fit")
        with tab_otros:
            mostrar_categoria("Extras", "Otros")

    with tab_bebidas:
        mostrar_categoria("Bebidas")

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
# 4. PESTAÑA FAMILIA
# ------------------------------------------------------------
with tab_familia:
    st.markdown('<div class="kitchen-banner notranslate" translate="no"></div>', unsafe_allow_html=True)

    tab_en_familia, tab_ninos, tab_para_peques, tab_lonche = st.tabs([
        "En familia", "Niños", "Para peques", "Lonche"
    ])

    with tab_en_familia:
        mostrar_categoria("Familia", "En familia")

    with tab_ninos:
        mostrar_categoria("Familia", "Niños")

    with tab_para_peques:
        mostrar_categoria("Familia", "Para peques")

    with tab_lonche:
        mostrar_categoria("Familia", "Lonche")

# ------------------------------------------------------------
# 5. PESTAÑA TEMPORADA
# ------------------------------------------------------------
with tab_temporada:
    st.markdown('<div class="kitchen-banner notranslate" translate="no"></div>', unsafe_allow_html=True)

    tab_primavera, tab_verano, tab_otono, tab_invierno = st.tabs([
        "Primavera", "Verano", "Otoño", "Invierno"
    ])

    with tab_primavera:
        mostrar_categoria("Temporada", "Primavera")

    with tab_verano:
        mostrar_categoria("Temporada", "Verano")

    with tab_otono:
        mostrar_categoria("Temporada", "Otoño")

    with tab_invierno:
        mostrar_categoria("Temporada", "Invierno")

# ------------------------------------------------------------
# 6. PESTAÑA DISEÑO
# ------------------------------------------------------------
with tab_diseno:
    st.markdown('<div class="kitchen-banner notranslate" translate="no"></div>', unsafe_allow_html=True)

    st.info("💻 **Nota para móviles:** La personalización del cursor solo es visible al usar la app desde una computadora.")

    iconos_comida = [
        {"nombre": "Nieve", "emoji": "🍦"},
        {"nombre": "Pizza", "emoji": "🍕"},
        {"nombre": "Hamburguesa", "emoji": "🍔"},
        {"nombre": "Sándwich", "emoji": "🥪"},
        {"nombre": "Taco", "emoji": "🌮"},
        {"nombre": "Donut", "emoji": "🍩"},
        {"nombre": "Aguacate", "emoji": "🥑"},
        {"nombre": "Papas", "emoji": "🍟"},
        {"nombre": "Hot Dog", "emoji": "🌭"},
        {"nombre": "Sushi", "emoji": "🍣"},
        {"nombre": "Pastel", "emoji": "🍰"},
        {"nombre": "Chef", "emoji": "👨‍‍🍳"}
    ]

    cols_diseno = st.columns(2)

    for idx, item in enumerate(iconos_comida):
        with cols_diseno[idx % 2]:
            st.markdown(
                f"""
                <div class="icon-card">
                    {item['emoji']}
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"Seleccionar {item['nombre']}", key=f"cursor_btn_{idx}"):
                st.session_state.cursor_actual = item["emoji"]
                st.rerun()

# ------------------------------------------------------------
# 7. PESTAÑA FAVORITOS
# ------------------------------------------------------------
with tab_favoritos:
    st.subheader("❤️ Tus Recetas Guardadas")
    if st.session_state.favoritos:
        fav_recetas = [{"receta": r} for r in recetas if r["nombre"] in st.session_state.favoritos]
        mostrar_grilla_recetas(fav_recetas, "favs", num_cols=2)
    else:
        st.info("Aún no has guardado recetas favoritas.")
