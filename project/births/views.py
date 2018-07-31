# project/recipes/views.py
 
#################
#### imports ####
#################
 
from flask import render_template, Blueprint
 
 
################
#### config ####
################
 
births_blueprint = Blueprint('births', __name__, template_folder='templates')
 
 
################
#### routes ####
################
 
@births_blueprint.route('/')
def index():
    return render_template('index.html')