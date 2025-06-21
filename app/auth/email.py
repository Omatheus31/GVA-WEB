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
