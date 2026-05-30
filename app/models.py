from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
import json


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return Usuario.query.get(int(user_id))


class Usuario(UserMixin, db.Model):
    """User model for authentication and authorization"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    telefono = db.Column(db.String(20))
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), default='usuario')  # admin, usuario, visitante
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    avatar = db.Column(db.String(255))
    sobre_mi = db.Column(db.Text)
    
    # Relationships
    ofertas = db.relationship('Oferta', backref='propietario', lazy='dynamic')
    contactos = db.relationship('Contacto', backref='usuario', lazy='dynamic')
    quejas = db.relationship('Queja', backref='usuario', lazy='dynamic')
    favoritos = db.relationship('Favorito', backref='usuario', lazy='dynamic')
    reservas = db.relationship('Reserva', backref='usuario', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.rol == 'admin'
    
    def __repr__(self):
        return f'<Usuario {self.email}>'


class Oferta(db.Model):
    """Property listing model"""
    __tablename__ = 'ofertas'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    
    # Location
    ubicacion = db.Column(db.String(200), nullable=False)
    ciudad = db.Column(db.String(100))  # Ciudad separada para búsqueda
    barrio = db.Column(db.String(100))  # Zona/Barrio
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    
    # Property details
    tipo_propiedad = db.Column(db.String(50))  # vivienda, locales_naves, oficinas, terreno
    subtipo_propiedad = db.Column(db.String(50))  # chalet, apartamento, piso, etc.
    tipo_operacion = db.Column(db.String(20))  # alquiler, venta
    tipo_alquiler = db.Column(db.String(20))  # indiferente, larga_duracion, temporada
    
    # Property condition and size
    estado_propiedad = db.Column(db.String(20))  # bien, muy_bien, obra_nueva, a_reformar
    metros_cuadrados = db.Column(db.Float)  # Tamaño en m2
    
    # Characteristics (stored as JSON)
    caracteristicas = db.Column(db.Text)  # JSON: {habitaciones: 3, baños: 2, m2: 120, ...}
    
    # Media
    imagenes = db.Column(db.Text)  # JSON array of image paths
    videos = db.Column(db.Text)  # JSON array of video paths
    
    # Status
    estado = db.Column(db.String(20), default='activo')  # activo, inactivo, vendido, alquilado
    destacado = db.Column(db.Boolean, default=False)
    
    # Rental-specific
    periodos_disponibles = db.Column(db.Text)  # JSON array of date ranges
    
    # Timestamps
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_baja_programada = db.Column(db.Date, nullable=True)  # Programmed deactivation date
    
    # Foreign keys
    propietario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Relationships
    contactos = db.relationship('Contacto', backref='oferta', lazy='dynamic', cascade='all, delete-orphan')
    favoritos = db.relationship('Favorito', backref='oferta', lazy='dynamic', cascade='all, delete-orphan')
    historial = db.relationship('HistorialOferta', backref='oferta', lazy='dynamic', cascade='all, delete-orphan')
    quejas = db.relationship('Queja', backref='oferta', lazy='dynamic')
    reservas = db.relationship('Reserva', backref='oferta', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_caracteristicas(self):
        """Parse JSON characteristics"""
        if self.caracteristicas:
            try:
                return json.loads(self.caracteristicas)
            except:
                return {}
        return {}
    
    def set_caracteristicas(self, data):
        """Set characteristics as JSON"""
        self.caracteristicas = json.dumps(data)
    
    def get_imagenes(self):
        """Parse JSON images array"""
        if self.imagenes:
            try:
                return json.loads(self.imagenes)
            except:
                return []
        return []
    
    def set_imagenes(self, images_list):
        """Set images as JSON array"""
        self.imagenes = json.dumps(images_list)
    
    def get_videos(self):
        """Parse JSON videos array"""
        if self.videos:
            try:
                return json.loads(self.videos)
            except:
                return []
        return []
    
    def set_videos(self, videos_list):
        """Set videos as JSON array"""
        self.videos = json.dumps(videos_list)
    
    def get_periodos(self):
        """Parse JSON available periods"""
        if self.periodos_disponibles:
            try:
                return json.loads(self.periodos_disponibles)
            except:
                return []
        return []
    
    def set_periodos(self, periods_list):
        """Set available periods as JSON"""
        self.periodos_disponibles = json.dumps(periods_list)
    
    def __repr__(self):
        return f'<Oferta {self.titulo}>'


class Contacto(db.Model):
    """Contact form submissions for property inquiries"""
    __tablename__ = 'contactos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20))
    mensaje = db.Column(db.Text, nullable=False)
    
    # Rental-specific
    fecha_entrada = db.Column(db.Date)
    fecha_salida = db.Column(db.Date)
    
    # Status tracking
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, resuelto, archivado
    notas_admin = db.Column(db.Text)  # Admin notes
    
    fecha_contacto = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_resolucion = db.Column(db.DateTime)
    
    # Foreign keys
    oferta_id = db.Column(db.Integer, db.ForeignKey('ofertas.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))  # Optional: if logged in
    
    def __repr__(self):
        return f'<Contacto {self.nombre} - {self.email}>'


class Queja(db.Model):
    """Complaint system for registered users"""
    __tablename__ = 'quejas'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(50))  # fraude, información incorrecta, spam, otro
    
    # Optional attachment
    adjunto = db.Column(db.String(255))  # File path
    
    # Status
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, en_proceso, resuelto
    respuesta_admin = db.Column(db.Text)
    
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_resolucion = db.Column(db.DateTime)
    
    # Foreign keys
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    oferta_id = db.Column(db.Integer, db.ForeignKey('ofertas.id'))  # Optional: related to specific property
    
    def __repr__(self):
        return f'<Queja {self.titulo}>'


class Favorito(db.Model):
    """User favorites for properties"""
    __tablename__ = 'favoritos'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_agregado = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    oferta_id = db.Column(db.Integer, db.ForeignKey('ofertas.id'), nullable=False)
    
    # Unique constraint to prevent duplicate favorites
    __table_args__ = (db.UniqueConstraint('usuario_id', 'oferta_id', name='_usuario_oferta_uc'),)
    
    def __repr__(self):
        return f'<Favorito usuario={self.usuario_id} oferta={self.oferta_id}>'


class HistorialOferta(db.Model):
    """Change history for property listings"""
    __tablename__ = 'historial_ofertas'
    
    id = db.Column(db.Integer, primary_key=True)
    campo_modificado = db.Column(db.String(50))  # Field that was changed
    valor_anterior = db.Column(db.Text)  # Previous value
    valor_nuevo = db.Column(db.Text)  # New value
    usuario_modificador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key
    oferta_id = db.Column(db.Integer, db.ForeignKey('ofertas.id'), nullable=False)
    
    # Relationship
    usuario_modificador = db.relationship('Usuario', foreign_keys=[usuario_modificador_id])
    
    def __repr__(self):
        return f'<HistorialOferta oferta={self.oferta_id} campo={self.campo_modificado}>'


class Reserva(db.Model):
    """Booking model for properties"""
    __tablename__ = 'reservas'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, confirmada, cancelada, completada
    precio_total = db.Column(db.Float)
    notas = db.Column(db.Text)
    
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    oferta_id = db.Column(db.Integer, db.ForeignKey('ofertas.id'), nullable=False)
    
    def __repr__(self):
        return f'<Reserva {self.id} usuario={self.usuario_id} oferta={self.oferta_id}>'
