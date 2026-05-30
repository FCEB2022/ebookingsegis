import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_babel import Babel
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
babel = Babel()


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    
    # Initialize Babel with locale selector
    from app.babel_config import get_locale
    babel.init_app(app, locale_selector=get_locale)
    
    # Initialize custom template filters
    from app.filters import init_filters
    init_filters(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    
    # Language switcher route
    from flask import redirect, url_for, request
    @app.route('/set_language/<lang>')
    def set_language(lang):
        from app.babel_config import LANGUAGES
        if lang in LANGUAGES:
            session['language'] = lang
        return redirect(request.referrer or url_for('main.index'))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        from flask import render_template
        return render_template('errors/403.html'), 403
    
    # Context processor for global template variables
    @app.context_processor
    def inject_globals():
        from app.babel_config import LANGUAGES
        from flask import session
        return {
            'app_name': app.config['APP_NAME'],
            'languages': LANGUAGES,
            'current_language': session.get('language', 'es')
        }
    
    return app


# Import models after db initialization to avoid circular imports
from app import models
