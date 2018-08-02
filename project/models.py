from project import db
from datetime import datetime
 
 
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