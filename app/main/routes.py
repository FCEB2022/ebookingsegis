from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from flask_babel import gettext as _
from app import db
from app.main import bp
from app.models import Oferta, Contacto, Favorito, Reserva
from app.forms import ContactoForm, SearchForm, AdvancedSearchForm, ReservaForm
from app.services.whatsapp_service import WhatsAppService
import json
from sqlalchemy import or_, and_


@bp.route('/')
@bp.route('/index')
def index():
    """Homepage with search"""
    form = SearchForm()
    
    # Get featured properties
    destacadas = Oferta.query.filter_by(estado='activo', destacado=True).limit(6).all()
    
    # Statistics
    total_propiedades = Oferta.query.filter_by(estado='activo').count()
    total_alquiler = Oferta.query.filter_by(estado='activo', tipo_operacion='alquiler').count()
    total_venta = Oferta.query.filter_by(estado='activo', tipo_operacion='venta').count()
    
    return render_template('index.html',
                         title='Inicio',
                         form=form,
                         destacadas=destacadas,
                         total_propiedades=total_propiedades,
                         total_alquiler=total_alquiler,
                         total_venta=total_venta)


@bp.route('/alquiler')
def alquiler():
    """Rental listings page with advanced filters"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    # Create form for filters
    form = AdvancedSearchForm(request.args, meta={'csrf': False})
    
    # Build query
    query = Oferta.query.filter_by(tipo_operacion='alquiler', estado='activo')
    
    # Apply filters
    query = apply_advanced_filters(query, request.args)
    
    # Pagination
    pagination = query.order_by(Oferta.fecha_creacion.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    ofertas = pagination.items
    
    return render_template('main/alquiler.html',
                         title='Alquiler',
                         ofertas=ofertas,
                         pagination=pagination,
                         form=form)


@bp.route('/compartir')
def compartir():
    """Compartir vivienda search page with advanced filters"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    # Create form for filters
    form = AdvancedSearchForm(request.args, meta={'csrf': False})
    
    # Build query for shared housing/offices
    # For now, we filter by alquiler type since "compartir" is a subset
    query = Oferta.query.filter_by(tipo_operacion='alquiler', estado='activo')
    
    # Apply advanced filters
    query = apply_advanced_filters(query, request.args)
    
    # Pagination
    pagination = query.order_by(Oferta.fecha_creacion.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    ofertas = pagination.items
    
    return render_template('main/compartir.html',
                         title='Compartir Vivienda',
                         ofertas=ofertas,
                         pagination=pagination,
                         form=form)


@bp.route('/booking')
def booking():
    """Booking/Reservation placeholder page"""
    # Future development: redirect to hotel landing or internal booking system
    flash(_('La funcionalidad de Booking estará disponible próximamente.'), 'info')
    return redirect(url_for('main.index'))


@bp.route('/venta')
def venta():
    """Sales listings page"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    # Create form for filters
    form = AdvancedSearchForm(request.args, meta={'csrf': False})
    
    # Build query
    query = Oferta.query.filter_by(tipo_operacion='venta', estado='activo')
    
    # Apply filters
    query = apply_advanced_filters(query, request.args)
    
    # Pagination
    pagination = query.order_by(Oferta.fecha_creacion.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    ofertas = pagination.items
    
    return render_template('main/venta.html',
                         title='Venta',
                         ofertas=ofertas,
                         pagination=pagination,
                         form=form)


@bp.route('/oferta/<int:id>', methods=['GET', 'POST'])
def oferta_detalle(id):
    """Property detail page"""
    oferta = Oferta.query.get_or_404(id)
    
    # Check if user has favorited this property
    es_favorito = False
    if current_user.is_authenticated:
        es_favorito = Favorito.query.filter_by(
            usuario_id=current_user.id,
            oferta_id=id
        ).first() is not None
        
    reserva_form = ReservaForm()
    
    if current_user.is_authenticated and reserva_form.validate_on_submit() and 'reserva_submit' in request.form:
        reserva = Reserva(
            fecha_inicio=reserva_form.fecha_inicio.data,
            fecha_fin=reserva_form.fecha_fin.data,
            notas=reserva_form.notas.data,
            usuario_id=current_user.id,
            oferta_id=id
        )
        db.session.add(reserva)
        db.session.commit()
        flash('Solicitud de reserva enviada correctamente.', 'success')
        return redirect(url_for('main.oferta_detalle', id=id))
    
    # Related properties (same city or type)
    relacionadas = Oferta.query.filter(
        Oferta.id != id,
        Oferta.estado == 'activo',
        or_(
            Oferta.ubicacion.like(f'%{oferta.ubicacion.split(",")[0]}%'),
            Oferta.tipo_propiedad == oferta.tipo_propiedad
        )
    ).limit(3).all()
    
    # Generate WhatsApp Link
    whatsapp_link = WhatsAppService.generar_enlace_oferta(oferta)
    
    return render_template('main/oferta_detalle.html',
                         title=oferta.titulo,
                         oferta=oferta,
                         es_favorito=es_favorito,
                         relacionadas=relacionadas,
                         reserva_form=reserva_form,
                         whatsapp_link=whatsapp_link)


@bp.route('/contactar/<int:id>', methods=['GET', 'POST'])
def contactar(id):
    """Contact form for property"""
    oferta = Oferta.query.get_or_404(id)
    form = ContactoForm()
    
    # Pre-fill form if user is logged in
    if current_user.is_authenticated and request.method == 'GET':
        form.nombre.data = current_user.nombre
        form.email.data = current_user.email
        form.telefono.data = current_user.telefono
    
    if form.validate_on_submit():
        contacto = Contacto(
            nombre=form.nombre.data,
            email=form.email.data,
            telefono=form.telefono.data,
            mensaje=form.mensaje.data,
            fecha_entrada=form.fecha_entrada.data,
            fecha_salida=form.fecha_salida.data,
            oferta_id=id,
            usuario_id=current_user.id if current_user.is_authenticated else None
        )
        
        db.session.add(contacto)
        db.session.commit()
        
        # TODO: Send email notifications
        
        flash('Tu mensaje ha sido enviado correctamente. El propietario se pondrá en contacto contigo pronto.', 'success')
        return redirect(url_for('main.oferta_detalle', id=id))
    
    # Generate WhatsApp link
    whatsapp_link = WhatsAppService.generar_enlace_oferta(oferta)
    
    return render_template('main/contacto.html',
                         title=f'Contactar - {oferta.titulo}',
                         form=form,
                         oferta=oferta,
                         whatsapp_link=whatsapp_link)


@bp.route('/buscar')
def buscar():
    """Search endpoint"""
    query_text = request.args.get('q', '')
    tipo_operacion = request.args.get('tipo_operacion', '')
    
    # Build base query
    query = Oferta.query.filter_by(estado='activo')
    
    # Filter by operation type if specified
    if tipo_operacion:
        query = query.filter_by(tipo_operacion=tipo_operacion)
    
    # Text search
    if query_text:
        query = query.filter(
            or_(
                Oferta.titulo.ilike(f'%{query_text}%'),
                Oferta.descripcion.ilike(f'%{query_text}%'),
                Oferta.ubicacion.ilike(f'%{query_text}%')
            )
        )
    
    # Apply other filters
    query = apply_filters(query, request.args)
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Oferta.fecha_creacion.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    return render_template('main/buscar.html',
                         title='Resultados de búsqueda',
                         ofertas=pagination.items,
                         pagination=pagination,
                         query=query_text)


def apply_filters(query, args):
    """Apply basic search filters to query (legacy function)"""
    # Price range
    precio_min = args.get('precio_min', type=float)
    precio_max = args.get('precio_max', type=float)
    if precio_min:
        query = query.filter(Oferta.precio >= precio_min)
    if precio_max:
        query = query.filter(Oferta.precio <= precio_max)
    
    # Location
    ubicacion = args.get('ubicacion', '')
    if ubicacion:
        query = query.filter(Oferta.ubicacion.ilike(f'%{ubicacion}%'))
    
    # Property type
    tipo_propiedad = args.get('tipo_propiedad', '')
    if tipo_propiedad:
        query = query.filter_by(tipo_propiedad=tipo_propiedad)
    
    # Rooms
    habitaciones = args.get('habitaciones', '')
    if habitaciones:
        if habitaciones == '4':
            # 4+ rooms
            query = query.filter(Oferta.caracteristicas.like('%"habitaciones": "%4%"%'))
        else:
            query = query.filter(Oferta.caracteristicas.like(f'%"habitaciones": "{habitaciones}"%'))
    
    return query


def apply_advanced_filters(query, args):
    """Apply advanced search filters to query"""
    
    # ===== FILTROS GENERALES =====
    
    # Ciudad
    ciudad = args.get('ciudad', '')
    if ciudad:
        query = query.filter(Oferta.ciudad == ciudad)
    
    # Barrio
    barrio = args.get('barrio', '')
    if barrio:
        query = query.filter(Oferta.barrio.ilike(f'%{barrio}%'))
    
    # Tipo de alquiler
    tipo_alquiler = args.get('tipo_alquiler', '')
    if tipo_alquiler:
        query = query.filter(Oferta.tipo_alquiler == tipo_alquiler)
    
    # Tipo de propiedad
    tipo_propiedad = args.get('tipo_propiedad', '')
    if tipo_propiedad:
        query = query.filter(Oferta.tipo_propiedad == tipo_propiedad)
    
    # Estado de la propiedad
    estado_propiedad = args.get('estado_propiedad', '')
    if estado_propiedad:
        query = query.filter(Oferta.estado_propiedad == estado_propiedad)
    
    # Rango de precio
    precio_min = args.get('precio_min', type=float)
    precio_max = args.get('precio_max', type=float)
    if precio_min:
        query = query.filter(Oferta.precio >= precio_min)
    if precio_max:
        query = query.filter(Oferta.precio <= precio_max)
    
    # Rango de tamaño
    tamano_min = args.get('tamano_min', type=float)
    tamano_max = args.get('tamano_max', type=float)
    if tamano_min:
        query = query.filter(Oferta.metros_cuadrados >= tamano_min)
    if tamano_max:
        query = query.filter(Oferta.metros_cuadrados <= tamano_max)
    
    # ===== FILTROS DEPENDIENTES =====
    
    # Subtipo de propiedad (vivienda, local, oficina)
    subtipo_vivienda = args.get('subtipo_vivienda', '')
    if subtipo_vivienda:
        query = query.filter(Oferta.subtipo_propiedad == subtipo_vivienda)
    
    tipologia_local = args.get('tipologia_local', '')
    if tipologia_local:
        query = query.filter(Oferta.subtipo_propiedad == tipologia_local)
    
    tipologia_oficina = args.get('tipologia_oficina', '')
    if tipologia_oficina:
        query = query.filter(Oferta.subtipo_propiedad == tipologia_oficina)
    
    # Habitaciones y baños (búsqueda en JSON)
    habitaciones = args.get('habitaciones', '')
    if habitaciones:
        if habitaciones == '4+':
            # 4 o más habitaciones
            query = query.filter(
                or_(
                    Oferta.caracteristicas.like('%"habitaciones": "4"%'),
                    Oferta.caracteristicas.like('%"habitaciones": "5"%'),
                    Oferta.caracteristicas.like('%"habitaciones": "6"%'),
                    Oferta.caracteristicas.like('%"habitaciones": 4%'),
                    Oferta.caracteristicas.like('%"habitaciones": 5%'),
                    Oferta.caracteristicas.like('%"habitaciones": 6%')
                )
            )
        else:
            query = query.filter(
                or_(
                    Oferta.caracteristicas.like(f'%"habitaciones": "{habitaciones}"%'),
                    Oferta.caracteristicas.like(f'%"habitaciones": {habitaciones}%')
                )
            )
    
    banos = args.get('banos', '')
    if banos:
        if banos == '4+':
            query = query.filter(
                or_(
                    Oferta.caracteristicas.like('%"banos": "4"%'),
                    Oferta.caracteristicas.like('%"banos": "5"%'),
                    Oferta.caracteristicas.like('%"banos": "6"%'),
                    Oferta.caracteristicas.like('%"banos": 4%'),
                    Oferta.caracteristicas.like('%"banos": 5%'),
                    Oferta.caracteristicas.like('%"banos": 6%')
                )
            )
        else:
            query = query.filter(
                or_(
                    Oferta.caracteristicas.like(f'%"banos": "{banos}"%'),
                    Oferta.caracteristicas.like(f'%"banos": {banos}%')
                )
            )
    
    # Características (multi-select) - buscar en JSON
    caracteristicas_vivienda = args.getlist('caracteristicas_vivienda')
    caracteristicas_local = args.getlist('caracteristicas_local')
    caracteristicas_oficina = args.getlist('caracteristicas_oficina')
    caracteristicas_terreno = args.getlist('caracteristicas_terreno')
    
    # Combinar todas las características seleccionadas
    todas_caracteristicas = (
        caracteristicas_vivienda + 
        caracteristicas_local + 
        caracteristicas_oficina + 
        caracteristicas_terreno
    )
    
    if todas_caracteristicas:
        # Aplicar filtro para cada característica seleccionada
        for caracteristica in todas_caracteristicas:
            query = query.filter(
                or_(
                    Oferta.caracteristicas.like(f'%"{caracteristica}": true%'),
                    Oferta.caracteristicas.like(f'%"{caracteristica}": "true"%'),
                    Oferta.caracteristicas.like(f'%"{caracteristica}": 1%')
                )
            )
    
    return query
