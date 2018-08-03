from project import db
from project.models import Birth

# drop all of the existing database tables
db.drop_all() 
 
# create the database and the database table
db.create_all()
 
# insert recipe data
birth1 = Birth('Nahashon Njenga', 'Alfred Misheba', 'Damaris Naliaka', 'Bernice Kipkeny', '02/08/2018', '', 'Kesses Hospital', 'Uasin Gishu', 'Kesses', 'Cheboiywo')

db.session.add(birth1)

# commit the changes
db.session.commit()