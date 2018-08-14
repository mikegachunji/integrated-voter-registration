import datetime
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from project import db, app
from project.models import Birth, User, ID


# drop all of the existing database tables
db.drop_all() 
# create the database and the database table
db.create_all()

