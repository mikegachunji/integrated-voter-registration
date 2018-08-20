# project/recipes/views.py
 
#################
#### imports ####
#################
 
from flask import render_template, Blueprint, request, redirect, url_for, flash
from project import db
from project.models import Birth, IEBC, ID
from project.iebc.forms import AddStationForm
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
 
iebc_blueprint = Blueprint('iebc', __name__)
 
 
################
#### routes ####
################

def birthday(date):
    # Get the current date
    now = 2018
    age = now - date

    return age


 


@iebc_blueprint.route('/voter_list')
def index():
    all_voters = db.session.query(Birth, ID).join(ID).filter(Birth.is_voter == True, Birth.deceased == False).all()
    if current_user.username == 'IEBCAdmin':
        return render_template('registered_voters.html', voters=all_voters)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')


@iebc_blueprint.route('/unregistered_voter_list')
def unregistered_voter_list():
    all_ids = db.session.query(Birth,ID).filter(Birth.id == ID.birth_id, birthday(Birth.birth_year) >= 18, Birth.has_id == True, Birth.is_voter == False).all()
    if current_user.username == 'IEBCAdmin':
        return render_template('unregistered_voters.html', ids=all_ids)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')


@iebc_blueprint.route('/list_of_unconfirmed_voters')
@login_required
def list_of_unconfirmed_voters():
    all_voters = db.session.query(Birth,ID, IEBC).join(ID).join(IEBC).filter(birthday(Birth.birth_year) >= 18, Birth.has_id == True, Birth.is_voter == False).all()
    if current_user.username == 'IEBCAdmin':
        return render_template('list_of_unconfirmed_voters.html', voters=all_voters)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')



@iebc_blueprint.route('/mark_as_voter/<birth_id>')
@login_required
def mark_as_voter(birth_id):
    birth = Birth.query.get_or_404(birth_id)
        #a = Birth.query.filter(Birth.deceased == False).all()
    birth.is_voter = True
    db.session.commit()
    return redirect(url_for('iebc.index'))



@iebc_blueprint.route('/add_polling_station/<id_card_id>')
def add_polling_station(id_card_id):
    id_with_birth = db.session.query(ID, Birth).join(Birth).filter(ID.id == id_card_id).first()
    if current_user.username == 'IEBCAdmin':
        return render_template('add_polling_station.html', ids=id_with_birth)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')



@iebc_blueprint.route('/voter_allocation_detail/<id_card_id>')
@login_required
def voter_allocation_details(id_card_id):
    all_voters = db.session.query(ID,Birth).join(Birth).filter(ID.id == id_card_id).first()
    if all_voters is not None:        
        if current_user.is_authenticated and current_user.username == 'IEBCAdmin':
            return render_template('voter_allocation_details.html', voters=all_voters)
        else:
            flash('Error! Incorrect permissions to access this record.', 'error')
    else:
        flash('Error! Record does not exist.', 'error')




@iebc_blueprint.route('/add_station', methods=['GET', 'POST'])    # Use of @roles_required decorator
def add_station():
    form = AddStationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_station = IEBC(form.polling_station.data, form.id_card_id.data)
            db.session.add(new_station)
            db.session.commit()
            flash('Polling Station Details, {}, added!'.format(new_station.polling_station), 'success')
            return redirect(url_for('iebc.list_of_unconfirmed_voters'))
        else:
        	flash_errors(form)
        	flash('ERROR! Record was not added.', 'error')
 
    return render_template('add_station.html', form=form)





@iebc_blueprint.route('/voter_detail/<voter_id>')
def voter_details(voter_id):
    all_voters = db.session.query(Birth, ID).join(ID).filter(ID.id == voter_id).first()
    if all_voters is not None:        
        if current_user.is_authenticated and current_user.username == 'IEBCAdmin':
            return render_template('voter_details.html', voters=all_voters)
        else:
            flash('Error! Incorrect permissions to access this record.', 'error')
    else:
        flash('Error! Record does not exist.', 'error')





