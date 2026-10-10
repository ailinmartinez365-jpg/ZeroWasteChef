# ============================================================
# 1. LISTA INICIAL DE RECETAS (CREADA AL INICIO PARA EVITAR EL ERROR)
# ============================================================
recetas = [
    {
        "nombre": "Huevos con tomate",
        "imagen": "imagenes/huevos_tomate.png",
        "ingredientes": ["huevo", "tomate", "cebolla", "sal", "aceite"],
        "tiempo": 10,
        "nivel": "Principiante",
        "descripcion": "Huevos revueltos tradicionales con tomate y cebolla."
    },
    {
        "nombre": "Quesadillas de queso",
        "imagen": "imagenes/quesadillas.png",
        "ingredientes": ["tortilla", "queso"],
        "tiempo": 5,
        "nivel": "Principiante",
        "descripcion": "Quesadillas calientes de sartén."
    },
    {
        "nombre": "Pasta con tomate",
        "imagen": "imagenes/pasta_tomate.png",
        "ingredientes": ["pasta", "tomate", "ajo", "aceite de oliva", "sal"],
        "tiempo": 15,
        "nivel": "Principiante",
        "descripcion": "Pasta sencilla con salsa natural de tomate."
    },
    {
        "nombre": "Pasta cremosa",
        "imagen": "imagenes/pasta_cremosa.png",
        "ingredientes": ["pasta", "crema", "mantequilla", "queso", "pimienta"],
        "tiempo": 20,
        "nivel": "Principiante",
        "descripcion": "Pasta con salsa cremosa y queso."
    },
    {
        "nombre": "Arroz con verduras",
        "imagen": "imagenes/arroz_verduras.png",
        "ingredientes": ["arroz", "zanahoria", "chícharo", "aceite", "caldo de pollo"],
        "tiempo": 25,
        "nivel": "Explorador",
        "descripcion": "Arroz clásico acompañado de verduras."
    },
    {
        "nombre": "Puré de papa cremoso con tocino",
        "imagen": "imagenes/pure_papa.png",
        "ingredientes": ["papa", "mantequilla", "leche", "tocino", "sal", "pimienta"],
        "tiempo": 25,
        "nivel": "Principiante",
        "descripcion": "Puré de papa suave con trocitos de tocino doradito."
    }
]


# ============================================================
# CATEGORÍAS DE LAS RECETAS EXISTENTES
# ============================================================

categorias_existentes = {
    "Huevos con tomate": "Comida",
    "Quesadillas de queso": "Comida",
    "Pasta con tomate": "Comida",
    "Pasta cremosa": "Comida",
    "Arroz con verduras": "Comida",
    "Puré de papa cremoso con tocino": "Comida",

    "Tiras de sandwich dorado a la francesa": "Para botanear",
    "Bocadillos de pollo": "Para botanear",
    "Mini rollitos de pizza": "Para botanear",
    "Burritos crujientes": "Para botanear",
    "Bocaditos de papa": "Para botanear",
    "Rollitos": "Para botanear",

    "Caldo de hongos": "Comida",
    "Chayotes a la canela": "Postres",
    "Rollo de res al horno": "Comida",
    "Corona de arroz": "Comida",
    "Queso asado": "Para botanear",
    "Soufflé de queso": "Comida",
    "Crema de poblano": "Comida",
    "Verduras en salsa de pavo": "Comida",
    "Ensalada mediterránea": "Fit",
    "Frutas al Roquefort": "Extras",
    "Queso empanizado": "Para botanear",
    "Hot dog de carrito": "Para botanear",
    "Tostadas de manzana": "Postres",
    "Multigrano con tres quesos": "Fit",
    "Bocadillos integrales": "Fit",

    "Rollitos crujientes de ramen y queso": "Para botanear",
    "Spaghetti tres quesos": "Comida",
    "Bimburguesas": "Comida",
    "Canastitas de sierra ahumada": "Para botanear",
    "Chuletas al chipotle": "Comida",
    "Arroz con un poco de todo": "Comida",
    "Cuadritos de ternera": "Comida",
    "Tiritas de pescado capeadas": "Para botanear",
    "Ruedas de ternera al tinto": "Comida",
    "Balsas de pavo al yogurt": "Fit",
    "Rollo de pan con queso": "Para botanear",
    "Triángulos Bimbo": "Para botanear",
    "Salpicadas de ajonjolí": "Para botanear",
    "Timbales Bimbo": "Para botanear",
    "Pechugas al pimiento": "Comida",

    "Copas Bimbo": "Postres",
    "Mousse de Chocolate a la Francesa": "Postres",
    "Galletas a la Naranja": "Postres",
    "Panqué Nevado": "Postres",
    "Chocolatines": "Postres",
    "Pastel de Zanahoria": "Postres",
    "Copas de Durazno": "Postres",
    "Pie de Peras": "Postres",
    "Madalenas con Fresas": "Postres",
    "Hot Cake Tropical": "Postres",
    "Pan Francés": "Postres",
    "Yogurt Completo": "Fit",
    "Arroz con Leche Tradicional": "Postres",
    "Arroz con Leche Choco Cereza": "Postres",
    "Donas de Avena": "Postres",
    "Gelatina de Mazapán": "Postres",
    "Pay de Mango": "Postres",
    "Pastel Imposible de Moka": "Postres",
    "Brownie Cookies and Cream": "Postres",
    "Brownie Cheesecake con Caramelo": "Postres"
}


