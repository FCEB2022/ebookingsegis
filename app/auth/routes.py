from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from urllib.parse import urlparse
from app import db
from app.auth import bp
from app.forms import LoginForm, RegistrationForm
from app.models import Usuario


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.activo:
            flash('Tu cuenta ha sido desactivada. Contacta al administrador.', 'warning')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        # Redirect to next page or homepage
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')
        
        flash(f'¡Bienvenido, {user.nombre}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Iniciar sesión', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Usuario(
            nombre=form.nombre.data,
            username=form.username.data,
            email=form.email.data,
            telefono=form.telefono.data,
            rol='usuario'  # Default role
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Crear cuenta', form=form)


@bp.route('/logout')
def logout():
    """User logout"""
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('main.index'))
