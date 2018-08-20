from flask import render_template, Blueprint, request, redirect, url_for, flash, abort
from flask_login import login_user, current_user, login_required, logout_user
from project.main.forms import SearchForm
from project.births.forms import AddBirthForm
from project.models import ID, Birth
from project import db
from project.tables import Results
from project.births.forms import UpdateBirthForm



main_blueprint = Blueprint('main', __name__)

def save_changes(album, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    birth = UpdateBirthForm()
    birth.child_name = form.child_name.data
    birth.birth_county = form.birth_county.data
    birth.birth_year = form.birth_year.data     
    
 
    # commit the data to the database
    db.session.commit()




@main_blueprint.route('/', methods=['GET', 'POST'])
def search():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
 
    return render_template('search_new.html', form=search)


@main_blueprint.route('/results', methods=['GET', 'POST'])
def search_results(search):
    results = []
    search_string = search.data['search']
 
    if search_string:
        if search.data['select'] == 'ID Number':
            qry = db.session.query(Birth, ID).join(ID).filter(
                Birth.id==ID.birth_id).filter(Birth.is_voter == True).filter(
                    ID.id_number.contains(search_string))
            results = [item[0] for item in qry.all()]
        
        elif search.data['select'] == 'Name':
            qry = db.session.query(Birth).filter(Birth.is_voter == True).filter(
                Birth.child_name.contains(search_string))
            results = qry.all()
        
        elif search.data['select'] == 'County':
            qry = db.session.query(Birth).filter(Birth.is_voter == True).filter(
                Birth.birth_county.contains(search_string))
            results = qry.all()
        
        elif search.data['select'] == 'County' and search.data['select1'] == 'Male':
            qry = db.session.query(Birth).filter(Birth.is_voter == True).filter(Birth.gender == 'Male').filter(
                Birth.birth_county.contains(search_string))
            results = qry.all()

        elif search.data['select'] == 'County' and search.data['select1'] == 'Female':
            qry = db.session.query(Birth).filter(Birth.is_voter == True).filter(Birth.gender == 'Female').filter(
                Birth.birth_county.contains(search_string))
            results = qry.all()
        
        else:
            qry = db.session.query(Birth, ID).join(ID)
            results = qry.all()
    else:
        qry = db.session.query(Birth, ID).join(ID)
        results = qry.all()
 
    if not results:
        flash('No results found!')
        return redirect('/search')
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)



@main_blueprint.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db.session.query(Birth).filter(
                Birth.id==id)
    voter = qry.first()
 
    if voter:
        form = AddBirthForm(formdata=request.form, obj=voter)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(voter, form)
            flash('Record updated successfully!')
            return redirect('/')
        return render_template('edit_record.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)