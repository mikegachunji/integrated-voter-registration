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

admin_user = User(username='Registrar', email='mikegachunji@gmail.com', password='awesomeness', role='admin')
db.session.add(admin_user)


birth1 = Birth('Nahashon Njenga', 'Alfred Misheba', 'Damaris Naliaka', 'Bernice Kipkeny', '02/08/2018', '', 'Kesses Hospital', 'Uasin Gishu', 'Kesses', 'Cheboiywo')

db.session.add(birth1)

id_card1 = ID('31283382', '1', '4102c99e9411e396.png', 'http://localhost:5000/static/img/4102c99e9411e396.png')

db.session.add(id_card1)

# commit the changes
db.session.commit()