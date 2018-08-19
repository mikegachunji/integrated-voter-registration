import string
import random
import datetime
import dateutil
from flask import render_template, Blueprint, request, redirect, url_for, flash, abort
from flask_login import login_user, current_user, login_required, logout_user
from project.id.forms import AddIDForm
from project.models import ID, Birth
from project import db, images

id_blueprint = Blueprint('id', __name__)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')

def birthday(date):
    # Get the current date
    now = 2018
    age = now - date

    return age

def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




@id_blueprint.route('/id_list')
@login_required
def index():
    all_ids = db.session.query(Birth,ID).join(ID).filter(Birth.id == ID.birth_id, Birth.has_id == True).all()
    if current_user.username == 'IDAdmin':
        return render_template('ids.html', ids=all_ids)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')


@id_blueprint.route('/qualified_id_list')
@login_required
def qualified_id_list():
    all_ids = db.session.query(Birth).filter(birthday(Birth.birth_year) >= 18, Birth.has_id == False).all()
    if current_user.username == 'IDAdmin':
        return render_template('qualified_id_list.html', ids=all_ids)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')



@id_blueprint.route('/unregistered_id_list')
@login_required
def unregistered_id_list():
    all_births = db.session.query(Birth).filter(birthday(Birth.birth_year) >= 18, Birth.has_id == False).all()
    if current_user.username == 'IDAdmin':
        return render_template('unregistered_ids.html', births=all_births)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')



@id_blueprint.route('/add_id_number/<birth_id>')
@login_required
def add_id_number(birth_id):
    all_births = Birth.query.get_or_404(birth_id)
    if current_user.username == 'IDAdmin':
        return render_template('add_id_number.html', births=all_births)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')

@id_blueprint.route('/mark_as_allocated/<birth_id>')
@login_required
def mark_as_allocated(birth_id):
    birth = Birth.query.get_or_404(birth_id)
        #a = Birth.query.filter(Birth.deceased == False).all()
    birth.has_id = True
    db.session.commit()
    return redirect(url_for('id.index'))


@id_blueprint.route('/id_allocation_detail/<id_card_id>')
@login_required
def id_allocation_details(id_card_id):
    all_voters = db.session.query(Birth, ID).join(ID).filter(ID.id == id_card_id).first()
    if all_voters is not None:        
        if current_user.is_authenticated and current_user.username == 'IDAdmin':
            return render_template('id_allocation_details.html', voters=all_voters)
        else:
            flash('Error! Incorrect permissions to access this record.', 'error')
    else:
        flash('Error! Record does not exist.', 'error')


@id_blueprint.route('/list_of_unconfirmed_persons')
@login_required
def list_of_unconfirmed_persons():
    all_ids = db.session.query(Birth,ID).filter(birthday(Birth.birth_year) >= 18, Birth.has_id == False).all()
    if current_user.username == 'IDAdmin':
        return render_template('list_of_unconfirmed_persons.html', ids=all_ids)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')



@id_blueprint.route('/add_id/<birth_id>', methods=['GET', 'POST'])
@login_required
def add_id(birth_id):
    
    id_number = id_generator()
    new_id = ID(id_number, birth_id)
    db.session.add(new_id)
    birth = Birth.query.get_or_404(birth_id)
    birth.has_id = True;
    db.session.commit()
    if current_user.username == 'IDAdmin':
        flash('New Identification Details, {}, added!'.format(id_number), 'success')
        return redirect(url_for('id.index'))
    else:
        flash_errors(form)
        flash('ERROR! Record was not added.', 'error')
 
    return render_template('add_id.html', form=form)



# @id_blueprint.route('/add_id', methods=['GET', 'POST'])
# @login_required
# def add_id():    
#     form = AddIDForm()
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             filename = images.save(request.files['profile_image'])
#             url = images.url(filename)
#             new_id = ID(form.id_number.data, form.birth_id.data, filename, url)
#             db.session.add(new_id)
#             db.session.commit()
#             flash('New Identification Details, {}, added!'.format(new_id.id_number), 'success')
#             return redirect(url_for('id.list_of_unconfirmed_persons'))
#         else:
#             flash_errors(form)
#             flash('ERROR! Record was not added.', 'error')
 
#     return render_template('add_id.html', form=form)


@id_blueprint.route('/id_detail/<id_card_id>')
def id_details(id_card_id):
    id_with_birth = db.session.query(ID, Birth).join(Birth).filter(ID.id == id_card_id).first()
    if id_with_birth is not None:        
        if current_user.is_authenticated and current_user.username == 'IDAdmin':
            return render_template('id_details.html', id_card=id_with_birth)
        else:
            flash('Error! Incorrect permissions to access this record.', 'error')
    else:
        flash('Error! Record does not exist.', 'error')


