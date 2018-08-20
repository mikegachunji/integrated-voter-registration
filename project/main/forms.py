from flask_wtf import Form
from wtforms import StringField, SelectField



class SearchForm(Form):
    choices = [('ID Number', 'ID Number'),
               ('Name', 'Name'),
               ('County', 'County')]
    choices2 = [('Male', 'Male'),
    			('Female', 'Female'),
               ('Less Than 30 Years', 'Less Than 30 Years'),
               ('30 Years and Above', '30 Years and Above')]
    select = SelectField('Search for voters:', choices=choices)
    select1 = SelectField('Search condition 2:', choices=choices2)
    search = StringField('')