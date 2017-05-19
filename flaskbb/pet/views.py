# -*- coding: utf-8 -*-
"""
    flaskbb.user.views
    ~~~~~~~~~~~~~~~~~~

    The user view handles the user profile
    and the user settings from a signed in user.

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, flash, request,redirect, url_for,jsonify, send_from_directory
from flask_login import login_required, current_user
from flask_themes2 import get_themes_list
from flask_babelplus import gettext as _

from flaskbb.extensions import babel
from flaskbb.utils.helpers import render_template
from flaskbb.user.models import User
from flaskbb.pet.models import Pet, Reminder

from flaskbb.pet.forms import (AddPetForm,EditPetForm, NewReminderForm)


pet = Blueprint("pet", __name__)


@pet.route("/<username>/<int:pet_id>")
def profile(username,pet_id):
    pet = Pet.query.filter_by(id = pet_id).first_or_404()
    user = User.query.filter_by(username = username).first_or_404()
    return render_template("pet/profile.html", pet=pet,user=user)




@pet.route("/Add-Pet", methods=["POST", "GET"])
@login_required
def add_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        pet=form.save(owner=current_user)
        flash(_("Pet added."), "success")
        return redirect(url_for("pet.profile",username=pet.user.username,pet_id=pet.id))

    return render_template("pet/pet_form.html", form=form,
                           title=_("Add Pet"))



@pet.route("/pets/<int:pet_id>/delete", methods=["POST"])
@pet.route("/pets/delete", methods=["POST"])
@login_required
def delete_pet(pet_id=None):
    # ajax request
    if request.is_xhr:
        ids = request.get_json()["ids"]

        data = []
        for pet in Pet.query.filter(Pet.id.in_(ids)).all():
            # do not delete current user
            
            if pet.delete():
                data.append({
                    "id": pet.id,
                    "type": "delete",
                    "reverse": False,
                    "reverse_name": None,
                    "reverse_url": None
                })

        return jsonify(
            message="{} pets deleted.".format(len(data)),
            category="success",
            data=data,
            status=200
        )



    pet = Pet.query.filter_by(id=pet_id).first_or_404()
    
    pet.delete()
    flash(_("Pet deleted."), "success")
    return redirect(url_for('user.view_all_pets', username=current_user.username))

@pet.route("/pets/<int:pet_id>/edit", methods=["GET", "POST"])
def edit_pet(pet_id):
    pet = Pet.query.filter_by(id=pet_id).first_or_404()

    form = EditPetForm(pet)

    if form.validate_on_submit():
        form.populate_obj(pet)
        pet.save()

        flash(_("Pet updated."), "success")
        return redirect(url_for("pet.profile",username=pet.user.username, pet_id=pet.id))

    return render_template("pet/pet_form.html", form=form,
                           title=_("Edit Pet"))

@pet.route('/file/<path:filename>')
def img_file(filename):
    # filename = filename + ''
    print current_app.config['PET_UPLOAD_FOLDER']+filename
    return send_from_directory(current_app.config['PET_UPLOAD_FOLDER'],filename)

@pet.route('/delete-reminder',methods=['POST'])
@pet.route('/delete-reminder/<int:id>',methods=['POST'])
def delete_reminder(id):
    remi = Reminder.query.filter_by(id=id).one()
    remi.delete()

    return redirect(url_for('user.view_all_reminders',username=current_user.username))


@pet.route('/new-reminder', methods=['GET', 'POST'])
def create_reminder():
    form = NewReminderForm()

    if form.validate():
        form.save(current_user.id)

        return redirect(url_for('user.view_all_reminders',username=current_user.username))
    else:
        return render_template('pet/new_reminder.html', form=form)
