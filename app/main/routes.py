from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.main.forms import LocationForm
from app.models import Location

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = LocationForm()
    # lógica para adicionar um novo local
    if form.validate_on_submit():
        # Cria um novo objeto Location associado ao usuário atual
        location = Location(name=form.name.data, owner=current_user)
        db.session.add(location)
        db.session.commit()
        flash('Novo local adicionado com sucesso!', 'success')
        return redirect(url_for('main.dashboard')) # Redireciona para limpar o formulário
    
    # Lógica para buscar os locais APENAS do usuário logado (AUTORIZAÇÃO)
    locations = Location.query.filter_by(user_id=current_user.id).order_by(Location.name).all()
    
    return render_template('dashboard.html', title='Menu Painel', form=form, locations=locations)