# ============================================================
# ASIGNAR CATEGORÍAS A LAS RECETAS EXISTENTES
# ============================================================

for receta in recetas:
    nombre_original = receta["nombre"]

    receta["categoria"] = categorias_existentes.get(
        nombre_original,
        "Comida"
    )


# ============================================================
# ELIMINAR MARCAS DE LOS NOMBRES
# ============================================================

cambios_nombres = {
    "Bimburguesas": "Hamburguesas con avena",
    "Triángulos Bimbo": "Triángulos de pan integral",
    "Timbales Bimbo": "Timbales de pan multigrano",
    "Copas Bimbo": "Copas de zarzamora"
}

for receta in recetas:
    if receta["nombre"] in cambios_nombres:
        receta["nombre"] = cambios_nombres[receta["nombre"]]

    if "ingredientes" in receta:
        receta["ingredientes"] = [
            "galletas tipo María"
            if ingrediente == "galletas Marías"
            else ingrediente
            for ingrediente in receta["ingredientes"]
        ]


# ============================================================
# NUEVAS RECETAS
# ============================================================

nuevas_recetas = [

    {
        "nombre": "Bocaditos para Niños",
        "imagen": "imagenes/bocaditos_ninos.png",
        "ingredientes": [
            "bocaditos de pan",
            "mostaza",
            "mayonesa",
            "mantequilla",
            "jamón",
            "queso manchego",
            "sal",
            "pimienta"
        ],
        "tiempo": 15,
        "nivel": "Principiante",
        "categoria": "Para botanear",
        "descripcion": "Bocaditos calientes de pan con jamón y queso.",
        "instrucciones": [
            "Corta la parte superior de los bocaditos sin romperlos.",
            "Unta mantequilla y mostaza en el interior.",
            "Agrega jamón, mayonesa, sal y pimienta.",
            "Cubre con queso manchego.",
            "Hornea unos minutos hasta que estén calientes y el queso se derrita."
        ]
    },

    {
        "nombre": "Crepas Poblanas",
        "imagen": "imagenes/crepas_poblanas.png",
        "ingredientes": [
            "crepas",
            "pollo",
            "chile poblano",
            "cebolla",
            "crema",
            "caldo de pollo",
            "leche",
            "mantequilla",
            "queso manchego",
            "sal",
            "pimienta"
        ],
        "tiempo": 35,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Crepas rellenas de pollo y poblano con una salsa cremosa.",
        "instrucciones": [
            "Sofríe la cebolla y el chile poblano.",
            "Agrega el pollo, sal y pimienta.",
            "Incorpora la crema y cocina unos minutos.",
            "Rellena las crepas con la preparación.",
            "Licúa una parte del relleno con leche.",
            "Cubre las crepas con la salsa y agrega queso.",
            "Hornea durante 10 minutos."
        ]
    },

    {
        "nombre": "Dobladas de Guajillo",
        "imagen": "imagenes/dobladas_guajillo.png",
        "ingredientes": [
            "tortilla",
            "chile guajillo",
            "tomate",
            "cebolla",
            "ajo",
            "pollo",
            "caldo de pollo",
            "queso",
            "crema",
            "aceite"
        ],
        "tiempo": 35,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Dobladas de tortilla bañadas en salsa de chile guajillo.",
        "instrucciones": [
            "Cocina los chiles guajillo con tomate, cebolla y ajo.",
            "Licúa los ingredientes con un poco de caldo.",
            "Fríe ligeramente la salsa.",
            "Pasa las tortillas por la salsa.",
            "Rellena con pollo y queso.",
            "Dobla las tortillas y sirve con crema."
        ]
    },

    {
        "nombre": "Sopa Levanta Muertos",
        "imagen": "imagenes/sopa_levanta_muertos.png",
        "ingredientes": [
            "pan blanco",
            "ajo",
            "cebolla",
            "epazote",
            "chipotle",
            "caldo de pollo",
            "huevo",
            "aceite de oliva"
        ],
        "tiempo": 35,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Sopa caliente de pan, chile y hierbas.",
        "instrucciones": [
            "Sofríe la cebolla y el ajo.",
            "Agrega el chipotle y el epazote.",
            "Incorpora el caldo de pollo.",
            "Añade el pan en trozos.",
            "Agrega huevo si deseas.",
            "Cocina hasta que todos los ingredientes estén integrados."
        ]
    },

    {
        "nombre": "Rollitos de Huevo con Tocino",
        "imagen": "imagenes/rollitos_huevo_tocino.png",
        "ingredientes": [
            "huevo",
            "tocino",
            "papa",
            "cebolla",
            "cilantro",
            "chile en vinagre",
            "caldo de pollo",
            "aceite"
        ],
        "tiempo": 35,
        "nivel": "Intermedio",
        "categoria": "Para botanear",
        "descripcion": "Rollitos de huevo rellenos de papa y tocino.",
        "instrucciones": [
            "Cocina el tocino y reserva.",
            "Prepara un puré de papa con cebolla y cilantro.",
            "Agrega el tocino picado.",
            "Prepara huevos delgados en un sartén.",
            "Rellena los huevos con la mezcla.",
            "Enrolla y cocina unos minutos más."
        ]
    },

    {
        "nombre": "Carne Morita",
        "imagen": "imagenes/carne_morita.png",
        "ingredientes": [
            "carne de res",
            "cebolla",
            "ajo",
            "chile morita",
            "tomatillo",
            "caldo de res",
            "sal",
            "pimienta",
            "aceite"
        ],
        "tiempo": 40,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Carne de res en una salsa de chile morita.",
        "instrucciones": [
            "Dora la carne con un poco de aceite.",
            "Cocina los tomatillos con chile morita, cebolla y ajo.",
            "Licúa la salsa.",
            "Agrega la salsa a la carne.",
            "Añade caldo de res.",
            "Cocina hasta que la carne esté suave."
        ]
    },

    {
        "nombre": "Bola de Queso",
        "imagen": "imagenes/bola_queso.png",
        "ingredientes": [
            "pan",
            "queso crema",
            "cebolla",
            "jugo de carne",
            "sal de ajo",
            "sal de cebolla",
            "sal",
            "pimienta",
            "nuez"
        ],
        "tiempo": 20,
        "nivel": "Principiante",
        "categoria": "Para botanear",
        "descripcion": "Botana cremosa de queso con nuez.",
        "instrucciones": [
            "Mezcla el queso crema con cebolla picada.",
            "Agrega jugo de carne, sal de ajo y sal de cebolla.",
            "Sazona con sal y pimienta.",
            "Forma una bola con la mezcla.",
            "Cubre con nuez picada.",
            "Refrigera antes de servir."
        ]
    },

    {
        "nombre": "Chalupas de Atún",
        "imagen": "imagenes/chalupas_atun.png",
        "ingredientes": [
            "pan integral",
            "atún",
            "cebolla",
            "ajo",
            "cilantro",
            "chile en vinagre",
            "caldo de pollo",
            "aceite",
            "rábano"
        ],
        "tiempo": 30,
        "nivel": "Intermedio",
        "categoria": "Para botanear",
        "descripcion": "Botana de atún preparada sobre pan integral.",
        "instrucciones": [
            "Sofríe cebolla y ajo.",
            "Agrega el atún y el chile.",
            "Sazona con caldo de pollo.",
            "Incorpora cilantro picado.",
            "Tuesta el pan integral.",
            "Coloca la preparación sobre el pan y decora con rábano."
        ]
    },

    {
        "nombre": "Budín de Atún",
        "imagen": "imagenes/budin_atun.png",
        "ingredientes": [
            "pan blanco",
            "atún",
            "cebolla",
            "crema",
            "leche",
            "cilantro",
            "caldo de pollo",
            "chile verde",
            "mantequilla",
            "queso Oaxaca",
            "pimienta"
        ],
        "tiempo": 50,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Budín salado de pan y atún con queso.",
        "instrucciones": [
            "Retira la corteza del pan.",
            "Mezcla el atún con cebolla, crema, leche y chile.",
            "Agrega cilantro y caldo de pollo.",
            "Engrasa un molde con mantequilla.",
            "Coloca capas de pan y relleno.",
            "Cubre con queso Oaxaca.",
            "Hornea hasta que el queso se derrita."
        ]
    },

    {
        "nombre": "Cappelli al Curry",
        "imagen": "imagenes/cappelli_curry.png",
        "ingredientes": [
            "cappelli",
            "cebolla",
            "curry",
            "harina",
            "crema",
            "almendra",
            "chabacano seco",
            "mantequilla",
            "caldo de pollo",
            "pimienta",
            "leche"
        ],
        "tiempo": 35,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Pasta cappelli con salsa cremosa de curry.",
        "instrucciones": [
            "Cuece la pasta.",
            "Sofríe la cebolla con mantequilla.",
            "Agrega curry y harina.",
            "Incorpora leche y crema.",
            "Añade caldo de pollo y pimienta.",
            "Agrega almendras y chabacano seco.",
            "Mezcla con la pasta y sirve."
        ]
    },

    {
        "nombre": "Cerdo al Chile Ancho",
        "imagen": "imagenes/cerdo_chile_ancho.png",
        "ingredientes": [
            "pierna de cerdo",
            "cebolla",
            "ajo",
            "caldo de pollo",
            "chile ancho",
            "zanahoria"
        ],
        "tiempo": 90,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Cerdo cocinado con chile ancho y verduras.",
        "instrucciones": [
            "Cocina la carne hasta que comience a dorarse.",
            "Hidrata los chiles ancho.",
            "Licúa los chiles con cebolla y ajo.",
            "Agrega la salsa a la carne.",
            "Incorpora caldo y zanahoria.",
            "Cocina hasta que el cerdo esté suave."
        ]
    },

    {
        "nombre": "Lasagna con Piñones",
        "imagen": "imagenes/lasagna_pinones.png",
        "ingredientes": [
            "pasta para lasagna",
            "brócoli",
            "aceite de oliva",
            "ajo",
            "cebolla",
            "anchoas",
            "tomate",
            "piñones",
            "pavo",
            "caldo de pollo",
            "pimienta",
            "queso manchego",
            "aceite"
        ],
        "tiempo": 60,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Lasagna con brócoli, pavo, piñones y queso.",
        "instrucciones": [
            "Cuece la pasta para lasagna.",
            "Sofríe ajo, cebolla y brócoli.",
            "Agrega tomate, pavo y piñones.",
            "Sazona con caldo de pollo y pimienta.",
            "Forma capas con la pasta y el relleno.",
            "Cubre con queso manchego.",
            "Hornea hasta gratinar."
        ]
    },

    {
        "nombre": "Donas Saladas de Pollo y Queso",
        "imagen": "imagenes/donas_saladas_pollo_queso.png",
        "ingredientes": [
            "pollo",
            "leche",
            "sal",
            "ajo en polvo",
            "paprika",
            "pimienta",
            "pan molido",
            "queso",
            "huevo",
            "panko",
            "aceite vegetal"
        ],
        "tiempo": 40,
        "nivel": "Intermedio",
        "categoria": "Para botanear",
        "descripcion": "Donas saladas de pollo rellenas de queso.",
        "instrucciones": [
            "Procesa el pollo con leche y condimentos.",
            "Forma pequeñas donas con la mezcla.",
            "Coloca queso en el centro.",
            "Pasa por huevo y pan molido.",
            "Cubre con panko.",
            "Cocina en aceite hasta dorar."
        ]
    },

    {
        "nombre": "Triángulos de Carne y Queso",
        "imagen": "imagenes/triangulos_carne_queso.png",
        "ingredientes": [
            "carne molida",
            "tortilla de harina",
            "queso amarillo",
            "queso para derretir",
            "huevo",
            "leche",
            "cúrcuma",
            "paprika",
            "sal",
            "pimienta"
        ],
        "tiempo": 30,
        "nivel": "Intermedio",
        "categoria": "Para botanear",
        "descripcion": "Triángulos crujientes rellenos de carne y queso.",
        "instrucciones": [
            "Cocina la carne molida con los condimentos.",
            "Coloca carne y queso sobre las tortillas.",
            "Dobla las tortillas formando triángulos.",
            "Mezcla huevo y leche.",
            "Pasa los triángulos por la mezcla.",
            "Cocina hasta que estén dorados."
        ]
    },

    {
        "nombre": "Tortitas de Avena, Papa y Atún",
        "imagen": "imagenes/tortitas_avena_papa_atun.png",
        "ingredientes": [
            "leche evaporada",
            "caldo de pollo",
            "mantequilla",
            "puré de papa instantáneo",
            "avena",
            "atún",
            "cebolla",
            "perejil",
            "huevo",
            "aceite",
            "berros",
            "tomate",
            "pepino",
            "cebolla morada",
            "limón",
            "aceite de oliva",
            "pimienta",
            "sal"
        ],
        "tiempo": 35,
        "nivel": "Intermedio",
        "categoria": "Fit",
        "descripcion": "Tortitas de avena, papa y atún acompañadas de ensalada.",
        "instrucciones": [
            "Prepara el puré de papa.",
            "Mezcla con avena, atún, cebolla y perejil.",
            "Agrega huevo y sazona.",
            "Forma las tortitas.",
            "Cocina en aceite hasta dorar.",
            "Acompaña con ensalada de verduras y limón."
        ]
    },

    {
        "nombre": "Lasaña Express en Sartén",
        "imagen": "imagenes/lasana_express_sarten.png",
        "ingredientes": [
            "carne molida",
            "zanahoria",
            "cebolla",
            "aceite",
            "sal",
            "salsa de tomate",
            "catsup",
            "pasta para lasagna",
            "crema",
            "queso para derretir"
        ],
        "tiempo": 35,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Lasaña rápida preparada directamente en sartén.",
        "instrucciones": [
            "Sofríe la carne con zanahoria y cebolla.",
            "Agrega salsa de tomate y catsup.",
            "Añade las láminas de lasagna.",
             "Cubre con crema y queso.",
            "Tapa el sartén.",
            "Cocina hasta que la pasta esté suave y el queso se derrita."
        ]
    },

    {
        "nombre": "Burritas de Frijol",
        "imagen": "imagenes/burritas_frijol.png",
        "ingredientes": [
            "tortilla de harina",
            "frijoles refritos",
            "queso",
            "cebolla",
            "ajo",
            "tomate",
            "caldo de pollo",
            "aceite"
        ],
        "tiempo": 20,
        "nivel": "Principiante",
        "categoria": "Comida",
        "descripcion": "Burritas sencillas de frijoles con queso.",
        "instrucciones": [
            "Sofríe cebolla y ajo.",
            "Agrega tomate picado.",
            "Incorpora los frijoles.",
            "Sazona con caldo de pollo.",
            "Rellena las tortillas con frijoles y queso.",
            "Enrolla y dora ligeramente."
        ]
    },

    {
        "nombre": "Cuadri-Pizza",
        "imagen": "imagenes/cuadri_pizza.png",
        "ingredientes": [
            "pan integral",
            "tomate",
            "orégano",
            "aceite de oliva",
            "salchicha",
            "jamón",
            "queso manchego",
            "sal",
            "pimienta"
        ],
        "tiempo": 20,
        "nivel": "Principiante",
        "categoria": "Para botanear",
        "descripcion": "Pequeñas pizzas hechas con pan integral.",
        "instrucciones": [
            "Corta el pan integral en cuadros.",
            "Agrega tomate y orégano.",
            "Añade salchicha o jamón.",
            "Cubre con queso manchego.",
            "Sazona con sal y pimienta.",
            "Hornea hasta que el queso se derrita."
        ]
    },

    {
        "nombre": "Caldo Tlalpeño",
        "imagen": "imagenes/caldo_tlalpeno.png",
        "ingredientes": [
            "pollo",
            "aceite",
            "cebolla",
            "ajo",
            "zanahoria",
            "papa",
            "ejote",
            "crema",
            "caldo de pollo",
            "agua",
            "sal",
            "pimienta",
            "tortilla",
            "aguacate",
            "queso fresco",
            "limón"
        ],
        "tiempo": 30,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Caldo tradicional con pollo, verduras y acompañamientos.",
        "instrucciones": [
            "Sofríe cebolla y ajo.",
            "Agrega zanahoria, papa y ejotes.",
            "Incorpora agua y caldo de pollo.",
            "Añade el pollo deshebrado.",
            "Cocina hasta que las verduras estén suaves.",
            "Sirve con crema, aguacate, queso y limón."
        ]
    },

    {
        "nombre": "Agua de Piña con Avena",
        "imagen": "imagenes/agua_pina_avena.png",
        "ingredientes": [
            "leche en polvo",
            "leche condensada",
            "avena",
            "jugo de piña",
            "agua",
            "hielo"
        ],
        "tiempo": 10,
        "nivel": "Principiante",
        "categoria": "Fit",
        "descripcion": "Bebida fría de piña y avena.",
        "instrucciones": [
            "Licúa la leche en polvo, leche condensada y avena.",
            "Agrega el jugo de piña y agua.",
            "Licúa hasta integrar.",
            "Sirve con hielo."
        ]
    },

    {
        "nombre": "Horchata con Manzana y Canela",
        "imagen": "imagenes/horchata_manzana_canela.png",
        "ingredientes": [
            "leche en polvo",
            "leche condensada",
            "arroz cocido",
            "agua",
            "canela",
            "manzana verde",
            "hielo"
        ],
        "tiempo": 15,
        "nivel": "Principiante",
        "categoria": "Extras",
        "descripcion": "Horchata cremosa con manzana y canela.",
        "instrucciones": [
            "Licúa el arroz cocido con agua.",
            "Agrega leche en polvo y leche condensada.",
            "Añade canela y manzana.",
            "Licúa hasta obtener una mezcla uniforme.",
            "Sirve fría con hielo."
        ]
    },

    {
        "nombre": "Piñada",
        "imagen": "imagenes/pinada.png",
        "ingredientes": [
            "piña congelada",
            "néctar de piña",
            "azúcar",
            "limón",
            "salsa de soya",
            "chile en polvo",
            "concentrado de jamaica",
            "piña",
            "dulce de tamarindo",
            "dulce enchilado"
        ],
        "tiempo": 10,
        "nivel": "Principiante",
        "categoria": "Extras",
        "descripcion": "Bebida fría y tropical de piña con un toque picante.",
        "instrucciones": [
            "Licúa la piña congelada con el néctar.",
            "Agrega azúcar y limón.",
            "Incorpora salsa de soya y chile en polvo.",
            "Sirve fría.",
            "Decora con piña y dulces enchilados."
        ]
    },

    {
        "nombre": "Agua de Aguacate",
        "imagen": "imagenes/agua_aguacate.png",
        "ingredientes": [
            "aguacate",
            "vainilla",
            "leche en polvo",
            "leche condensada",
            "agua",
            "hielo"
        ],
        "tiempo": 10,
        "nivel": "Principiante",
        "categoria": "Fit",
        "descripcion": "Bebida cremosa preparada con aguacate.",
        "instrucciones": [
            "Coloca el aguacate en la licuadora.",
            "Agrega vainilla, leche y agua.",
            "Añade leche condensada al gusto.",
            "Licúa hasta obtener una mezcla cremosa.",
            "Sirve con hielo."
        ]
    },

    {
        "nombre": "Crema de Queso con Espárragos",
        "imagen": "imagenes/crema_queso_esparragos.png",
        "ingredientes": [
            "leche evaporada",
            "ajo",
            "espárragos",
            "chile jalapeño",
            "queso mozzarella",
            "agua",
            "caldo de pollo",
            "crutones"
        ],
        "tiempo": 20,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Crema suave de queso y espárragos.",
        "instrucciones": [
            "Asa los espárragos.",
            "Licúa los espárragos con leche evaporada y ajo.",
            "Agrega jalapeño y queso mozzarella.",
            "Calienta la mezcla en una olla.",
            "Añade agua y caldo de pollo.",
            "Sirve con crutones."
        ]
    },

    {
        "nombre": "Palomitas de Atún",
        "imagen": "imagenes/palomitas_atun.png",
        "ingredientes": [
            "atún",
            "cebolla",
            "perejil",
            "huevo",
            "pan molido",
            "comino",
            "salsa de soya",
            "salsa inglesa",
            "harina",
            "aceite de maíz",
            "media crema",
            "queso manchego",
            "chipotle",
            "sal de cebolla",
            "tocino"
        ],
        "tiempo": 30,
        "nivel": "Intermedio",
        "categoria": "Para botanear",
        "descripcion": "Bocaditos crujientes de atún con queso.",
        "instrucciones": [
            "Mezcla el atún con cebolla, perejil y tocino.",
            "Agrega huevo, pan molido y condimentos.",
            "Forma pequeñas bolitas.",
            "Pásalas por harina.",
            "Fríe hasta que estén doradas.",
            "Sirve con media crema y queso."
        ]
    },

    {
        "nombre": "Dip de Atún con Chipotle",
        "imagen": "imagenes/dip_atun_chipotle.png",
        "ingredientes": [
            "crema",
            "salsa inglesa",
            "salsa sazonadora",
            "queso crema",
            "atún con chipotle",
            "baguette"
        ],
        "tiempo": 25,
        "nivel": "Principiante",
        "categoria": "Para botanear",
        "descripcion": "Dip cremoso de atún con chipotle.",
        "instrucciones": [
            "Mezcla el queso crema con la crema.",
            "Agrega el atún con chipotle.",
            "Incorpora las salsas.",
            "Mezcla hasta integrar.",
            "Refrigera unos minutos.",
            "Sirve con rebanadas de baguette."
        ]
    },

    {
        "nombre": "Aguachile Mixto",
        "imagen": "imagenes/aguachile_mixto.png",
        "ingredientes": [
            "camarón",
            "pescado",
            "aceite de oliva",
            "ajo",
            "cebolla morada",
            "tomate",
            "chile serrano",
            "jugo de limón",
            "salsa inglesa",
            "salsa sazonadora",
            "aguacate",
            "cilantro",
            "sal",
            "galletas saladas"
        ],
        "tiempo": 50,
        "nivel": "Intermedio",
        "categoria": "Para botanear",
        "descripcion": "Preparación fresca de camarón y pescado con limón y chile.",
        "instrucciones": [
            "Corta el pescado y los vegetales.",
            "Prepara una mezcla de limón, chile y salsas.",
            "Integra el pescado y camarón.",
            "Agrega cebolla, tomate y cilantro.",
            "Sazona al gusto.",
            "Sirve con aguacate y galletas saladas."
        ]
    },

    {
        "nombre": "Salchichas con Tocino y Piña",
        "imagen": "imagenes/salchichas_tocino_pina.png",
        "ingredientes": [
            "tocino",
            "salchicha",
            "palillos",
            "piña",
            "salsa sazonadora",
            "salsa inglesa",
            "perejil",
            "chile serrano"
        ],
        "tiempo": 30,
        "nivel": "Principiante",
        "categoria": "Para botanear",
        "descripcion": "Botana de salchicha, tocino y piña.",
        "instrucciones": [
            "Corta las salchichas y la piña.",
            "Envuelve las salchichas con tocino.",
            "Coloca los ingredientes en palillos.",
            "Cocina hasta que el tocino esté dorado.",
            "Agrega las salsas y perejil."
        ]
    },

    {
        "nombre": "Empanadas de Alcachofa",
        "imagen": "imagenes/empanadas_alcachofa.png",
        "ingredientes": [
            "pasta de hojaldre",
            "alcachofa",
            "queso Chihuahua",
            "huevo",
            "ajonjolí",
            "crema",
            "pimiento",
            "sal de cebolla"
        ],
        "tiempo": 55,
        "nivel": "Intermedio",
        "categoria": "Para botanear",
        "descripcion": "Empanadas horneadas de alcachofa y queso.",
        "instrucciones": [
            "Prepara el relleno con alcachofa, crema y pimiento.",
            "Agrega queso y sal de cebolla.",
            "Corta la pasta de hojaldre.",
            "Rellena y cierra las empanadas.",
            "Barniza con huevo.",
            "Agrega ajonjolí.",
            "Hornea hasta dorar."
        ]
    },

    {
        "nombre": "Empanaditas de Pescado",
        "imagen": "imagenes/empanaditas_pescado.png",
        "ingredientes": [
            "aceite de oliva",
            "cebolla",
            "tomate",
            "pescado blanco",
            "salsa sazonadora",
            "sal de ajo",
            "perejil",
            "tortilla de maíz",
            "palillos",
            "aceite vegetal",
            "aguacate",
            "cebolla morada",
            "cilantro",
            "limón"
        ],
        "tiempo": 34,
        "nivel": "Intermedio",
        "categoria": "Para botanear",
        "descripcion": "Pequeñas empanadas de pescado acompañadas de aguacate.",
        "instrucciones": [
            "Sofríe cebolla y tomate.",
            "Agrega el pescado deshebrado.",
            "Sazona con salsa y sal de ajo.",
            "Rellena las tortillas.",
            "Cierra con palillos.",
            "Fríe hasta dorar.",
            "Sirve con aguacate, cebolla, cilantro y limón."
        ]
    },

    {
        "nombre": "Pimientos Rellenos",
        "imagen": "imagenes/pimientos_rellenos.png",
        "ingredientes": [
            "aceite vegetal",
            "arrachera",
            "salsa sazonadora",
            "salsa inglesa",
            "pimienta",
            "ajo",
            "pimiento",
            "queso manchego"
        ],
        "tiempo": 35,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Pimientos rellenos de carne y queso.",
        "instrucciones": [
            "Corta los pimientos por la mitad.",
            "Cocina la arrachera en cubos.",
            "Agrega ajo y las salsas.",
            "Rellena los pimientos con la carne.",
            "Cubre con queso manchego.",
            "Hornea hasta que el queso se derrita."
        ]
    },

    {
        "nombre": "Finger Potatoes",
        "imagen": "imagenes/finger_potatoes.png",
        "ingredientes": [
            "papa",
            "aceite de maíz",
            "orégano",
            "pimienta",
            "cebolla",
            "carne molida",
            "sal de ajo",
            "salsa sazonadora",
            "salsa inglesa",
            "queso amarillo",
            "chile serrano",
            "chorizo"
        ],
        "tiempo": 70,
        "nivel": "Intermedio",
        "categoria": "Para botanear",
        "descripcion": "Papas preparadas con carne, queso y chile.",
        "instrucciones": [
            "Cocina las papas hasta que estén suaves.",
            "Dóralas con aceite y orégano.",
            "Cocina la carne con cebolla y condimentos.",
            "Agrega chorizo y chile serrano.",
            "Coloca la carne sobre las papas.",
            "Cubre con queso amarillo derretido."
        ]
    },

    {
        "nombre": "Elotes Asados con Chipotle y Tocino",
        "imagen": "imagenes/elotes_chipotle_tocino.png",
        "ingredientes": [
            "mayonesa",
            "salsa sazonadora",
            "chipotle",
            "palillos",
            "elote",
            "tocino"
        ],
        "tiempo": 44,
        "nivel": "Principiante",
        "categoria": "Para botanear",
        "descripcion": "Elotes asados con chipotle, mayonesa y tocino.",
        "instrucciones": [
            "Asa los elotes.",
            "Mezcla mayonesa con chipotle.",
            "Agrega salsa sazonadora.",
            "Unta la mezcla sobre los elotes.",
            "Cubre con tocino picado.",
            "Sirve calientes."
        ]
    },

    {
        "nombre": "Sopa de Coditos con Atún",
        "imagen": "imagenes/sopa_coditos_atun.png",
        "ingredientes": [
            "mayonesa",
            "atún",
            "pasta de coditos",
            "chícharos",
            "tomate",
            "crema",
            "caldo de pollo"
        ],
        "tiempo": 5,
        "nivel": "Principiante",
        "categoria": "Comida",
        "descripcion": "Ensalada fría de coditos con atún y verduras.",
        "instrucciones": [
            "Cuece y escurre la pasta.",
            "Mezcla el atún con mayonesa y crema.",
            "Agrega chícharos y tomate.",
            "Incorpora los coditos.",
            "Sazona con caldo de pollo.",
            "Refrigera antes de servir."
        ]
    },

    {
        "nombre": "Costillas a las Finas Hierbas",
        "imagen": "imagenes/costillas_finas_hierbas.png",
        "ingredientes": [
            "finas hierbas",
            "sal de ajo",
            "limón",
            "salsa inglesa",
            "salsa sazonadora",
            "costillas de cerdo"
        ],
        "tiempo": 54,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Costillas de cerdo sazonadas con hierbas y cítricos.",
        "instrucciones": [
            "Sazona las costillas con finas hierbas y sal de ajo.",
            "Agrega limón y las salsas.",
            "Deja reposar unos minutos.",
            "Cocina hasta que estén completamente hechas.",
            "Sirve calientes."
        ]
    },

    {
        "nombre": "Pizza de Pollo Hawaiano",
        "imagen": "imagenes/pizza_pollo_hawaiano.png",
        "ingredientes": [
            "harina",
            "miel",
            "aceite de oliva",
            "levadura",
            "finas hierbas",
            "agua",
            "tomate",
            "puré de tomate",
            "caldo de pollo",
            "pollo",
            "cebolla",
            "queso manchego",
            "tocino",
            "salsa BBQ",
            "salsa inglesa"
        ],
        "tiempo": 67,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Pizza casera de pollo con queso y un toque hawaiano.",
        "instrucciones": [
            "Prepara la masa con harina, levadura, agua, miel y aceite.",
            "Prepara la salsa con tomate y puré de tomate.",
            "Cocina el pollo con cebolla.",
            "Extiende la masa.",
            "Agrega salsa, pollo, queso y tocino.",
            "Añade salsa BBQ.",
            "Hornea hasta que la masa esté dorada."
        ]
    },

    {
        "nombre": "Canelones en Salsa Cremosa de Champiñones",
        "imagen": "imagenes/canelones_champinones.png",
        "ingredientes": [
            "aceite de maíz",
            "cebolla",
            "champiñones",
            "leche evaporada",
            "caldo de pollo",
            "maicena",
            "agua",
            "mantequilla",
            "pollo",
            "elote",
            "calabacita",
            "papa",
            "zanahoria",
            "sal de ajo",
            "pasta para lasagna",
            "queso manchego"
        ],
        "tiempo": 45,
        "nivel": "Intermedio",
        "categoria": "Comida",
        "descripcion": "Canelones rellenos de pollo y verduras con salsa cremosa de champiñones.",
        "instrucciones": [
            "Sofríe cebolla y champiñones.",
            "Agrega leche evaporada y caldo de pollo.",
            "Espesa con maicena.",
            "Prepara el relleno con pollo y verduras.",
            "Rellena las láminas de pasta.",
            "Coloca los canelones en un recipiente.",
            "Cubre con salsa y queso.",
            "Hornea hasta gratinar."
        ]
    }
]


# ============================================================
# AGREGAR LAS NUEVAS RECETAS A LA LISTA GENERAL
# ============================================================

recetas.extend(nuevas_recetas)


# ============================================================
# LIMPIEZA FINAL DE INGREDIENTES
# ============================================================

for receta in recetas:
    if "ingredientes" in receta:
        receta["ingredientes"] = [
            ingrediente.strip().lower()
            for ingrediente in receta["ingredientes"]
]
