from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.user import bp
from app.models import Favorito, Oferta, Queja, Reserva
from app.forms import QuejaForm, PerfilForm
from app.services.file_service import save_uploaded_file


@bp.route('/favoritos')
@login_required
def favoritos():
    """View user's favorite properties"""
    page = request.args.get('page', 1, type=int)
    
    # Get user's favorites with related offers
    favoritos_query = Favorito.query.filter_by(usuario_id=current_user.id)\
        .join(Oferta).filter(Oferta.estado == 'activo')
    
    pagination = favoritos_query.order_by(Favorito.fecha_agregado.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    return render_template('user/favoritos.html',
                         title='Mis Favoritos',
                         favoritos=pagination.items,
                         pagination=pagination)


@bp.route('/favoritos/toggle/<int:oferta_id>', methods=['POST'])
@login_required
def favorito_toggle(oferta_id):
    """Add or remove property from favorites (AJAX)"""
    oferta = Oferta.query.get_or_404(oferta_id)
    
    favorito = Favorito.query.filter_by(
        usuario_id=current_user.id,
        oferta_id=oferta_id
    ).first()
    
    if favorito:
        # Remove from favorites
        db.session.delete(favorito)
        db.session.commit()
        return jsonify({'success': True, 'action': 'removed', 'message': 'Eliminado de favoritos'})
    else:
        # Add to favorites
        favorito = Favorito(usuario_id=current_user.id, oferta_id=oferta_id)
        db.session.add(favorito)
        db.session.commit()
        return jsonify({'success': True, 'action': 'added', 'message': 'Agregado a favoritos'})


@bp.route('/quejas', methods=['GET', 'POST'])
@login_required
def quejas():
    """Submit and view complaints"""
    form = QuejaForm()
    
    if form.validate_on_submit():
        queja = Queja(
            titulo=form.titulo.data,
            categoria=form.categoria.data,
            descripcion=form.descripcion.data,
            usuario_id=current_user.id,
            oferta_id=form.oferta_id.data if form.oferta_id.data else None
        )
        
        # Handle file upload
        if form.adjunto.data:
            filename = save_uploaded_file(form.adjunto.data, 'complaints')
            queja.adjunto = filename
        
        db.session.add(queja)
        db.session.commit()
        
        flash('Tu queja ha sido enviada. La revisaremos pronto.', 'success')
        return redirect(url_for('user.quejas'))
    
    # Get user's complaints
    mis_quejas = Queja.query.filter_by(usuario_id=current_user.id)\
        .order_by(Queja.fecha_creacion.desc()).all()
    
    return render_template('user/quejas.html',
                         title='Mis Quejas',
                         form=form,
                         quejas=mis_quejas)


@bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    """User profile page"""
    form = PerfilForm()
    
    if form.validate_on_submit():
        current_user.nombre = form.nombre.data
        current_user.telefono = form.telefono.data
        current_user.sobre_mi = form.sobre_mi.data
        
        if form.avatar.data:
            filename = save_uploaded_file(form.avatar.data, 'avatars')
            if filename:
                current_user.avatar = filename
                
        db.session.commit()
        flash('Tu perfil ha sido actualizado.', 'success')
        return redirect(url_for('user.perfil'))
    elif request.method == 'GET':
        form.nombre.data = current_user.nombre
        form.telefono.data = current_user.telefono
        form.sobre_mi.data = current_user.sobre_mi

    # Get user statistics
    total_favoritos = Favorito.query.filter_by(usuario_id=current_user.id).count()
    total_contactos = db.session.query(db.func.count(db.distinct('id')))\
        .filter_by(usuario_id=current_user.id).scalar() or 0
    total_quejas = Queja.query.filter_by(usuario_id=current_user.id).count()
    
    return render_template('user/perfil.html',
                         title='Mi Perfil',
                         form=form,
                         total_favoritos=total_favoritos,
                         total_contactos=total_contactos,
                         total_quejas=total_quejas)

@bp.route('/reservas')
@login_required
def mis_reservas():
    """View user's bookings"""
    page = request.args.get('page', 1, type=int)
    reservas = Reserva.query.filter_by(usuario_id=current_user.id)\
        .order_by(Reserva.fecha_creacion.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
    return render_template('user/reservas.html',
                         title='Mis Reservas',
                         reservas=reservas.items,
                         pagination=reservas)
