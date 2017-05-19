# -*- coding: utf-8 -*-
"""
    flaskbb.user.forms
    ~~~~~~~~~~~~~~~~~~

    It provides the forms that are needed for the user views.

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField,DateTimeField, TextAreaField, SelectField,
                     ValidationError, SubmitField)
from wtforms.validators import (Length, DataRequired, regexp, InputRequired, Email,
                                EqualTo, Optional, URL)
from flask_babelplus import lazy_gettext as _

from flaskbb.pet.models import Pet, Reminder
from flaskbb.extensions import db
from flaskbb.utils.fields import BirthdayField
from flaskbb.utils.helpers import check_image
from pytz import common_timezones
import arrow

def _timezones():
    return [(tz, tz) for tz in common_timezones][::-1]

appointment_times = [(t, t + " minutes") for t in ['15', '30', '45', '60']]


class NewReminderForm(FlaskForm):
    
    subject = StringField(_("Subject"), validators=[DataRequired(), Length(min=6, max=100)])

    content = TextAreaField(_("Content"), validators=[
        Optional(), Length(min=0, max=500)])

    delta = SelectField('Notification time',
                        choices=appointment_times, validators=[DataRequired()])
    time = BirthdayField(_("Time"), format="%d %m %Y %H:%M", validators=[
        DataRequired()])
    timezone = SelectField(
        'Time zone', choices=_timezones(), validators=[DataRequired()])

    submit = SubmitField(_("Save"))

    def save(self,user_id=None):
        data = self.data
        data.pop('submit', None)
        data.pop('csrf_token', None)
        remi = Reminder(**data)
        remi.time = arrow.get(remi.time, remi.timezone).to('utc').naive

        if user_id:
            return remi.save(user_id) #add
        else:
            return remi.save() #edit


USERNAME_RE = r'^[\w.+-]+$'
is_username = regexp(USERNAME_RE,
                     message=_("You can only use letters, numbers or dashes."))



class PetForm(FlaskForm):
    petname = StringField(_("Pet name"), validators=[is_username,Length(min=0, max=100)])

    breed = StringField(_("Pet Breed"), validators=[Optional(),is_username,Length(min=0, max=100)])

    birthday = BirthdayField(_("Birthday"), format="%d %m %Y", validators=[
        Optional()])

    gender = SelectField(_("Gender"), default="None", choices=[
        ("None", ""),
        ("Male", _("Male")),
        ("Female", _("Female"))])

    avatar = StringField(_("Avatar"), validators=[
        Optional()])
    
    info = TextAreaField(_("Notes"), validators=[
        Optional(), Length(min=0, max=5000)])


    submit = SubmitField(_("Save"))

    def validate_birthday(self, field):
        if field.data is None:
            return True

    def save(self,owner=None):
        data = self.data
        data.pop('submit', None)
        data.pop('csrf_token', None)
        pet = Pet(**data)

        if owner:
            return pet.save(owner) #add pet
        else:
            return pet.save() #edit pet

class AddPetForm(PetForm):
    pass


class EditPetForm(PetForm):
    def __init__(self, pet, *args, **kwargs):
        self.pet = pet
        kwargs['obj'] = self.pet
        PetForm.__init__(self, *args, **kwargs)

