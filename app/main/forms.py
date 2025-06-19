from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class LocationForm(FlaskForm):
    name = StringField('Nome do Local', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Salvar Local')