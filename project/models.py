from project import db, app
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

 
class Birth(db.Model):
 
    __tablename__ = "births"
    
 
    id = db.Column(db.Integer, primary_key=True)
    child_name = db.Column(db.String, nullable=False)
    father_name = db.Column(db.String, nullable=False)
    mother_name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    birth_year = db.Column(db.Integer(), nullable=False)
    birth_county = db.Column(db.String, nullable=False)
    deceased = db.Column(db.Boolean, default=False, nullable=False)
    has_id = db.Column(db.Boolean, default=False, nullable=False)
    is_voter = db.Column(db.Boolean, default=False, nullable=False)
    id_cards = db.relationship('ID', uselist=False, back_populates='births')

            
 
    def __init__(self, child_name, father_name, mother_name, gender, birth_year, birth_county, deceased, has_id, is_voter):
        self.child_name = child_name
        self.father_name = father_name
        self.mother_name = mother_name
        self.gender = gender
        self.birth_year = birth_year
        self.birth_county = birth_county
        self.deceased = False
        self.has_id = False
        self.is_voter = False

        
 
    def __repr__(self):
        return '<id: {}, name: {}, gender: {}, year_of_birth: {}, county: {}, deceased: {}, has_id: {}, is_voter: {}>'.format(self.id, self.child_name, self.gender, self.birth_year, self.birth_county, self.deceased, self.has_id, self.is_voter)

class User(db.Model):
 
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
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


class ID(db.Model):
 
    __tablename__ = "id_cards"

     
    id = db.Column(db.Integer, primary_key=True)
    id_number = db.Column(db.String, nullable=False)    
    birth_id = db.Column(db.Integer, db.ForeignKey('births.id'))
    births = db.relationship('Birth', back_populates='id_cards') 
    iebc = db.relationship('IEBC', uselist=False, back_populates='id_cards')   
    
     
    def __init__(self, id_number, birth_id):
        self.id_number = id_number
        self.birth_id = birth_id        
        
 
    def __repr__(self):
        return '<id: {}, id_number: {}, birth_id: {}>'.format(self.id, self.id_number, self.birth_id)


class IEBC(db.Model):

    __tablename__ = "iebc"

    id = db.Column(db.Integer, primary_key=True)
    id_card_id = db.Column(db.Integer, db.ForeignKey('id_cards.id')) 
    id_cards = db.relationship('ID', back_populates='iebc')

    def __init__(self, polling_station, id_card_id):
        self.polling_station = polling_station
        self.id_card_id = id_card_id

    def __repr__(self):
        return '<id: {}, polling_station: {}, id_card_id: {}>'.format(self.id, self.polling_station, self.id_card_id)

        

