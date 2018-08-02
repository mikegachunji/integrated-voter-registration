# project/recipes/forms.py
 
 
from flask_wtf import Form
from wtforms import StringField, DateField
from wtforms.validators import DataRequired
 
 
class AddBirthForm(Form):
    child_name = StringField('Name of Child', validators=[DataRequired()])
    father_name = StringField('Name of Father', validators=[DataRequired()])
    mother_name = StringField('Name of Mother', validators=[DataRequired()])
    midwife_name = StringField('Name of Midwife', validators=[DataRequired()])
    birth_date = DateField('Date of Birth', format='%d/%m/%Y', validators=[DataRequired()])
    registration_date = DateField('Date of Registration', format='%d/%m/%Y', validators=[DataRequired()])
    hospital_name = StringField('Name of Hospital', validators=[DataRequired()])
    birth_county = StringField('County', validators=[DataRequired()])
    birth_constituency = StringField('Constituency', validators=[DataRequired()])
    birth_ward = StringField('Ward', validators=[DataRequired()])