# project/recipes/views.py
 
#################
#### imports ####
#################
 
from flask import render_template, Blueprint
from project.models import Birth
 
 
################
#### config ####
################
 
births_blueprint = Blueprint('births', __name__, template_folder='templates')
 
 
################
#### routes ####
################
 
@births_blueprint.route('/')
def index():
    all_births = Birth.query.all()
    return render_template('births.html', births=all_births)