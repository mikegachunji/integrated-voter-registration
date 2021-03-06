from flask_wtf import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from project import images
 
 
class AddIDForm(Form):
    id_number = IntegerField('ID Number', validators=[DataRequired(), NumberRange(min=30000000, max=40000000)])
    birth_id = IntegerField('Birth ID', validators=[DataRequired(), NumberRange(min=1, max=9)])
    profile_image = FileField('Profile Photo', validators=[FileRequired(), FileAllowed(images, 'Images only!')])