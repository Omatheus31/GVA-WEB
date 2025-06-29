from flask import Flask
from config import Config
from .extensions import db, migrate, login_manager, bcrypt, csrf, recaptcha, mail

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

    @app.after_request
    def add_security_headers(response):
        # Adiciona cabeçalhos de segurança em todas as respostas HTTP
        # para fortalecer a aplicação contra ataques comuns como XSS e Clickjacking.
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

# Importa os modelos no final para evitar importações circulares com o 'db'
from app import models