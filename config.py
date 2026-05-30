import os
from datetime import timedelta

import sys

# Detect if we are running as a bundle (PyInstaller)
if getattr(sys, 'frozen', False):
    # If running as a bundle, the real folder is where the .exe is
    # sys._MEIPASS is where temporary assets are extracted
    bundle_dir = sys._MEIPASS
    basedir = os.path.abspath(os.path.dirname(sys.executable))
else:
    # Standard development mode
    bundle_dir = os.path.abspath(os.path.dirname(__file__))
    basedir = bundle_dir


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    # Use basedir for the database so it remains in the same folder as the .exe
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'equahome.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File uploads
    # Uploads should go to basedir (where the exe is) to persist
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'avi', 'mov'}
    
    # Pagination
    PROPERTIES_PER_PAGE = 12
    CONTACTS_PER_PAGE = 20
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@equahome.gq'
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True  # Only send cookie over HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    
    # Security
    WTF_CSRF_TIME_LIMIT = None  # CSRF tokens don't expire
    WTF_CSRF_SSL_STRICT = True  # Require HTTPS for CSRF
    
    # Babel (i18n)  
    BABEL_DEFAULT_LOCALE = 'es'
    BABEL_SUPPORTED_LOCALES = ['es', 'en', 'fr']
    # Translations are read-only assets, so we use bundle_dir
    BABEL_TRANSLATION_DIRECTORIES = os.path.join(bundle_dir, 'app', 'translations')
    
    # Application
    APP_NAME = 'EquaHome'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@equahome.gq'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development
    WTF_CSRF_SSL_STRICT = False  # Allow HTTP in development


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Use PostgreSQL in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost/equahome'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
