# project/recipes/views.py
 
#################
#### imports ####
#################
 
from flask import render_template, Blueprint, request, redirect, url_for, flash
from project import db
from project.models import Birth, ID, IEBC
from project.births.forms import AddBirthForm
from flask_login import login_user, current_user, login_required, logout_user

 
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')
 
################
#### config ####
################
 
births_blueprint = Blueprint('births', __name__)
 
 
################
#### routes ####
################
 

def method_is_delete(request):
    '''Workaround for a lack of delete method is the HTML spec for forms.'''
    return request.form.get('_method') == 'DELETE'


        # delete somehing




@births_blueprint.route('/births_list')
def index():
    all_births = Birth.query.all()
    return render_template('births.html', births=all_births)


@births_blueprint.route('/list_of_persons')
def list_of_persons():
    all_ids = db.session.query(Birth,ID).filter(Birth.id == ID.id).all()
    print (all_ids)
    return render_template('list_of_persons.html', ids=all_ids)


@births_blueprint.route('/mark_as_deceased/<birth_id>')
def mark_as_deceased(birth_id):
    birth = Birth.query.get_or_404(birth_id)
        #a = Birth.query.filter(Birth.deceased == False).all()
    birth.deceased = True
    db.session.commit()
    return redirect(url_for('iebc.index'))


@births_blueprint.route('/person_detail/<id_card_id>')
def person_details(id_card_id):
    all_voters = db.session.query(Birth, ID, IEBC).join(ID).join(IEBC).filter(ID.id == id_card_id).first()
    print (all_voters)
    if all_voters is not None:        
        if current_user.is_authenticated:
            return render_template('person_details.html', voters=all_voters)
        else:
            flash('Error! Incorrect permissions to access this record.', 'error')
    else:
        flash('Error! Record does not exist.', 'error')


@births_blueprint.route('/add', methods=['GET', 'POST'])    # Use of @roles_required decorator
def add_birth():
    form = AddBirthForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_birth = Birth(form.child_name.data, form.father_name.data, form.mother_name.data, form.midwife_name.data, form.birth_date.data, form.registration_date.data, form.hospital_name.data, form.birth_county.data, form.birth_constituency.data, form.birth_ward.data, False)
            db.session.add(new_birth)
            db.session.commit()
            flash('New Birth Record, {}, added!'.format(new_birth.child_name), 'success')
            return redirect(url_for('births.index'))
        else:
        	flash_errors(form)
        	flash('ERROR! Record was not added.', 'error')
 
    return render_template('add_birth.html',
                           form=form)


@births_blueprint.route('/birth/<birth_id>')
def birth_details(birth_id):
    birth = db.session.query(Birth).filter(Birth.id == birth_id).first()
    if birth is not None:        
        if current_user.username == 'Registrar':
            return render_template('birth_details.html', birth=birth)
        else:
            flash('Error! Incorrect permissions to access this record.', 'error')
    else:
        flash('Error! Record does not exist.', 'error')
    return redirect(url_for('births.index'))


@births_blueprint.route('/birth_with_ID/<birth_id>')
def birth_with_ID_details(birth_id):
    birth = db.session.query(Birth).filter(Birth.id == birth_id).first()
    if birth is not None:        
        if current_user.is_authenticated:
            return render_template('add_id_number.html', birth=birth)
        else:
            flash('Error! Incorrect permissions to access this record.', 'error')
    else:
        flash('Error! Record does not exist.', 'error')
    return redirect(url_for('births.index'))


