# Template filters for the application
from app.ciudades import format_currency_xaf

def currency_filter(value):
    """Format value as XAF currency"""
    try:
        return format_currency_xaf(float(value))
    except (ValueError, TypeError):
        return value

def init_filters(app):
    """Initialize template filters"""
    app.jinja_env.filters['currency'] = currency_filter
