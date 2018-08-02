# project/recipes/views.py
 
#################
#### imports ####
#################
 
from flask import render_template, Blueprint, request, redirect, url_for, flash
from project import db
from project.models import Birth
from project.births.forms import AddBirthForm

 
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
 
births_blueprint = Blueprint('births', __name__, template_folder='templates')
 
 
################
#### routes ####
################
 
@births_blueprint.route('/')
def index():
    all_births = Birth.query.all()
    return render_template('births.html', births=all_births)

@births_blueprint.route('/add', methods=['GET', 'POST'])
def add_birth():
    form = AddBirthForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_birth = Birth(form.child_name.data, form.father_name.data, form.mother_name.data, form.midwife_name.data, form.birth_date.data, form.registration_date.data, form.hospital_name.data, form.birth_county.data, form.birth_constituency.data, form.birth_ward.data)
            db.session.add(new_birth)
            db.session.commit()
            flash('New Birth Record, {}, added!'.format(new_birth.child_name), 'success')
            return redirect(url_for('births.index'))
        else:
        	flash_errors(form)
        	flash('ERROR! Record was not added.', 'error')
 
    return render_template('add_birth.html',
                           form=form)