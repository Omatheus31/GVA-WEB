from flask import render_template, current_app
from flask_mail import Message
from app.extensions import mail

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    msg = Message('Redefinição de Senha - GVA-WEB',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = render_template('auth/email/reset_password.txt',
                               user=user, token=token)
    msg.html = render_template('auth/email/reset_password.html',
                               user=user, token=token)
    mail.send(msg)

def send_expiry_alert_email(user, items):
    """Envia o e-mail de alerta de validade com uma lista de itens."""
    msg = Message('Alerta de Validade de Alimentos - GVA-WEB',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.html = render_template('auth/email/expiry_alert.html',
                               user=user, items=items)
    mail.send(msg)