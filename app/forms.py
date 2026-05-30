from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, FloatField, FileField, MultipleFileField, DateField, HiddenField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput
from flask_wtf.file import FileAllowed
from flask_babel import lazy_gettext as _l
from app.models import Usuario
from app.ciudades import (
    get_ciudades_choices, get_barrios_choices, 
    TIPOS_PROPIEDAD, SUBTIPOS_VIVIENDA, TIPOLOGIAS_LOCAL, TIPOLOGIAS_OFICINA,
    TIPOS_ALQUILER, ESTADOS_PROPIEDAD, OPCIONES_HABITACIONES_BANOS,
    CARACTERISTICAS_VIVIENDA, CARACTERISTICAS_LOCAL, CARACTERISTICAS_OFICINA,
    CARACTERISTICAS_TERRENO
)


class LoginForm(FlaskForm):
    """User login form"""
    username = StringField(_l('Nombre de usuario'), validators=[
        DataRequired(message=_l('El nombre de usuario es requerido')),
        Length(min=3, max=64, message=_l('El nombre de usuario debe tener entre 3 y 64 caracteres'))
    ])
    password = PasswordField(_l('Contraseña'), validators=[
        DataRequired(message=_l('La contraseña es requerida'))
    ])
    remember_me = BooleanField(_l('Recordarme'))


class RegistrationForm(FlaskForm):
    """User registration form"""
    nombre = StringField(_l('Nombre completo'), validators=[
        DataRequired(message=_l('El nombre es requerido')),
        Length(min=3, max=100, message=_l('El nombre debe tener entre 3 y 100 caracteres'))
    ])
    username = StringField(_l('Nombre de usuario'), validators=[
        DataRequired(message=_l('El nombre de usuario es requerido')),
        Length(min=3, max=64, message=_l('El nombre de usuario debe tener entre 3 y 64 caracteres'))
    ])
    email = StringField(_l('Email'), validators=[
        DataRequired(message=_l('El email es requerido')),
        Email(message=_l('Email inválido'))
    ])
    telefono = StringField(_l('Teléfono'), validators=[
        DataRequired(message=_l('El teléfono es requerido')),
        Length(min=9, max=20, message=_l('Teléfono inválido'))
    ])
    password = PasswordField(_l('Contraseña'), validators=[
        DataRequired(message=_l('La contraseña es requerida')),
        Length(min=6, message=_l('La contraseña debe tener al menos 6 caracteres'))
    ])
    password2 = PasswordField(_l('Confirmar contraseña'), validators=[
        DataRequired(message=_l('Confirme la contraseña')),
        EqualTo('password', message=_l('Las contraseñas deben coincidir'))
    ])
    
    def validate_username(self, username):
        """Check if username already exists"""
        user = Usuario.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(_l('Este nombre de usuario ya está en uso. Por favor elige otro.'))
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = Usuario.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(_l('Este email ya está registrado. Por favor usa otro.'))


