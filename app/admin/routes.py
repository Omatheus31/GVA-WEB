from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.admin import bp
from app.decorators import admin_required
from app.models import AuditLog, User
from app.extensions import db

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

@bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)

    # Medida de segurança extra para impedir que um admin se auto-delete
    if user_to_delete.id == current_user.id:
        flash('Você não pode excluir sua própria conta de administrador.', 'danger')
        return redirect(url_for('admin.users_list'))
    
    db.session.delete(user_to_delete)
    db.session.commit()

    flash(f"O usuário '{user_to_delete.username}' foi excluído com sucesso.", 'success')
    return redirect(url_for('admin.users_list'))