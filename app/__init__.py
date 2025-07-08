from flask import Flask, render_template
from config import Config
from .extensions import db, migrate, login_manager, bcrypt, csrf, recaptcha, mail
import pytz
from datetime import datetime

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa as extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    recaptcha.init_app(app)
    mail.init_app(app)

    # Configurações do Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça o login para acessar esta página.'
    login_manager.login_message_category = 'info'

    # Registra os Blueprints
    from .main import bp as main_bp
    app.register_blueprint(main_bp)
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from .admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Registra os comandos de linha de comando
    from . import cli
    cli.register_commands(app)

    # Registra os manipuladores de erro e filtros
    with app.app_context():
        @app.errorhandler(403)
        def forbidden_error(error):
            return render_template('errors/403.html'), 403

        def format_datetime_local(value, format='%d/%m/%Y %H:%M:%S'):
            if value is None:
                return ""
            local_tz = pytz.timezone('America/Sao_Paulo')
            local_dt = value.replace(tzinfo=pytz.utc).astimezone(local_tz)
            return local_dt.strftime(format)
        
        app.jinja_env.filters['localdatetime'] = format_datetime_local

    # Registra os cabeçalhos de segurança
    @app.after_request
    def add_security_headers(response):
        csp = (
            "default-src 'self';"
            "script-src 'self' 'unsafe-inline' http://www.google.com/recaptcha/ https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/;"
            "style-src 'self' 'unsafe-inline';" 
            "img-src 'self' data:;"
            "font-src 'self';"
            "object-src 'none';"
            "frame-src 'self' http://www.google.com/recaptcha/ https://www.google.com/recaptcha/;"
            "base-uri 'self';"
            "form-action 'self';"
            "frame-ancestors 'none';"
        )
        response.headers['Content-Security-Policy'] = csp
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    return app

# Importa os modelos no final para evitar importações circulares
from app import models