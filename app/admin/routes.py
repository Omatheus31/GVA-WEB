from flask import render_template
from flask_login import login_required
from app.admin import bp
from app.decorators import admin_required
from app.models import AuditLog, User

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html', title='Painel Admin')

@bp.route('/audit_log')
@login_required
@admin_required
def audit_log():
    # Busca todos os logs, ordenados do mais recente para o mais antigo
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template('admin/audit_log.html', title='Log de Auditoria', logs=logs)

@bp.route('/users')
@login_required
@admin_required
def users_list():
    # Busca todos os usuários
    users = User.query.order_by(User.username).all()
    return render_template('admin/users_list.html', title='Lista de Usuários', users=users)
