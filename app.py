import streamlit as st
import streamlit.components.v1 as components
import recetas as modulo_recetas
import os
import urllib.parse

# Configuración de página
st.set_page_config(
    page_title="Chef Cero Residuos",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cargar base de datos
recetas = modulo_recetas.recetas

# Inicializar estado para Favoritos
if "favoritos" not in st.session_state:
    st.session_state.favoritos = []

# Detectar clic desde el carrusel HTML a través de parámetros de URL
query_params = st.query_params
if "receta_clic" in query_params:
    nombre_receta = query_params["receta_clic"]
    st.query_params.clear()
    for r in recetas:
        if r["nombre"] == nombre_receta:
            st.session_state.receta_seleccionada = r
            break

# ============================================================
# NORMALIZAR INGREDIENTES
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
# ESTILOS GENERALES
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
        max-width: 1250px;
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
# CARRUSEL HORIZONTAL CON FLECHAS Y REDIRECCIÓN FUNCIONAL
# ============================================================

def renderizar_carrusel_netflix(lista_items, id_carrusel):
    tarjetas_html = ""
    for item in lista_items:
        receta = item["receta"]
        porcentaje = round(item["porcentaje"])

        badge_color = "#28a745" if porcentaje == 100 else ("#17a2b8" if porcentaje >= 75 else "#ffc107")
        badge_texto = f"{porcentaje}% Match"

        # Manejo de imagen
        ruta_img = receta.get("imagen", "")
        if os.path.exists(os.path.join(os.path.dirname(__file__), ruta_img)):
            img_html = f'<img src="{ruta_img}" class="card-img" alt="{receta["nombre"]}"/>'
        else:
            img_html = '<div class="card-img-placeholder">🍳</div>'

        # Nombre codificado para pasar de manera segura en la URL
        nombre_escapado = urllib.parse.quote(receta['nombre'])

        tarjetas_html += f"""
        <div class="card-netflix" onclick="seleccionarReceta('{nombre_escapado}')">
            <div class="img-container">
                {img_html}
                <div class="badge" style="background-color: {badge_color};">{badge_texto}</div>
            </div>
            <div class="card-body">
                <h4>{receta['nombre']}</h4>
                <p class="info">⏱️ {receta['tiempo']} min</p>
            </div>
        </div>
        """

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: transparent;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        .carrusel-wrapper {{
            position: relative;
            display: flex;
            align-items: center;
            width: 100%;
        }}
        .carrusel-container {{
            display: flex;
            overflow-x: auto;
            gap: 16px;
            padding: 10px 40px 20px 40px;
            scroll-behavior: smooth;
            -webkit-overflow-scrolling: touch;
            width: 100%;
        }}
        .carrusel-container::-webkit-scrollbar {{
            height: 6px;
        }}
        .carrusel-container::-webkit-scrollbar-thumb {{
            background-color: #C9C2B5;
            border-radius: 10px;
        }}

        /* BOTONES DE FLECHA NAV */
        .btn-nav {{
            position: absolute;
            top: 42%;
            transform: translateY(-50%);
            width: 36px;
            height: 36px;
            background-color: rgba(83, 107, 89, 0.85);
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            z-index: 10;
            font-size: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: background-color 0.2s ease, transform 0.2s ease;
        }}
        .btn-nav:hover {{
            background-color: rgba(63, 85, 69, 1);
            transform: translateY(-50%) scale(1.1);
        }}
        .btn-left {{
            left: 2px;
        }}
        .btn-right {{
            right: 2px;
        }}

        /* TARJETAS DE TAMAÑO EXACTO Y UNIFORME */
        .card-netflix {{
            flex: 0 0 200px;
            width: 200px;
            height: 240px;
            background-color: #FFFFFF;
            border: 1px solid #DED8CC;
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            display: flex;
            flex-direction: column;
            user-select: none;
            box-sizing: border-box;
        }}
        .card-netflix:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.12);
            border-color: #536B59;
        }}

        /* CONTENEDOR DE IMAGEN */
        .img-container {{
            width: 100%;
            height: 130px;
            position: relative;
            background-color: #EFECE6;
        }}
        .card-img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .card-img-placeholder {{
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
            background-color: #E4DFC3;
        }}

        /* BADGE */
        .badge {{
            position: absolute;
            top: 8px;
            right: 8px;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: bold;
            color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}

        /* CUERPO DE LA TARJETA */
        .card-body {{
            padding: 10px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            flex-grow: 1;
        }}
        .card-body h4 {{
            margin: 0;
            font-size: 15px;
            color: #26352B;
            line-height: 1.25;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .info {{
            margin: 6px 0 0 0;
            font-size: 12px;
            color: #666;
            font-weight: 600;
        }}
    </style>
    </head>
    <body>
        <div class="carrusel-wrapper">
            <button class="btn-nav btn-left" onclick="moverCarrusel(-300)">❮</button>
            <div class="carrusel-container" id="{id_carrusel}">
                {tarjetas_html}
            </div>
            <button class="btn-nav btn-right" onclick="moverCarrusel(300)">❯</button>
        </div>

        <script>
        function moverCarrusel(distancia) {{
            const carrusel = document.getElementById('{id_carrusel}');
            carrusel.scrollBy({{ left: distancia, behavior: 'smooth' }});
        }}

        function seleccionarReceta(nombreCodificado) {{
            // Redirección directa y segura en la ventana principal de Streamlit
            window.top.location.href = '?receta_clic=' + nombreCodificado;
        }}
        </script>
    </body>
    </html>
    """

    components.html(html_code, height=270)


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


# Abrir modal si hay una receta seleccionada
if "receta_seleccionada" in st.session_state and st.session_state.receta_seleccionada:
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
        st.markdown(f"### 🍽️ Resultados ({len(resultados)})")

        if resultados:
            niveles = ["Principiante", "Intermedio", "Explorador", "Experto"]

            for i, nivel in enumerate(niveles):
                recetas_nivel = [res for res in resultados if res["receta"]["nivel"] == nivel]

                if recetas_nivel:
                    st.subheader(f"📌 {nivel}")
                    renderizar_carrusel_netflix(recetas_nivel, f"carrusel_{i}")
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
        st.info("Aún no has guardado recetas favoritas.")
    
