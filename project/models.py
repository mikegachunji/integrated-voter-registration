from project import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
 
 
class Birth(db.Model):
 
    __tablename__ = "births"
 
    id = db.Column(db.Integer, primary_key=True)
    child_name = db.Column(db.String, nullable=False)
    father_name = db.Column(db.String, nullable=False)
    mother_name = db.Column(db.String, nullable=False)
    midwife_name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.DateTime())
    registration_date = db.Column(db.DateTime(), default=datetime.utcnow)
    hospital_name = db.Column(db.String, nullable=False)
    birth_county = db.Column(db.String, nullable=False)
    birth_constituency = db.Column(db.String, nullable=False)
    birth_ward = db.Column(db.String, nullable=False)
 
    def __init__(self, child_name, father_name, mother_name, midwife_name, birth_date, registration_date, hospital_name, birth_county, birth_constituency, birth_ward):
        self.child_name = child_name
        self.father_name = father_name
        self.mother_name = mother_name
        self.midwife_name = midwife_name
        self.birth_date = birth_date
        self.registration_date = datetime.now()
        self.hospital_name = hospital_name
        self.birth_county = birth_county
        self.birth_constituency = birth_constituency
        self.birth_ward = birth_ward
 
    def __repr__(self):
        return '<title {}'.format(self.name)

class User(db.Model):
 
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)  # TEMPORARY - TO BE DELETED IN FAVOR OF HASHED PASSWORD
    authenticated = db.Column(db.Boolean, default=False)
    email_confirmation_sent_on = db.Column(db.DateTime, nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=True)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String, default='user')
 
    def __init__(self, username, email, password, email_confirmation_sent_on=None, role='user'):
        self.email = email
        self.username = username
        self.password = password
        self.authenticated = False
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = datetime.now()
        self.role = role
 
    
    @hybrid_method
    def is_correct_password(self, password):
        return self.password == password
 
    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated
 
    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True
 
    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False
 
    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)
 
    def __repr__(self):
        return '<User {0}>'.format(self.name)