from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Optional

class LocationForm(FlaskForm):
    name = StringField('Nome do Local', validators=[
        DataRequired(message="O nome do local é obrigatório."), 
        Length(min=2, max=100, message="O nome deve ter entre 2 e 100 caracteres.")
    ])
    submit_location = SubmitField('Salvar Local')

class FoodItemForm(FlaskForm):
    name = StringField('Nome do Alimento', validators=[
        DataRequired(message="O nome do alimento é obrigatório."), 
        Length(max=100, message="O nome não pode exceder 100 caracteres.")
    ])
    quantity = StringField('Quantidade (ex: 1kg, 2 unidades)', validators=[
        Optional(), 
        Length(max=50, message="A quantidade não pode exceder 50 caracteres.")
    ])
    expiry_date = DateField('Data de validade', format='%Y-%m-%d', validators=[
        DataRequired(message="A data de validade é obrigatória.")
    ])
    location = SelectField('Local de Armazenamento', coerce=int, validators=[
        DataRequired(message="Por favor, selecione um local.")
    ])
    submit_food = SubmitField('Salvar Alimento')