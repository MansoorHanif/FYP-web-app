# -*- coding: utf-8 -*-
"""
    flaskbb.user.models
    ~~~~~~~~~~~~~~~~~~~

    This module provides the models for the user.

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import url_for
from flask_login import UserMixin, AnonymousUserMixin

from flaskbb.extensions import db, cache
from flaskbb.exceptions import AuthenticationError
from flaskbb.utils.helpers import time_utcnow
from flaskbb.utils.database import CRUDMixin, UTCDateTime
# from flaskbb.user.models import User
import arrow

class Reminder(db.Model):
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey("users.id",
                                       use_alter=True,
                                       name="fk_reminders_users_id",
                                       ondelete="CASCADE"))
    subject = db.Column(db.String(100))
    
    content = db.Column(db.Text,nullable=False)

    delta = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    timezone = db.Column(db.String(50), nullable=False)

    def __init__(self, subject, content, delta, time, timezone):
        self.subject = subject
        self.content = content
        self.delta = delta
        self.time = time
        self.timezone = timezone
    
    # # Properties
    # @property
    # def url(self):
    #     """Returns the url for the reminder."""
    #     return url_for("pet.reminder", username=self.user.username, petname=self.pet.petname)

    
    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self, user_id=None):

        # update/edit the reminder
        if self.id:
            db.session.add(self)
            db.session.commit()
            return self

        # Adding a new pet
        if user_id:
            self.user_id = user_id

            db.session.add(self)
            db.session.commit()

           
            return self

    def delete(self):
        """Deletes a reminder and returns self."""
      
        db.session.delete(self)
        db.session.commit()
        return self

    def get_notification_time(self):
        remi_time = arrow.get(self.time)
        reminder_time = remi_time.replace(minutes=-self.delta)
        return reminder_time

class Pet(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey("users.id",
                                       use_alter=True,
                                       name="fk_pets_owners_id",
                                       ondelete="CASCADE"))

    petname = db.Column(db.String(200), nullable=False)
    birthday = db.Column(db.DateTime)
    gender = db.Column(db.String(10),default=False, nullable=False)
    breed = db.Column(db.String(50),default=False, nullable=False)
    avatar = db.Column(db.String(200))
    info = db.Column(db.Text)
   
    # Properties
    @property
    def url(self):
        """Returns the url for the pet."""
        return url_for("pet.profile", username=self.user.username, pet_id=self.id)

    # Methods
    def __init__(self, petname, birthday, gender,breed=None,avatar=None,info=None):
        """Creates a pet object with some initial values."""

        self.petname = petname
        self.birthday = birthday
        self.gender = gender
        self.breed = breed
        self.avatar=avatar
        self.info = info


    def __repr__(self):
        """Set to a unique key specific to the object in the database.
        Required for cache.memoize() to work across requests.
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)

    def save(self, user=None):
        """Saves a new pet. If no parameters are passed we assume that
        you will just update an existing pet. It returns the object after the
        operation was successful.

        :param user: The user who has added the pet
        """
        # update/edit the pet
        if self.id:
            db.session.add(self)
            db.session.commit()
            return self

        # Adding a new pet
        if user :

            self.user_id = user.id

            db.session.add(self)
            db.session.commit()

           
            return self

    def delete(self):
        """Deletes a pet and returns self."""
      
        db.session.delete(self)
        db.session.commit()
        return self