class OfertaForm(FlaskForm):
    """Property listing form"""
    titulo = StringField(_l('Título'), validators=[
        DataRequired(message=_l('El título es requerido')),
        Length(max=200)
    ])
    descripcion = TextAreaField(_l('Descripción'), validators=[
        DataRequired(message=_l('La descripción es requerida'))
    ])
    precio = FloatField(_l('Precio (FCFA)'), validators=[
        DataRequired(message=_l('El precio es requerido')),
        NumberRange(min=0, message=_l('El precio debe ser mayor a 0'))
    ])
    ubicacion = SelectField(_l('Ciudad'), choices=get_ciudades_choices(), validators=[
        DataRequired(message=_l('La ciudad es requerida'))
    ])
    barrio = StringField(_l('Barrio / Zona'), validators=[Optional()])
    latitud = FloatField(_l('Latitud'), validators=[Optional()])
    longitud = FloatField(_l('Longitud'), validators=[Optional()])
    
    tipo_propiedad = SelectField(_l('Tipo de propiedad'), choices=TIPOS_PROPIEDAD, validators=[DataRequired(message=_l('Selecciona el tipo de propiedad'))])
    
    subtipo_propiedad = SelectField(_l('Subtipo de propiedad'), 
                                    choices=[('', _l('Indiferente'))] + SUBTIPOS_VIVIENDA[1:] + TIPOLOGIAS_LOCAL[1:] + TIPOLOGIAS_OFICINA[1:],
                                    validators=[Optional()])
    
    tipo_operacion = SelectField(_l('Tipo de transacción'), choices=[
        ('', _l('Seleccionar...')),
        ('venta', _l('Comprar')),
        ('alquiler', _l('Alquiler')),
        ('compartir', _l('Compartir')),
        ('booking', _l('Booking'))
    ], validators=[DataRequired(message=_l('Selecciona el tipo de transacción'))])
    
    tipo_alquiler = SelectField(_l('Tipo de alquiler'), choices=TIPOS_ALQUILER, validators=[Optional()])
    
    estado_propiedad = SelectField(_l('Estado de la propiedad'), choices=ESTADOS_PROPIEDAD, validators=[Optional()])
    
    # Characteristics are handled dynamically
    m2 = FloatField(_l('Tamaño (m²)'), validators=[DataRequired(message=_l('El tamaño es requerido')), NumberRange(min=0)])
    habitaciones = SelectField(_l('N.º Habitaciones'), choices=OPCIONES_HABITACIONES_BANOS, validators=[Optional()])
    banos = SelectField(_l('N.º Baños'), choices=OPCIONES_HABITACIONES_BANOS, validators=[Optional()])
    
    # Specific fields for sections
    caracteristicas_vivienda = SelectMultipleField(_l('Características de la vivienda'), 
                                                  choices=CARACTERISTICAS_VIVIENDA,
                                                  option_widget=CheckboxInput(),
                                                  widget=ListWidget(prefix_label=False),
                                                  validators=[Optional()])
    
    caracteristicas_oficina = SelectMultipleField(_l('Características de la oficina'),
                                                 choices=CARACTERISTICAS_OFICINA,
                                                 option_widget=CheckboxInput(),
                                                 widget=ListWidget(prefix_label=False),
                                                 validators=[Optional()])
    
    caracteristicas_local = SelectMultipleField(_l('Características de locales y naves'),
                                               choices=CARACTERISTICAS_LOCAL,
                                               option_widget=CheckboxInput(),
                                               widget=ListWidget(prefix_label=False),
                                               validators=[Optional()])
    
    caracteristicas_terreno = SelectMultipleField(_l('Características del terreno'),
                                                 choices=CARACTERISTICAS_TERRENO,
                                                 option_widget=CheckboxInput(),
                                                 widget=ListWidget(prefix_label=False),
                                                 validators=[Optional()])
    
    # Media uploads
    imagenes = MultipleFileField(_l('Imágenes'), validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], _l('Solo se permiten imágenes'))
    ])
    videos = MultipleFileField(_l('Videos'), validators=[
        FileAllowed(['mp4', 'avi', 'mov'], _l('Solo se permiten videos'))
    ])
    
    destacado = BooleanField(_l('Destacar oferta'))
    estado = SelectField(_l('Estado de la oferta'), choices=[
        ('abierta', _l('Abierta')),
        ('activada', _l('Activada')),
        ('desactivada', _l('Desactivada')),
        ('caducada', _l('Caducada'))
    ], validators=[DataRequired()], default='abierta')
    
    fecha_baja_programada = DateField(_l('Fecha de baja programada'), validators=[Optional()], format='%Y-%m-%d')


