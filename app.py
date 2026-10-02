import streamlit as st
import recetas as modulo_recetas
import os

# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================
st.set_page_config(
    page_title="Kitchen help",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cargar base de datos
recetas = modulo_recetas.recetas

# Inicializar estados en sesión
if "favoritos" not in st.session_state:
    st.session_state.favoritos = []

if "receta_seleccionada" not in st.session_state:
    st.session_state.receta_seleccionada = None

if "cursor_icono" not in st.session_state:
    st.session_state.cursor_icono = "https://img.icons8.com/emoji/32/pizza-emoji.png"

# ============================================================
# NORMALIZAR INGREDIENTES CON CACHÉ
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

    palabras_limpias = [
        p.strip(".,;:()") for p in palabras 
        if not p.strip(".,;:()").isdigit() and "/" not in p and p.strip(".,;:()") not in palabras_ignoradas
    ]

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
# CSS ESTILIZADO Y PROTECCIÓN CONTRA TRADUCCIÓN AUTOMÁTICA
# ============================================================
st.markdown(
    f"""
    <style>
    body {{
        cursor: url('{st.session_state.cursor_icono}'), auto !important;
    }}

    .stApp {{
        background-color: #F5F1E8;
    }}

    .block-container {{
        max-width: 1250px;
        padding-top: 35px;
        padding-bottom: 60px;
    }}

    /* MARCA PRINCIPAL - PROTEGIDA CONTRA TRADUCCIÓN */
    .marca {{
        text-align: center;
        margin-bottom: 8px;
    }}

    .marca h1 {{
        font-size: 46px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 5px;
        color: #26352B;
    }}

    .marca p {{
        font-size: 18px;
        color: #59645C;
        margin-top: 0;
    }}

    .linea {{
        height: 1px;
        background-color: #D7D0C2;
        margin: 25px 0;
    }}

    /* VISTA DE PORTADA / HERO */
    .portada {{
        text-align: center;
        padding: 50px 20px;
        background-color: #EFE9DC;
        border-radius: 20px;
        margin-bottom: 30px;
        border: 1px solid #DED8CC;
    }}

    .portada h1 {{
        font-size: 55px;
        color: #26352B;
        font-weight: 900;
        margin-bottom: 10px;
    }}

    .portada h3 {{
        font-size: 24px;
        color: #536B59;
        font-weight: 400;
        margin-bottom: 15px;
    }}

    .portada p {{
        font-size: 20px;
        color: #727D75;
        font-style: italic;
    }}

    /* ESTILOS DEL CARRUSEL Y BOTONES */
    div[data-testid="stTextInput"] input {{
        border: 1px solid #C9C2B5;
        border-radius: 12px;
        background-color: #FFFFFF;
        padding: 14px;
        font-size: 16px;
    }}

    .stButton > button {{
        border-radius: 10px;
        background-color: #536B59;
        color: white;
        font-weight: 600;
        width: 100%;
    }}

    .stButton > button:hover {{
        background-color: #3F5545;
        color: white;
    }}

    /* Clase para evitar traducción en navegadores */
    .notranslate {{
        translate: no !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# MODAL PARA DETALLES DE RECETA
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

if st.session_state.receta_seleccionada:
    mostrar_modal_receta(st.session_state.receta_seleccionada)
    st.session_state.receta_seleccionada = None


# ============================================================
# ENCABEZADO CON MARCA
# ============================================================
st.markdown(
    """
    <div class="marca notranslate" translate="no">
        <h1>Kitchen help</h1>
        <p>No solo cocines. Aprovecha, descubre y comparte.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="linea"></div>', unsafe_allow_html=True)

# PESTAÑAS PRINCIPALES DE LA APLICACIÓN
tab_inicio, tab_menu, tab_buscador, tab_favoritos, tab_diseno = st.tabs([
    "🏠 Inicio", 
    "📖 Menú", 
    "🔍 Buscador Inteligente", 
    f"❤️ Favoritos ({len(st.session_state.favoritos)})",
    "🎨 Diseño / Cursores"
])

# ============================================================
# PESTAÑA 1: INICIO
# ============================================================
with tab_inicio:
    st.markdown(
        """
        <div class="portada">
            <h1 class="notranslate" translate="no">KITCHEN HELP</h1>
            <h3>No solo cocines.</h3>
            <p>Aprovecha, descubre y comparte.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🥦 **Cero Desperdicio**\nUtiliza los ingredientes que ya tienes en casa antes de que se echen a perder.")
    with col2:
        st.success("⚡ **Ahorra Tiempo**\nFiltra recetas rápidas según el tiempo disponible que tengas para cocinar.")
    with col3:
        st.warning("🍳 **Recetas por Nivel**\nDesde opciones sencillas para principiantes hasta platillos para expertos.")


# ============================================================
# PESTAÑA 2: MENÚ (COMIDA, POSTRES, EXTRAS, BEBIDAS)
# ============================================================
with tab_menu:
    st.subheader("📖 Menú de Recetas")
    subtab_comida, subtab_postres, subtab_extras, subtab_bebidas = st.tabs([
        "🍲 Comida", "🍰 Postres", "🍟 Extras", "🥤 Bebidas"
    ])

    def desplegar_grid_categoria(cat_nombre):
        # Filtrar o mostrar recetas pertenecientes a la categoría
        recetas_cat = [r for r in recetas if r.get("categoria", "Comida") == cat_nombre]
        if not recetas_cat:
            recetas_cat = recetas[:6] # Muestra las primeras como ejemplo si aún no tienen categoría asignada
            
        cols = st.columns(2)
        for idx, rec in enumerate(recetas_cat):
            with cols[idx % 2]:
                with st.container(border=True):
                    ruta_img = os.path.join(os.path.dirname(__file__), rec.get("imagen", ""))
                    if os.path.exists(ruta_img):
                        st.image(ruta_img, use_container_width=True)
                    st.subheader(rec["nombre"])
                    st.caption(f"⏱️ {rec['tiempo']} min | 📈 Nivel: {rec['nivel']}")
                    if st.button("Ver receta", key=f"btn_menu_{cat_nombre}_{idx}_{rec['nombre']}"):
                        st.session_state.receta_seleccionada = rec
                        st.rerun()

    with subtab_comida:
        desplegar_grid_categoria("Comida")
    with subtab_postres:
        desplegar_grid_categoria("Postres")
    with subtab_extras:
        desplegar_grid_categoria("Extras")
    with subtab_bebidas:
        desplegar_grid_categoria("Bebidas")


# ============================================================
# PESTAÑA 3: BUSCADOR INTELIGENTE CON CARRUSELES POR NIVEL
# ============================================================
with tab_buscador:
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 25px;">
            <h2>Busca tu receta ideal</h2>
            <p>Ingresa tus ingredientes disponibles y filtra por tus preferencias.</p>
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
        filtro_tiempo = st.selectbox("Tiempo disponible", ["Todos", "10 minutos", "20 minutos", "30+ minutos"])
    with columna_nivel:
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

            resultados.append({
                "receta": receta,
                "porcentaje": porcentaje,
                "faltantes": faltantes,
                "coincidencias": coincidencias
            })

        resultados.sort(key=lambda r: (r["porcentaje"], r["coincidencias"]), reverse=True)

        st.markdown('<div class="linea"></div>', unsafe_allow_html=True)
        st.markdown(f"### 🍽️ Recetas encontradas ({len(resultados)})")

        if resultados:
            niveles = ["Principiante", "Intermedio", "Explorador", "Experto"]
            for nivel in niveles:
                recetas_nivel = [res for res in resultados if res["receta"]["nivel"] == nivel]

                if recetas_nivel:
                    st.subheader(f"📌 Nivel: {nivel}")
                    
                    # CARRUSEL HORIZONTAL DIVIDIDO EN SECCIONES POR NIVEL
                    cols = st.columns(len(recetas_nivel))
                    for idx, res in enumerate(recetas_nivel):
                        receta = res["receta"]
                        porcentaje = res["porcentaje"]
                        faltantes = res["faltantes"]

                        with cols[idx]:
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

                                st.caption(f"⏱ {receta['tiempo']} min")

                                if faltantes:
                                    st.caption(f"**Te falta:** {', '.join(faltantes)}")
                                else:
                                    st.caption("✨ **¡Tienes todo!**")

                                if st.button("Ver receta", key=f"btn_carrusel_{nivel}_{receta['nombre']}"):
                                    st.session_state.receta_seleccionada = receta
                                    st.rerun()

                    st.markdown('<div class="linea"></div>', unsafe_allow_html=True)
        else:
            st.info("No se encontraron recetas con esos ingredientes y filtros.")


# ============================================================
# PESTAÑA 4: FAVORITOS
# ============================================================
with tab_favoritos:
    st.subheader("❤️ Tus Recetas Guardadas")
    if st.session_state.favoritos:
        fav_recetas = [r for r in recetas if r["nombre"] in st.session_state.favoritos]
        cols_fav = st.columns(min(len(fav_recetas), 3))
        for idx, receta in enumerate(fav_recetas):
            with cols_fav[idx % len(cols_fav)]:
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
        st.info("Aún no has guardado recetas favoritas. Haz clic en el botón de corazón dentro de cualquier receta para guardarla aquí.")


# ============================================================
# PESTAÑA 5: PERSONALIZACIÓN DE CURSORES
# ============================================================
with tab_diseno:
    st.subheader("🎨 Personaliza el Cursor de la App")
    st.write("Selecciona tu icono de comida favorito para cambiar el puntero del ratón:")

    iconos = [
        {"nombre": "Pizza", "url": "https://img.icons8.com/emoji/32/pizza-emoji.png", "emoji": "🍕"},
        {"nombre": "Hamburguesa", "url": "https://img.icons8.com/emoji/32/hamburger-emoji.png", "emoji": "🍔"},
        {"nombre": "Taco", "url": "https://img.icons8.com/emoji/32/taco-emoji.png", "emoji": "🌮"},
        {"nombre": "Aguacate", "url": "https://img.icons8.com/emoji/32/avocado-emoji.png", "emoji": "🥑"},
        {"nombre": "Donut", "url": "https://img.icons8.com/emoji/32/doughnut-emoji.png", "emoji": "🍩"},
        {"nombre": "Chef", "url": "https://img.icons8.com/emoji/32/cook-emoji.png", "emoji": "👨‍🍳"}
    ]

    cols_iconos = st.columns(3)
    for idx, item in enumerate(iconos):
        with cols_iconos[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {item['emoji']} {item['nombre']}")
                if st.button(f"Usar cursor {item['nombre']}", key=f"cursor_{item['nombre']}"):
                    st.session_state.cursor_icono = item["url"]
                    st.rerun()
    
