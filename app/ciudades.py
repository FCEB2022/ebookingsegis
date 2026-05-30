# Ciudades de Guinea Ecuatorial por región

# Lista completa de ciudades principales de Guinea Ecuatorial
CIUDADES_GUINEA_ECUATORIAL = [
    # Región Insular
    ('Malabo', 'Malabo (Capital)'),
    ('Luba', 'Luba'),
    ('Riaba', 'Riaba'),
    ('Baney', 'Baney'),
    ('Rebola', 'Rebola'),
    ('Santiago de Baney', 'Santiago de Baney'),
    ('San Antonio de Palé', 'San Antonio de Palé (Annobón)'),
    
    # Región Continental - Litoral
    ('Bata', 'Bata'),
    ('Mbini', 'Mbini'),
    ('Cogo', 'Cogo'),
    ('Río Campo', 'Río Campo'),
    
    # Centro Sur
    ('Evinayong', 'Evinayong'),
    ('Aconibe', 'Aconibe'),
    ('Añisoc', 'Añisoc'),
    ('Niefang', 'Niefang'),
    
    # Kié-Ntem
    ('Ebebiyín', 'Ebebiyín'),
    ('Micomeseng', 'Micomeseng'),
    ('Nsok-Nsomo', 'Nsok-Nsomo'),
    ('Ncue', 'Ncue'),
    
    # Wele-Nzas
    ('Mongomo', 'Mongomo'),
    ('Aconibe', 'Aconibe'),
    ('Añisoc', 'Añisoc'),
    ('Nsork', 'Nsork'),
    
    # Djibloho
    ('Oyala', 'Oyala (Ciudad de la Paz)'),
]

# Diccionario organizado por provincias
CIUDADES_POR_PROVINCIA = {
    'Bioko Norte': ['Malabo', 'Baney', 'Rebola', 'Santiago de Baney'],
    'Bioko Sur': ['Luba', 'Riaba'],
    'Annobón': ['San Antonio de Palé'],
    'Litoral': ['Bata', 'Mbini', 'Cogo', 'Río Campo'],
    'Centro Sur': ['Evinayong', 'Niefang', 'Aconibe', 'Añisoc'],
    'Kié-Ntem': ['Ebebiyín', 'Micomeseng', 'Nsok-Nsomo', 'Ncue'],
    'Wele-Nzas': ['Mongomo', 'Aconibe', 'Añisoc', 'Nsork'],
    'Djibloho': ['Oyala'],
}

# Función helper para obtener la lista de ciudades
def get_ciudades_choices():
    """Retorna lista de tuplas para WTForms SelectField"""
    return [('', 'Seleccionar ciudad...')] + CIUDADES_GUINEA_ECUATORIAL

# Función para formatear precios en XAF  
def format_currency_xaf(amount):
    """Formatea cantidad en Francos CFA (XAF)"""
    return f"{amount:,.0f} FCFA".replace(',', '.')

# Tasa de conversión aproximada (1 EUR ≈ 656 XAF)
CONVERSION_EUR_TO_XAF = 656

# ===========================
# CONSTANTES PARA FILTROS
# ===========================

# Tipos de propiedad principales
TIPOS_PROPIEDAD = [
    ('', 'Indiferente'),
    ('vivienda', 'Vivienda'),
    ('locales_naves', 'Locales y Naves'),
    ('oficinas', 'Oficinas'),
    ('terrenos', 'Solares Urbanos/Terrenos'),
]

# Subtipos de vivienda
SUBTIPOS_VIVIENDA = [
    ('', 'Indiferente'),
    ('chalet', 'Chalet'),
    ('apartamento', 'Apartamento'),
    ('piso', 'Piso'),
    ('estudio', 'Estudio'),
    ('duplex', 'Dúplex'),
    ('atico', 'Ático'),
]

# Tipologías de locales y naves
TIPOLOGIAS_LOCAL = [
    ('', 'Indiferente'),
    ('comercial', 'Comercial'),
    ('ocio', 'Ocio'),
    ('eventos', 'Eventos'),
    ('industrial', 'Industrial'),
    ('almacenamiento', 'Almacenamiento/Trasteros'),
]

