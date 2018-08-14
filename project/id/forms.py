from flask_wtf import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from project import images
 
 
class AddIDForm(Form):
    id_number = IntegerField('ID Number', validators=[DataRequired()])
    birth_id = IntegerField('Birth ID', validators=[DataRequired()])
    profile_image = FileField('Profile Photo', validators=[FileRequired(), FileAllowed(images, 'Images only!')])