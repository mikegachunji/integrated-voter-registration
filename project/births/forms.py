# project/recipes/forms.py
 
 
from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, validators, ValidationError, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def check_int(form, field):
    if RepresentsInt(field.data) == True:
        raise ValidationError('No numeric values are allowed')


 
 
class AddBirthForm(Form):
    child_name = StringField('Name of Child', [DataRequired(), check_int])
    father_name = StringField('Name of Father', validators=[DataRequired(), check_int])
    mother_name = StringField('Name of Mother', validators=[DataRequired(), check_int])
    gender = SelectField('Gender', choices=[('Male', 'Male'),('Female', 'Female')])
    birth_year = SelectField('Year of Birth', choices=[('1971', '1971'),('1972', '1972'),('1973', '1973'),('1974', '1974'),('1975', '1975'),('1976', '1976'),('1977', '1977'),('1978', '1978'),('1979', '1979'), ('1980', '1980'), ('1981', '1981'), ('1982', '1982'), ('1983', '1983'), ('1984', '1984'), ('1985', '1985'), ('1986', '1986'), ('1987', '1987'), ('1988', '1988'), ('1989', '1989'), ('1990', '1990'), ('1991', '1991'), ('1992', '1992'), ('1993', '1993'), ('1994', '1994'), ('1995', '1995'), ('1996', '1996'), ('1997', '1997'), ('1998', '1998'), ('1999', '1999'), ('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'), ('2004', '2004'), ('2005', '2005'), ('2006', '2006'), ('2007', '2007'), ('2008', '2008'), ('2009', '2009'), ('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018') ], validators=[DataRequired()])
    birth_county = SelectField('County', choices=[('Mombasa', 'Mombasa'),('Kwale', 'Kwale'),('Kilifi', 'Kilifi'),('Tana River', 'Tana River'),('Lamu', 'Lamu'),('Taita–Taveta', 'Taita–Taveta'),('Garissa', 'Garissa'),('Wajir', 'Wajir'),('Mandera', 'Mandera'), ('Marsabit', 'Marsabit'), ('Isiolo', 'Isiolo'), ('Meru', 'Meru'), ('Tharaka-Nithi', 'Tharaka-Nithi'), ('Embu', 'Embu'), ('Kitui', 'Kitui'), ('Machakos', 'Machakos'), ('Makueni', 'Makueni'), ('Nyandarua', 'Nyandarua'), ('Nyeri', 'Nyeri'), ('Kirinyaga', 'Kirinyaga'), ('Muranga', 'Muranga'), ('Kiambu', 'Kiambu'), ('Turkana', 'Turkana'), ('West Pokot', 'West Pokot'), ('Samburu', 'Samburu'), ('Trans-Nzoia', 'Trans-Nzoia'), ('Uasin Gishu', 'Uasin Gishu'), ('Elgeyo-Marakwet', 'Elgeyo-Marakwet'), ('Nandi', 'Nandi'), ('Baringo', 'Baringo'), ('Laikipia', 'Laikipia'), ('Nakuru', 'Nakuru'), ('Narok', 'Narok'), ('Kajiado', 'Kajiado'), ('Kericho', 'Kericho'), ('Bomet', 'Bomet'), ('Kakamega', 'Kakamega'), ('Vihiga', 'Vihiga'), ('Bungoma', 'Bungoma'), ('Busia', 'Busia'), ('Siaya', 'Siaya'), ('Kisumu', 'Kisumu'), ('Homa Bay', 'Homa Bay'), ('Migori', 'Migori'), ('Kisii', 'Kisii'), ('Nyamira', 'Nyamira'), ('Nairobi', 'Nairobi') ], validators=[DataRequired()])
    



