from flask import render_template
from app.main import bp
from flask_login import current_user

@bp.route('/')
@bp.route('/index')
def index():
    # ---- INÍCIO DO DEBUG ----
    print(f"--- ROTA INDEX: O current_user é: {current_user} ---")
    print(f"--- ROTA INDEX: current_user.is_authenticated é: {current_user.is_authenticated} ---")
    # ---- FIM DO DEBUG ----
    return render_template('index.html')