# Tipologías de oficinas
TIPOLOGIAS_OFICINA = [
    ('', 'Indiferente'),
    ('cerradas', 'Oficinas Cerradas'),
    ('abiertas', 'Oficinas Abiertas (Open plan)'),
    ('mixtas', 'Oficinas Mixtas (Flexibles)'),
    ('coworking', 'Coworking'),
]

# Tipos de alquiler
TIPOS_ALQUILER = [
    ('', 'Indiferente'),
    ('larga_duracion', 'Larga duración'),
    ('temporada', 'De temporada'),
]

# Estados de propiedad
ESTADOS_PROPIEDAD = [
    ('', 'Indiferente'),
    ('bien', 'Bien'),
    ('muy_bien', 'Muy bien'),
    ('obra_nueva', 'Obra nueva'),
    ('a_reformar', 'A reformar'),
]

# Opciones de habitaciones y baños
OPCIONES_HABITACIONES_BANOS = [
    ('', 'Indiferente'),
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4+', '+4'),
]

# Características de vivienda
CARACTERISTICAS_VIVIENDA = [
    ('amueblado', 'Amueblado'),
    ('sin_amueblar', 'Sin amueblar'),
    ('con_electrodomesticos', 'Con electrodomésticos'),
    ('sin_electrodomesticos', 'Sin electrodomésticos'),
    ('accesibilidad', 'Buena accesibilidad'),
    ('ascensor', 'Ascensor'),
    ('internet', 'Internet'),
    ('aire_acondicionado', 'Aire acondicionado'),
    ('jardin', 'Jardín o patio'),
    ('parking', 'Garaje/Parking'),
    ('terraza', 'Terraza/Balcón'),
    ('piscina', 'Piscina'),
]

# Características de locales (para comercial, ocio, eventos)
CARACTERISTICAS_LOCAL = [
    ('accesibilidad', 'Buena accesibilidad'),
    ('amueblado', 'Amueblado'),
    ('sin_amueblar', 'Sin amueblar'),
    ('parking', 'Garaje/Parking'),
    ('terraza', 'Terraza/Balcón'),
    ('piscina', 'Piscina'),
]

# Características de oficinas
CARACTERISTICAS_OFICINA = [
    ('amueblado', 'Amueblado'),
    ('sin_amueblar', 'Sin amueblar'),
    ('accesibilidad', 'Buena accesibilidad'),
    ('ascensor', 'Ascensor'),
    ('internet', 'Internet'),
    ('aire_acondicionado', 'Aire acondicionado'),
    ('jardin', 'Jardín o patio'),
    ('parking', 'Garaje/Parking'),
]

# Características de terrenos
CARACTERISTICAS_TERRENO = [
    ('acceso_rodado', 'Con acceso rodado'),
    ('sin_acceso_rodado', 'Sin acceso rodado'),
    ('terreno_llano', 'Terreno llano'),
    ('terreno_montanoso', 'Terreno montañoso'),
    ('terreno_pantanoso', 'Terreno Pantanoso'),
    ('suministro_electrico', 'Con suministro eléctrico cercano'),
    ('cerca_centro', 'Cerca del centro urbano'),
]

# Barrios por ciudad (principales ciudades)
BARRIOS_POR_CIUDAD = {
    'Malabo': ['Centro', 'Ela Nguema', 'Magno', 'Semu', 'Baney', 'Rebola', 'Sampaka'],
    'Bata': ['Centro', 'Ukomba', 'Nkubilhon', 'Mbini', 'Litoral Norte', 'Litoral Sur'],
    'Oyala': ['Centro Administrativo', 'Zona Residencial', 'Zona Universitaria'],
    'Ebebiyín': ['Centro', 'Norte', 'Sur'],
    'Mongomo': ['Centro', 'Este', 'Oeste'],
}

def get_barrios_choices(ciudad=None):
    """Retorna lista de barrios para una ciudad específica"""
    if ciudad and ciudad in BARRIOS_POR_CIUDAD:
        return [('', 'Seleccionar barrio...')] + [(b, b) for b in BARRIOS_POR_CIUDAD[ciudad]]
    return [('', 'Escribir barrio...')]
