from flask_wtf import Form
from wtforms import StringField, SelectField



class SearchForm(Form):
    choices = [('ID Number', 'ID Number'),
               ('Name', 'Name'),
               ('County', 'County')]
    select = SelectField('Search for voters:', choices=choices)
    search = StringField('')