from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
import re

# Validador customizado para complexidade de senha
def password_complexity(form, field):
    password = field.data
    if not re.search(r'[A-Z]', password):
        raise ValidationError('A senha deve conter pelo menos uma letra maiúscula.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('A senha deve conter pelo menos uma letra minúscula.')
    if not re.search(r'[0-9]', password):
        raise ValidationError('A senha deve conter pelo menos um número.')
    # Corrigido: 'contem' para 'conter'
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError('A senha deve conter pelo menos um caractere especial (!@#$ etc).')

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(message="Por favor, insira seu nome de usuário.")])
    password = PasswordField('Senha', validators=[DataRequired(message="Por favor, insira sua senha.")])
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[
        DataRequired(message="O nome de usuário é obrigatório."), 
        Length(min=4, max=64, message="O nome de usuário deve ter entre 4 e 64 caracteres.")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="O e-mail é obrigatório."), 
        Email(message="Por favor, insira um endereço de e-mail válido.")
    ])
    email2 = StringField('Repita o Email', validators=[
        DataRequired(message="A confirmação de e-mail é obrigatória."), 
        EqualTo('email', message='Os e-mails devem ser iguais.')
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(message="A senha é obrigatória."), 
        Length(min=8, message="A senha deve ter no mínimo 8 caracteres."), 
        password_complexity
    ])
    password2 = PasswordField('Repita a Senha', validators=[
        DataRequired(message="A confirmação de senha é obrigatória."), 
        EqualTo('password', message='As senhas devem ser iguais.')
    ])
    accept_terms = BooleanField(
        'Eu li e aceito os Termos de Uso e a Política de Segurança.',
        validators=[DataRequired(message='Você deve aceitar os termos para se registrar.')]
    )
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro.')
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Este email já está em uso. Por favor, escolha outro.')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Por favor, insira seu e-mail."), 
        Email(message="Endereço de e-mail inválido.")
    ])
    submit = SubmitField('Pedir Redefinição de Senha')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nova Senha', validators=[
        DataRequired(message="A nova senha é obrigatória."), 
        Length(min=8, message="A senha deve ter no mínimo 8 caracteres."),
        password_complexity
    ])
    password2 = PasswordField('Repita a Nova Senha', validators=[
        DataRequired(message="A confirmação de senha é obrigatória."), 
        EqualTo('password', message='As senhas devem ser iguais.') # Corrigido: 'senha' para 'senhas'
    ])
    submit = SubmitField('Redefinir Senha')

class TwoFactorForm(FlaskForm):
    code = StringField('Código de 6 dígitos', validators=[
        DataRequired(message="O código é obrigatório."), 
        Length(min=6, max=6, message="O código deve ter exatamente 6 dígitos.")
    ])
    submit = SubmitField('Verificar e Ativar')

class TwoFactorVerifyForm(FlaskForm):
    code = StringField('Código', validators=[
        DataRequired(message="O código é obrigatório."), 
        Length(min=6, max=6, message="O código deve ter exatamente 6 dígitos.")
    ])
    submit = SubmitField('Verificar Código')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Senha Atual', validators=[DataRequired(message='Você precisa informar sua senha atual')])
    new_password = PasswordField('Nova senha', validators=[
        DataRequired(message="A nova senha é obrigatória."),
        Length(min=8, message="A nova senha deve ter no mínimo 8 caracteres."),
        password_complexity
    ])
    new_password2 = PasswordField('Repita a Nova Senha', validators=[
        DataRequired(message="A confirmação de senha é obrigatória."),
        EqualTo('new_password', message='As senhas devem ser iguais.')
    ])
    submit = SubmitField('Alterar Senha')

class DeleteAccountForm(FlaskForm):
    password = PasswordField('Para continuar a exclusão, digite sua senha',
                             validators=[DataRequired(message="A senha é obrigatória para excluir a conta.")])
    submit = SubmitField('Excluir Minha Conta Permanentemente')