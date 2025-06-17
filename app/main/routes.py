from flask import render_template
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    return "Olá, GVA-WEB! Esta é a página principal."