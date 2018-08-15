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
    now = datetime.datetime.utcnow()
    now = now.date()

    # Get the difference between the current date and the birthday
    age = dateutil.relativedelta.relativedelta(now, date)
    age = age.years

    return age




@id_blueprint.route('/id_list')
@login_required
def index():
    all_ids = db.session.query(Birth,ID).filter(Birth.id == ID.id).all()
    print (all_ids)
    if current_user.username == 'IDAdmin':
        return render_template('ids.html', ids=all_ids)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')


@id_blueprint.route('/unregistered_id_list')
@login_required
def unregistered_id_list():
    all_births = Birth.query.all()
    if current_user.username == 'IDAdmin':
        return render_template('unregistered_ids.html', births=all_births)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')



@id_blueprint.route('/add_id_number/<birth_id>')
@login_required
def add_id_number(birth_id):
    all_births = Birth.query.filter(Birth.id == birth_id).first()
    if current_user.username == 'IDAdmin':
        return render_template('add_id_number.html', births=all_births)
    else:
        flash('Error! Incorrect permissions to access this record.', 'error')
        return render_template('403.html')






@id_blueprint.route('/add_id', methods=['GET', 'POST'])
@login_required
def add_id():    
    form = AddIDForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filename = images.save(request.files['profile_image'])
            url = images.url(filename)
            new_id = ID(form.id_number.data, form.birth_id.data, filename, url)
            db.session.add(new_id)
            db.session.commit()
            flash('New Identification Details, {}, added!'.format(new_id.id_number), 'success')
            return redirect(url_for('id.index', id_card_id=new_id.id))
        else:
            flash_errors(form)
            flash('ERROR! Record was not added.', 'error')
 
    return render_template('add_id.html', form=form)


@id_blueprint.route('/id_detail/<id_card_id>')
def id_details(id_card_id):
    id_with_birth = db.session.query(ID, Birth).join(Birth).filter(ID.id == id_card_id).first()
    print (id_with_birth)
    if id_with_birth is not None:        
        if current_user.is_authenticated and current_user.username == 'IDAdmin':
            return render_template('id_details.html', id_card=id_with_birth)
        else:
            flash('Error! Incorrect permissions to access this record.', 'error')
    else:
        flash('Error! Record does not exist.', 'error')


