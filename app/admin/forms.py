from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User

class EditUserForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(message='O nome de usuário é obrigatório.')])
    email = StringField('Email', validators=[DataRequired('O e-mail é obrigatório')])
    is_admin = BooleanField('É Administrador?')
    submit = SubmitField('Salvar Alterações')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user:
                raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro.')
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user: 
                raise ValidationError('Este e-mail já está em uso por outra conta.')
            