class ContactoForm(FlaskForm):
    """Contact form for property inquiries"""
    nombre = StringField(_l('Nombre'), validators=[
        DataRequired(message=_l('El nombre es requerido')),
        Length(max=100)
    ])
    email = StringField(_l('Email'), validators=[
        DataRequired(message=_l('El email es requerido')),
        Email(message=_l('Email inválido'))
    ])
    telefono = StringField(_l('Teléfono'), validators=[
        DataRequired(message=_l('El teléfono es requerido'))
    ])
    mensaje = TextAreaField(_l('Mensaje'), validators=[
        DataRequired(message=_l('El mensaje es requerido'))
    ])
    
    # For rentals
    fecha_entrada = DateField(_l('Fecha de entrada'), validators=[Optional()], format='%Y-%m-%d')
    fecha_salida = DateField(_l('Fecha de salida'), validators=[Optional()], format='%Y-%m-%d')


class QuejaForm(FlaskForm):
    """Complaint form for registered users"""
    titulo = StringField(_l('Título'), validators=[
        DataRequired(message=_l('El título es requerido')),
        Length(max=200)
    ])
    categoria = SelectField(_l('Categoría'), choices=[
        ('', _l('Seleccionar...')),
        ('fraude', _l('Posible fraude')),
        ('informacion_incorrecta', _l('Información incorrecta')),
        ('spam', _l('Spam')),
        ('otro', _l('Otro'))
    ], validators=[DataRequired(message=_l('Selecciona una categoría'))])
    descripcion = TextAreaField(_l('Descripción'), validators=[
        DataRequired(message=_l('La descripción es requerida'))
    ])
    oferta_id = HiddenField(_l('Oferta ID'), validators=[Optional()])
    adjunto = FileField(_l('Adjunto (opcional)'), validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf'], _l('Solo se permiten imágenes o PDF'))
    ])


class SearchForm(FlaskForm):
    """Search and filter form for properties"""
    q = StringField(_l('Búsqueda'), validators=[Optional()])
    ubicacion = StringField(_l('Ubicación'), validators=[Optional()])
    tipo_propiedad = SelectField(_l('Tipo'), choices=[
        ('', _l('Cualquiera')),
        ('Apartamento', _l('Apartamento')),
        ('Casa', _l('Casa')),
        ('Local', _l('Local comercial')),
        ('Terreno', _l('Terreno'))
    ], validators=[Optional()])
    precio_min = FloatField(_l('Precio mínimo (FCFA)'), validators=[Optional()])
    precio_max = FloatField(_l('Precio máximo (FCFA)'), validators=[Optional()])
    habitaciones = SelectField(_l('Habitaciones'), choices=[
        ('', _l('Cualquiera')),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4+')
    ], validators=[Optional()])
    
    # Quick filters
    parking = BooleanField(_l('Con parking'))
    amueblado = BooleanField(_l('Amueblado'))
    mascotas = BooleanField(_l('Admite mascotas'))
    obra_nueva = BooleanField(_l('Obra nueva'))


