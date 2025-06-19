from flask import Flask
from config import Config
from .extensions import db, migrate, login_manager, bcrypt, csrf, recaptcha

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

    # Configurações do Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça o login para acessar esta página.'
    login_manager.login_message_category = 'info'

    # Registra os Blueprints
    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

# Importa os modelos no final para evitar importações circulares com o 'db'
from app import models