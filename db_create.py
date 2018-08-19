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

user1 = User(username='Registrar', email='registrar@go.ke', password='simba123')
user2 = User(username='IDAdmin', email='idadmin@go.ke', password='simba123')
user3 = User(username='IEBCAdmin', email='iebc@go.ke', password='simba123')

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

db.session.commit()