class AdvancedSearchForm(FlaskForm):
    """Advanced search form for properties with dynamic filters (Venta/Alquiler)"""
    
    # ===== FILTROS GENERALES =====
    
    # Ubicación
    ciudad = SelectField(_l('Ciudad'), choices=get_ciudades_choices(), validators=[Optional()])
    barrio = StringField(_l('Barrio'), validators=[Optional()])
    
    # Tipo de alquiler
    tipo_alquiler = SelectField(_l('Tipo de alquiler'), 
                                choices=TIPOS_ALQUILER, 
                                validators=[Optional()])
    
    # Tipo de propiedad principal
    tipo_propiedad = SelectField(_l('Tipo de propiedad'), 
                                 choices=TIPOS_PROPIEDAD, 
                                 validators=[Optional()])
    
    # Estado de la propiedad
    estado_propiedad = SelectField(_l('Estado de la propiedad'), 
                                   choices=ESTADOS_PROPIEDAD, 
                                   validators=[Optional()])
    
    # Rango de precio
    precio_min = FloatField(_l('Precio mínimo (FCFA)'), validators=[Optional(), NumberRange(min=0)])
    precio_max = FloatField(_l('Precio máximo (FCFA)'), validators=[Optional(), NumberRange(min=0)])
    
    # Rango de tamaño
    tamano_min = FloatField(_l('Tamaño mínimo (m²)'), validators=[Optional(), NumberRange(min=0)])
    tamano_max = FloatField(_l('Tamaño máximo (m²)'), validators=[Optional(), NumberRange(min=0)])
    
    # ===== FILTROS DEPENDIENTES - VIVIENDA =====
    
    # Subtipo de vivienda
    subtipo_vivienda = SelectField(_l('Tipo de vivienda'), 
                                   choices=SUBTIPOS_VIVIENDA, 
                                   validators=[Optional()])
    
    # Habitaciones y baños
    habitaciones = SelectField(_l('Habitaciones'), 
                              choices=OPCIONES_HABITACIONES_BANOS, 
                              validators=[Optional()])
    banos = SelectField(_l('Baños'), 
                       choices=OPCIONES_HABITACIONES_BANOS, 
                       validators=[Optional()])
    
    # Características de vivienda (multi-selección)
    caracteristicas_vivienda = SelectMultipleField(
        _l('Características'),
        choices=CARACTERISTICAS_VIVIENDA,
        validators=[Optional()],
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False)
    )
    
    # ===== FILTROS DEPENDIENTES - LOCALES Y NAVES =====
    
    # Tipología de local
    tipologia_local = SelectField(_l('Tipología'), 
                                  choices=TIPOLOGIAS_LOCAL, 
                                  validators=[Optional()])
    
    # Características de local (multi-selección)
    caracteristicas_local = SelectMultipleField(
        _l('Características'),
        choices=CARACTERISTICAS_LOCAL,
        validators=[Optional()],
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False)
    )
    
    # ===== FILTROS DEPENDIENTES - OFICINAS =====
    
    # Tipología de oficina
    tipologia_oficina = SelectField(_l('Tipología'), 
                                    choices=TIPOLOGIAS_OFICINA, 
                                    validators=[Optional()])
    
    # Características de oficina (multi-selección)
    caracteristicas_oficina = SelectMultipleField(
        _l('Características'),
        choices=CARACTERISTICAS_OFICINA,
        validators=[Optional()],
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False)
    )
    # ===== FILTROS DEPENDIENTES - SOLARES Y TERRENOS =====
    
    # Características de terreno (multi-selección)
    caracteristicas_terreno = SelectMultipleField(
        _l('Características'),
        choices=CARACTERISTICAS_TERRENO,
        validators=[Optional()],
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False)
    )

class PerfilForm(FlaskForm):
    """User profile editing form"""
    nombre = StringField(_l('Nombre completo'), validators=[
        DataRequired(message=_l('El nombre es requerido')),
        Length(min=3, max=100)
    ])
    telefono = StringField(_l('Teléfono'), validators=[
        Optional(), Length(max=20)
    ])
    sobre_mi = TextAreaField(_l('Sobre mí'), validators=[
        Optional(), Length(max=500)
    ])
    avatar = FileField(_l('Avatar'), validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], _l('Solo se permiten imágenes (jpg, png, webp)'))
    ])

class ReservaForm(FlaskForm):
    """Booking form for properties"""
    fecha_inicio = DateField(_l('Fecha de inicio'), validators=[
        DataRequired(message=_l('La fecha de inicio es requerida'))
    ], format='%Y-%m-%d')
    fecha_fin = DateField(_l('Fecha de fin'), validators=[
        DataRequired(message=_l('La fecha de fin es requerida'))
    ], format='%Y-%m-%d')
    notas = TextAreaField(_l('Notas (Opcional)'), validators=[
        Optional()
    ])
    
    def validate_fecha_fin(self, field):
        if self.fecha_inicio.data and field.data and field.data <= self.fecha_inicio.data:
            raise ValidationError(_l('La fecha de fin debe ser posterior a la fecha de inicio.'))
