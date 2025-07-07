from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from ..extensions import db, bcrypt, recaptcha
from app.models import User, AuditLog
from app.auth.forms import LoginForm, RegistrationForm, PasswordResetRequestForm, ResetPasswordForm, TwoFactorVerifyForm 
from app.auth import bp
from .email import send_password_reset_email, send_confirmation_email
import pyotp

def log_audit(action, user_id=None, details=None):
    log = AuditLog(
        action=action,
        user_id=user_id,
        ip_address=request.remote_addr,
        details=details
    )
    db.session.add(log)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # se o usuário estiver logado, redireciona para a página inicial
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    # Se o formulário for enviado e for válido
    if form.validate_on_submit() and recaptcha.verify():

        user = User(username=form.username.data, email=form.email.data)
        
        user.set_password(form.password.data) # Usa o novo método do modelo
        
        # Adiciona o novo usuário ao banco de dados
        db.session.add(user)
        db.session.commit()

        # Envia o e-mail de confirmação
        send_confirmation_email(user) 

        # Mosta uma mensagem de instrução para o usuário
        flash('Um e-mail de confirmação foi enviado para sua caixa de entrada. Por favor, ative sua conta.', 'success')
        
        # Redireciona para a página de login
        return redirect(url_for('auth.login'))
    
    

    if request.method == 'POST':
        print("--- ERROS DO FORMULÁRIO DE REGISTRO:", form.errors)
        if not recaptcha.verify():
            print("--- A VERIFICAÇÃO DO RECAPTCHA FALHOU ---")

    return render_template('auth/register.html', title='Registrar', form=form)



    # Se a requisição for GET, apenas mostra a página com o formulário
    return render_template('auth/register.html', title='Registrar', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            
            # verifica se a conta foi confirmada antes de permitir o login
            if not user.is_confirmed:
                flash('Sua conta ainda não foi confirmada. Por favor, verifique seu e-mail.', 'warning')
                return redirect(url_for('auth.login'))
            
            if user.tfa_enabled:
                session['2fa_user_id'] = user.id
                return redirect(url_for('auth.tfa_verify'))

            login_user(user)
            log_audit('LOGIN_SUCCESS', user_id=user.id, details=f"User '{user.username}' logged in successfully.")
            db.session.commit()
            next_page = request.args.get('next')
            flash('Login realizado com sucesso!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            log_audit('LOGIN_FAILED', details=f"Failed login attempt for username '{form.username.data}'.")
            db.session.commit()

            flash('Login sem sucesso. Por favor, verifique seu usuário e senha.', 'danger')
        
    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Verifique seu e-mail para as instruções de redefinição de senha.', 'info') 
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Redefinir Senha', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user = User.verify_reset_password_token(token)
    if not user:
        flash('O token de redefinição de senha é inválido ou expirou.', 'warnig')
        return redirect(url_for('main.index'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Sua senha foi redefinida com sucesso! Você já pode fazer o login', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', title="Redefinir Senha", form=form)

@bp.route('/2fa_verify', methods=['GET', 'POST'])
def tfa_verify():
    if '2fa_user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['2fa_user_id'])
    if not user:
        return redirect(url_for('auth.login'))
    
    form = TwoFactorVerifyForm()
    if form.validate_on_submit():
        totp = pyotp.TOTP(user.tfa_secret)
        if totp.verify(form.code.data):
            login_user(user)

            log_audit('2FA_SUCCESS', user_id=user.id, details=f"User '{user.username}' completed 2FA.")
            db.session.commit()

            session.pop('2fa_user_id')

            next_page = request.args.get('next')
            flash('Login realizado com sucesso!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Código 2FA inválido.', 'danger')
    
    return render_template('auth/2fa_verify.html', form=form)

@bp.route('/confirm/<token>')
def confirm_email(token):

    user = User.verify_confirmation_token(token)

    if user is None:
        flash('O link de confirmação é inválido ou expirou.', 'danger')
        return redirect(url_for('auth.login'))
    
    if user.is_confirmed:
        flash('Sua conta já foi confirmada. POr favor, faça o login.', 'info')
    else:
        user.is_confirmed = True
        db.session.commit()
        flash('Sua conta foi confirmada com sucesso.', 'success')
    
    return redirect(url_for('auth.login'))
