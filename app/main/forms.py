from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Optional

class LocationForm(FlaskForm):
    name = StringField('Nome do Local', validators=[DataRequired(), Length(min=2, max=100)])
    submit_location = SubmitField('Salvar Local')

class FoodItemForm(FlaskForm):
    name = StringField('Nome do Alimento', validators=[DataRequired(), Length(max=100)])
    quantity = StringField('Quantidade (ex: 1kg, 2 unidades)', validators=[Optional(), Length(max=50)])
    expiry_date = DateField('Data de validade', format='%Y-%m-%d', validators=[DataRequired()])
    location = SelectField('Local de Armazenamento', coerce=int, validators=[DataRequired()])
    submit_food = SubmitField('Salvar Alimento')
