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
 
@iebc_blueprint.route('/voter_list')
def index():
    all_voters = db.session.query(Birth, ID, IEBC).join(ID).join(IEBC).filter(Birth.deceased == False).all()
    print (all_voters)
    if current_user.username == 'IEBCAdmin':
        return render_template('registered_voters.html', voters=all_voters)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')

@iebc_blueprint.route('/unregistered_voter_list')
def unregistered_voter_list():
    all_ids = db.session.query(Birth,ID).filter(Birth.id == ID.id).all()
    print (all_ids)
    if current_user.username == 'IEBCAdmin':
        return render_template('unregistered_voters.html', ids=all_ids)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')


@iebc_blueprint.route('/add_polling_station/<id_card_id>')
def add_polling_station(id_card_id):
    id_with_birth = db.session.query(ID, Birth).join(Birth).filter(ID.id == id_card_id).first()
    if current_user.username == 'IEBCAdmin':
        return render_template('add_polling_station.html', ids=id_with_birth)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')



@iebc_blueprint.route('/add_station', methods=['GET', 'POST'])    # Use of @roles_required decorator
def add_station():
    form = AddStationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_station = IEBC(form.polling_station.data, form.id_card_id.data)
            db.session.add(new_station)
            db.session.commit()
            flash('Polling Station Details, {}, added!'.format(new_station.polling_station), 'success')
            return redirect(url_for('iebc.index'))
        else:
        	flash_errors(form)
        	flash('ERROR! Record was not added.', 'error')
 
    return render_template('add_station.html', form=form)





@iebc_blueprint.route('/voter_detail/<voter_id>')
def voter_details(voter_id):
    all_voters = db.session.query(Birth, ID, IEBC).join(ID).join(IEBC).filter(IEBC.id == voter_id).first()
    print (all_voters)
    if all_voters is not None:        
        if current_user.is_authenticated and current_user.username == 'IEBCAdmin':
            return render_template('voter_details.html', voters=all_voters)
        else:
            flash('Error! Incorrect permissions to access this record.', 'error')
    else:
        flash('Error! Record does not exist.', 'error')





