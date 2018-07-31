#################
#### imports ####
#################
 
from flask import Flask
 
 
################
#### config ####
################
 
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')
 
 
####################
#### blueprints ####
####################
 
from project.births.views import births_blueprint
from project.deaths.views import deaths_blueprint
from project.iebc.views import iebc_blueprint
from project.id.views import id_blueprint
 
# register the blueprints
app.register_blueprint(births_blueprint)
app.register_blueprint(deaths_blueprint)
app.register_blueprint(iebc_blueprint)
app.register_blueprint(id_blueprint)