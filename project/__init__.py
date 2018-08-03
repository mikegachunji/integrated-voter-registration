#################
#### imports ####
#################
 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
 
 
################
#### config ####
################
 
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

db = SQLAlchemy(app)
 
 
####################
#### blueprints ####
####################
 
from project.births.views import births_blueprint
from project.users.views import users_blueprint


 
# register the blueprints
app.register_blueprint(births_blueprint)
app.register_blueprint(users_blueprint)
