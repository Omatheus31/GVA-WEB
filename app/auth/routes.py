from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from ..extensions import db, bcrypt, recaptcha
from app.models import User 
from app.auth.forms import LoginForm, RegistrationForm, PasswordResetRequestForm, ResetPasswordForm 
from app.auth import bp
from .email import send_password_reset_email

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

        # Mostar uma mensagem de sucesso e redireciona para o login
        flash('Sua conta foi criada com sucesso! Agora você pode fazer o login.', 'success')
        return redirect(url_for('auth.login'))
    
    # Se a requisição for GET, apenas mostra a página com o formulário
    return render_template('auth/register.html', title='Registrar', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # Verifica se o usuário existe E se a senha digitada corresponde ao hash no banco
        if user and user.check_password(form.password.data):
            
            login_user(user, remember=form.remember_me.data)
            
            # Redireciona para a página que o usuário tentava acessar antes de ser enviado para o login
            next_page = request.args.get('next')
            flash('Login realizado com sucesso!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
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
        flash('Sua senha foi redefinida com suceeso! Você já pode fazer o login', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', title="Redefinir Senha", form=form)
