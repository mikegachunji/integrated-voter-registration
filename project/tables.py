from flask_table import Table, Col, LinkCol
 
class Results(Table):
    id = Col('Id', show=False)
    child_name = Col('Name')
    birth_county = Col('County')
    birth_year = Col('Year Of Birth')
    edit = LinkCol('Edit', 'main.edit', url_kwargs=dict(id='id'))