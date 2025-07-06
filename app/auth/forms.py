from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
import re

def password_complexity(form, field):
    password = field.data
    if not re.search(r'[A-Z]', password):
        raise ValidationError('A senha deve conter pelo menos uma letra maiúscula.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('A senha deve conter pelo menos uma letra minúscula.')
    if not re.search(r'[0-9]', password):
        raise ValidationError('A senha deve conter pelo menos um número.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError('A senha deve contem pelo menos um caractere especial (!@#$ etc).')
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=64)])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    email2 = StringField('Repita o Email', validators=[DataRequired(), EqualTo('email', message='Os e-mails devem ser iguais.')])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=8), password_complexity])
    password2 = PasswordField(
        'Repita a Senha', validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais.')])
    accept_terms = BooleanField(
        'Eu li e aceito os Termos de Uso e a Política de Segurança.',
        validators=[DataRequired(message='Você deve aceitar os termos para se registrar.')]
    )
    submit = SubmitField('Registrar')

    # Validador para verificar se o usuário já existe
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Este nome de usuário já está em uso. Por favor, escola outro.')
        
    # Validador para verificar se o email já existe
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Este email já está em uso. Por favor, escolha outro.')
        
class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Pedir Redefinição de Senha')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nova Senha', validators=[DataRequired(), Length(min=8), password_complexity])
    password2 = PasswordField(
        'Repita a Nova Senha', validators=[DataRequired(), EqualTo('password', message='As senha devem ser iguais.')]
    )
    submit = SubmitField('Redefinir Senha')

class TwoFactorForm(FlaskForm):
    code = StringField('Código de 6 dígitos', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verificar e Ativar')

class TwoFactorVerifyForm(FlaskForm):
    code = StringField('Código', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verificar Código')