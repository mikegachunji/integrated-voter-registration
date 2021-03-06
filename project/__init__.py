#################
#### imports ####
#################
 
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_uploads import UploadSet, IMAGES, configure_uploads
 
 
################
#### config ####
################
 
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

db = SQLAlchemy(app)
mail = Mail(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

# Configure the image uploading via Flask-Uploads
images = UploadSet('images', IMAGES)
configure_uploads(app, images)
 
 
from project.models import User
 
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
 
 
####################
#### blueprints ####
####################
 
from project.births.views import births_blueprint
from project.users.views import users_blueprint
from project.id.views import id_blueprint
from project.iebc.views import iebc_blueprint
from project.main.views import main_blueprint



 
# register the blueprints
app.register_blueprint(births_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(id_blueprint)
app.register_blueprint(iebc_blueprint)
app.register_blueprint(main_blueprint)


############################
#### custom error pages ####
############################
 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
 
 
@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403
 
 
@app.errorhandler(410)
def page_not_found(e):
    return render_template('410.html'), 410
