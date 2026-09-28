import streamlit as st
import streamlit.components.v1 as components
import recetas as modulo_recetas
import os
import base64
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

if "favoritos" not in st.session_state:
    st.session_state.favoritos = []

if "receta_modal" not in st.session_state:
    st.session_state.receta_modal = None


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def obtener_base64_imagen(ruta_relativa):
    if not ruta_relativa:
        return ""
    ruta_abs = os.path.join(os.path.dirname(__file__), ruta_relativa)
    if os.path.exists(ruta_abs):
        try:
            with open(ruta_abs, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
                ext = ruta_relativa.split(".")[-1].lower()
                mime = "jpeg" if ext in ["jpg", "jpeg"] else ext
                return f"data:image/{mime};base64,{encoded}"
        except Exception:
            return ""
    return ""

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
# ESTILOS GENERALES
# ============================================================

st.markdown(
    """
    <style>
    .stApp { background-color: #F5F1E8; }
    .block-container { max-width: 1250px; padding-top: 35px; padding-bottom: 60px; }
    .marca { text-align: center; margin-bottom: 8px; }
    .marca h1 { font-size: 46px; font-weight: 800; letter-spacing: 2px; margin-bottom: 5px; color: #26352B; }
    .marca p { font-size: 18px; color: #59645C; margin-top: 0; }
    .linea { height: 1px; background-color: #D7D0C2; margin: 25px 0; }
    .seccion-busqueda { text-align: center; margin-bottom: 25px; }
    div[data-testid="stTextInput"] input { border: 1px solid #C9C2B5; border-radius: 12px; background-color: #FFFFFF; padding: 14px; font-size: 16px; }
    .stButton > button { border-radius: 10px; background-color: #536B59; color: white; font-weight: 600; width: 100%; }
    .stButton > button:hover { background-color: #3F5545; color: white; }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# RENDERIZADOR DE CARRUSEL HORIZONTAL HTML REAL
# ============================================================

def renderizar_carrusel_real(lista_items, prefijo_key):
    cards_html = ""
    for idx, item in enumerate(lista_items):
        receta = item["receta"]
        porcentaje = round(item["porcentaje"])
        badge_color = "#28a745" if porcentaje == 100 else ("#17a2b8" if porcentaje >= 75 else "#ffc107")
        img_src = obtener_base64_imagen(receta.get("imagen", ""))
        
        img_tag = f'<img src="{img_src}" class="card-img"/>' if img_src else '<div class="card-img-placeholder">🍳</div>'
        
        # Guardamos el nombre escapado para JS
        nombre_safe = receta["nombre"].replace("'", "\\'")

        cards_html += f"""
        <div class="card">
            <div class="img-box">
                {img_tag}
                <span class="badge" style="background-color: {badge_color};">{porcentaje}% Match</span>
            </div>
            <div class="card-content">
                <div class="title">{receta['nombre']}</div>
                <div class="meta">⏱️ {receta['tiempo']} min | 📊 {receta['nivel']}</div>
                <button class="btn-receta" onclick="abrirReceta('{nombre_safe}')">Ver receta</button>
            </div>
        </div>
        """

    html_componente = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }}
        body {{ background: transparent; overflow: hidden; }}
        
        .carousel-wrapper {{
            position: relative;
            width: 100%;
            display: flex;
            align-items: center;
        }}
        
        .carousel-track {{
            display: flex;
            flex-direction: row;
            gap: 16px;
            overflow-x: auto;
            scroll-behavior: smooth;
            padding: 10px 5px 15px 5px;
            width: 100%;
        }}
        
        .carousel-track::-webkit-scrollbar {{
            height: 6px;
        }}
        .carousel-track::-webkit-scrollbar-thumb {{
            background: #C9C2B5;
            border-radius: 10px;
        }}
        
        .card {{
            flex: 0 0 210px;
            width: 210px;
            height: 275px;
            background: #FFFFFF;
            border: 1px solid #DED8CC;
            border-radius: 12px;
            box-shadow: 0 3px 8px rgba(0,0,0,0.06);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
        }}
        
        .img-box {{
            width: 100%;
            height: 120px;
            position: relative;
            background: #EFECE6;
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
        }}
        
        .badge {{
            position: absolute;
            top: 6px;
            right: 6px;
            padding: 2px 7px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: bold;
            color: white;
        }}
        
        .card-content {{
            padding: 10px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            flex-grow: 1;
        }}
        
        .title {{
            font-size: 14px;
            font-weight: 700;
            color: #26352B;
            line-height: 1.2;
            height: 34px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }}
        
        .meta {{
            font-size: 12px;
            color: #666;
            margin: 4px 0 8px 0;
            font-weight: 600;
        }}
        
        .btn-receta {{
            width: 100%;
            background-color: #536B59;
            color: white;
            border: none;
            padding: 8px 0;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }}
        
        .btn-receta:hover {{
            background-color: #3F5545;
        }}
        
        .nav-btn {{
            position: absolute;
            top: 40%;
            transform: translateY(-50%);
            width: 32px;
            height: 32px;
            background: rgba(83, 107, 89, 0.9);
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            z-index: 10;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }}
        .nav-left {{ left: -5px; }}
        .nav-right {{ right: -5px; }}
    </style>
    </head>
    <body>
        <div class="carousel-wrapper">
            <button class="nav-btn nav-left" onclick="scrollCarrusel(-300)">❮</button>
            <div class="carousel-track" id="track_{prefijo_key}">
                {cards_html}
            </div>
            <button class="nav-btn nav-right" onclick="scrollCarrusel(300)">❯</button>
        </div>

        <script>
            function scrollCarrusel(val) {{
                document.getElementById('track_{prefijo_key}').scrollBy({{ left: val, behavior: 'smooth' }});
            }}

            function abrirReceta(nombre) {{
                // Dispara el evento sin recargar la página ni romper Streamlit
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: nombre
                }}, '*');
            }}
        </script>
    </body>
    </html>
    """

    # Retorna el valor seleccionado de la receta directamente al hacer clic
    return components.html(html_componente, height=300)


# ============================================================
# MODAL / POPUP DE LA RECETA
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


# Abrir modal si hay receta activa
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

        resultados.sort(key=lambda r: (r["puntuacion"], r["porcentaje"], r["coincidencias"], -r["receta"]["tiempo"]), reverse=True)

        st.markdown('<div class="linea"></div>', unsafe_allow_html=True)
        st.markdown(f"### 🍽️ Resultados ({len(resultados)})")

        if resultados:
            niveles = ["Principiante", "Intermedio", "Explorador", "Experto"]

            for i, nivel in enumerate(niveles):
                recetas_nivel = [res for res in resultados if res["receta"]["nivel"] == nivel]

                if recetas_nivel:
                    st.subheader(f"📌 {nivel}")
                    # Renderizamos carrusel HTML estilizado e independiente
                    seleccion = renderizar_carrusel_real(recetas_nivel, f"car_{i}")
                    
                    # Si el usuario hace clic en "Ver receta", capturamos el evento
                    if seleccion:
                        for r in recetas:
                            if r["nombre"] == seleccion:
                                st.session_state.receta_modal = r
                                st.rerun()
        else:
            st.info("No se encontraron recetas con esos ingredientes y filtros.")


# ============================================================
# TAB FAVORITOS
# ============================================================

with tab_favoritos:
    st.subheader("❤️ Tus Recetas Guardadas")
    if st.session_state.favoritos:
        fav_recetas = [r for r in recetas if r["nombre"] in st.session_state.favoritos]
        cols_fav = st.columns(3)
        for idx, receta in enumerate(fav_recetas):
            with cols_fav[idx % 3]:
                with st.container(border=True):
                    ruta_imagen = os.path.join(os.path.dirname(__file__), receta.get("imagen", ""))
                    if os.path.exists(ruta_imagen):
                        st.image(ruta_imagen, use_container_width=True)
                    st.subheader(receta["nombre"])
                    st.caption(f"⏱️ {receta['tiempo']} min | 📈 {receta['nivel']}")
                    if st.button("Ver receta", key=f"fav_btn_{receta['nombre']}"):
                        st.session_state.receta_modal = receta
                        st.rerun()
    else:
        st.info("Aún no has guardado recetas favoritas.")
    
