from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from ..extensions import db, bcrypt
from app.models import User 
from app.auth.forms import LoginForm, RegistrationForm 
from app.auth import bp

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # se o usuário estiver logado, redireciona para a página inicial
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    # Se o formulário for enviado e for válido
    if form.validate_on_submit():

        user = User(username=form.username.data, email=form.email.data)
        
        user.set_password(form.password.data) # Usa o novo método do modelo
        
        # Adiciona o novo usuário ao banco de dados
        db.session.add(user)
        db.session.commit()

        # Mostar uma mensagem de sucesso e redireciona para o login
        flash('Sua conta foi criada com sucesso! Agora você pode fazer o login.', 'success')
        return redirect(url_for('auth.login'))
    
    # Se a requisição for GET, apenas mostra a página com o formulário
    print("Erros do formulário:", form.errors)
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
            
            print(f"--- LOGIN SUCESSO: Tentando logar o usuário ID: {user.id}, Nome: {user.username} ---")
    
            login_user(user, remember=form.remember_me.data)
            
            print(f"--- LOGIN_USER CHAMADO. current_user.is_authenticated AGORA É: {current_user.is_authenticated} ---")
    
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