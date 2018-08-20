# project/recipes/forms.py
 
 
from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
 
 
class AddStationForm(Form):
    polling_station = StringField('Polling Station', validators=[DataRequired()])
    id_card_id = IntegerField('Identification ID', validators=[DataRequired(), NumberRange(min=1, max=10)])


 
