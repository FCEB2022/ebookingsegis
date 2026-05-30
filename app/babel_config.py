# Babel configuration
from flask import request, session

# Supported languages
LANGUAGES = {
    'es': 'Español',
    'en': 'English',
    'fr': 'Français'
}

def get_locale():
    """Get user's preferred language"""
    # Try to get language from session
    lang = session.get('language')
    if lang in LANGUAGES:
        return lang
    
    # Try to get from request args (for language switcher)
    lang = request.args.get('lang')
    if lang in LANGUAGES:
        session['language'] = lang
        return lang
    
    # Try to get from browser's accept languages
    return request.accept_languages.best_match(LANGUAGES.keys()) or 'es'
