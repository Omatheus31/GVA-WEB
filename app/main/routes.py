from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.main.forms import LocationForm, FoodItemForm
from app.models import Location, FoodItem

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Cria uma instância de cada formulário
    location_form = LocationForm()
    food_form = FoodItemForm()

    # Popula o menu suspenso de locais no formulário de alimento
    # Isso pega todos os locais do usuário e os tranforma em opções para o dropdown
    location_choices = [(loc.id, loc.name) for loc in Location.query.filter_by(user_id=current_user.id).order_by('name').all()]
    food_form.location.choices = location_choices

    # Verifica se o formulário de ADICIONAR LOCAL foi enviado
    if location_form.submit_location.data and location_form.validate_on_submit():
        
        existing_location = Location.query.filter_by(user_id=current_user.id, name=location_form.name.data).first()
        if existing_location:
            flash('Você já tem um local com este nome. Por favor, escolha outro.', 'warning')
        else:
            location = Location(name=location_form.name.data, owner=current_user)
            db.session.add(location)
            db.session.commit()
            flash('Novo local adicionado com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))
    
    # Verifica se o formulário de ADICIONAR ALIMENTO foi enviado
    if food_form.submit_food.data and food_form.validate_on_submit():
        food_item = FoodItem(name=food_form.name.data,
                             quantity=food_form.quantity.data,
                             expiry_date=food_form.expiry_date.data,
                             location_id=food_form.location.data,
                             owner=current_user) 
        db.session.add(food_item)
        db.session.commit()
        flash('Novo alimento adicionado com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))
        
    # Busca dos dados para exibir na página
    locations = Location.query.filter_by(user_id=current_user.id).order_by('name').all()
    food_items = FoodItem.query.filter_by(user_id=current_user.id).order_by(FoodItem.expiry_date).all()

    # Envia tudo para o template
    return render_template('dashboard.html',
                           title='Meu Painel',
                           location_form=location_form,
                           food_form=food_form,
                           locations=locations,
                           food_items=food_items)