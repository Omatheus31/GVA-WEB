from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user, fresh_login_required, logout_user
from app import db
from app.auth.routes import log_audit
from app.main import bp
from app.main.forms import LocationForm, FoodItemForm
from app.models import Location, FoodItem, User
import pyotp
import qrcode
import io
import base64
from ..auth.forms import TwoFactorForm, ChangePasswordForm, DeleteAccountForm

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
        
    # Filtra os locais para mostrar APENAS os que pertencem ao usuário logado.
    # Esta é a implementação da Autorização
    locations = Location.query.filter_by(user_id=current_user.id).order_by('name').all()
    food_items = FoodItem.query.filter_by(user_id=current_user.id).order_by(FoodItem.expiry_date).all()

    # Envia tudo para o template
    return render_template('dashboard.html',
                           title='Meu Painel',
                           location_form=location_form,
                           food_form=food_form,
                           locations=locations,
                           food_items=food_items)

@bp.route('/2fa_setup', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def tfa_setup():
    if current_user.tfa_enabled:
        return redirect(url_for('main.dashboard'))
    
    form = TwoFactorForm()

    if 'tfa_secret' not in session:
        session['tfa_secret'] = pyotp.random_base32()

    if form.validate_on_submit():
        totp = pyotp.TOTP(session['tfa_secret'])

        if totp.verify(form.code.data):
            current_user.tfa_secret = session['tfa_secret']
            current_user.tfa_enabled = True
            db.session.commit()
            session.pop('tfa_secret')
            flash('2FA ativado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Código inválido. Tente novamente.', 'danger')
            return redirect(url_for('main.tfa_setup'))
    
    provisioning_uri = pyotp.totp.TOTP(session['tfa_secret']).provisioning_uri(
        name=current_user.username,
        issuer_name='GVA-WEB'
    )

    img = qrcode.make(provisioning_uri)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    qr_code_data = base64.b64encode(buf.getvalue()).decode('ascii')

    return render_template('2fa_setup.html', title='Configurar 2FA',
                           form=form, qr_code_data=qr_code_data)

@bp.route('/location/<int:location_id>/delete', methods=['POST'])
@login_required
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)

    # AUTORIZAÇÃO: Garante que o usuário só pode apagar seus próprios locais
    if location.owner != current_user:
        flash('Operação não permitida.', 'danger')
        return redirect(url_for('main'))
    
    db.session.delete(location)
    db.session.commit()
    flash('Local excluído com sucesso!', 'success')
    return redirect(url_for('main.dashboard'))


@bp.route('/location/<int:location_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)

    # AUTRORIZAÇÃO: Garante que o usuário só pode editar seus prórpios locais
    if location.owner != current_user:
        flash('Operação não permitida.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = LocationForm()
    if form.validate_on_submit():
        # Lógica para evitar nomes duplicados, igual à da criação
        existing_location = Location.query.filter(Location.id != location_id, Location.user_id == current_user.id, Location.name == form.name.data).first()
        if existing_location:
            flash('Você já tem um local com este nome.', 'warning')
        else:
            location.name = form.name.data
            db.session.commit()
            flash('Seu local foi atualizado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        
    elif request.method == 'GET':
        # Pré-preenche o formulário com o nome atual do local
        form.name.data = location.name
    
    return render_template('edit_location.html', title='Editar Local', form=form)

@bp.route('/food_item/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_food_item(item_id):
    item = FoodItem.query.get_or_404(item_id)

    # AUTORIZAÇÃO: Garante que o usuário só pode apagar seus próprios itens
    if item.owner != current_user:
        flash('Operação não permitida.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(item)
    db.session.commit()
    flash('Alimento excluído com sucesso!', 'success')
    return redirect(url_for('main.dashboard'))


@bp.route('/food_item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_food_item(item_id):
    item = FoodItem.query.get_or_404(item_id)

    # AUTORIZAÇÃO: Garante que o usuário só pode editar seus próprios itens
    if item.owner != current_user:
        flash('Operação não permitida.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = FoodItemForm()

    # Popula o dropdown de locais
    form.location.choices = [(loc.id, loc.name) for loc in Location.query.filter_by(user_id=current_user.id).order_by('name').all()]

    if form.validate_on_submit():
        item.name = form.name.data
        item.quantity = form.quantity.data
        item.expiry_date = form.expiry_date.data
        item.location_id = form.location.data
        db.session.commit()
        flash('Seu alimento foi atualizado com sucesso!', 'success')       
        return redirect(url_for('main.dashboard'))
    elif request.method == 'GET':
        # Pré-preenche o formulário com os dados atuais do item
        form.name.data = item.name
        form.quantity.data = item.quantity
        form.expiry_date.data = item.expiry_date
        form.location.data = item.location_id

    return render_template('edit_food_item.html', title='Editar Alimento', form=form)

@bp.route('/terms')
def terms():
    return render_template('legal/terms.html', title='Termos de Uso')

@bp.route('/security-policy')
def security_policy():
    return render_template('legal/security_policy.html', title='Política de Segurança')

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # Verifica se a senha atual fornecida está correta
        if current_user.check_password(form.current_password.data):
            # Se sim, atualiza para a nova senha
            current_user.set_password(form.new_password.data)

            # Adiciona um log de auditoria para a mudança de senha
            log_audit('PASSWORD_CHANGED', user_id=current_user.id, details="User changed their password successfully.")

            db.session.commit()

            # Faz o logout do usuário por segurança
            logout_user()
            flash('Sua senha foi alterada com sucesso! Por favor, faça o login novamente com sua nova senha.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Sua senha atual está incorreta.', 'danger')

    return render_template('change_password.html', title='Alterar Senha', form=form)


@bp.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        # Varifica se a senha fornecida para a confirmação está correta
        if current_user.check_password(form.password.data):
            # Guarda o usuário em uma variável temporária antes de deslogar
            user_to_delete = User.query.get(current_user.id)
            username = user_to_delete.username

            # Deleta o usuário do banco juntamente com os dados pertencente a ele
            db.session.delete(user_to_delete)
            db.session.commit()

            #Faz o logout para invalidar a sessão antes de apagar
            logout_user()

            flash(f'A conta de {username} foi exluída permanentemente. Sentiremos sua falta!', 'info')
            return redirect(url_for('main.index'))
        else:
            flash('Senha incorreta. A exclusão da sua conta foi cancelada.', 'danger')
            return redirect(url_for('main.delete_account'))
    
    return render_template('delete_account.html', title='Excluir Conta', form=form)