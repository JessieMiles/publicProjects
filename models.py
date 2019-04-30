from config import db, bcrypt
from sqlalchemy import func
import re
from flask import session
import os.path


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(45))
    screen_name = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "Users(id ='%s', screen_name = '%s', first_name ='%s', last_name ='%s', email='%s')" % \
               (self.id, self.screen_name, self.first_name, self.last_name, self.email)

    @classmethod
    def validate(cls, form):

        errors = []
        if len(form['first_name']) < 2:
            errors.append("First name must be greater than 2 characters")
        if len(form['last_name']) < 2:
            errors.append("Last name must be greater than 2 characters")
        if not EMAIL_REGEX.match(form['email']):
            errors.append("Email address format invalid")

        if 'user_id' not in session:
            existing_email = cls.query.filter_by(email=form['email']).first()
            if existing_email:
                errors.append("Email address already in use")

            if len(form['password']) < 4:
                errors.append("Password must be at least 4 characters long")

            if form['password'] != form['password_confirm']:
                errors.append("Password mis-match")
        return errors

    @classmethod
    def create(cls, form):
        print(f"PASS: {form['password']}")
        pw_hash = bcrypt.generate_password_hash(form['password'])
        user = cls(first_name=form['first_name'],
                   last_name=form['last_name'],
                   screen_name=form['screen_name'],
                   email=form['email'],
                   password=pw_hash
                   )
        db.session.add(user)
        db.session.commit()
        return user.id

    @classmethod
    def login_validate(cls, form):
        user = cls.query.filter_by(email=form['login_email']).first()
        if user:
            if bcrypt.check_password_hash(user.password, form['login_password']):
                return True, user.id
        return False, "Email or bad password"


class Channels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45))
    description = db.Column(db.String(45))
    channel_type_id = db.Column(db.Integer)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    creator = db.relationship("Users", foreign_keys=[created_by_id], backref="created_channels", cascade="all")
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "Channels(id ='%s', title = '%s', created_by_id = '%s', creator = '%s')" % (self.id, self.title,
                                                                                           self.created_by_id,
                                                                                           self.creator)

    @classmethod
    def add_new_channel(cls, owner_id, title, description, channel_type):
        channel = cls(title=title, created_by_id=owner_id, description=description, channel_type_id=channel_type)
        db.session.add(channel)
        db.session.commit()
        return channel.id

    @classmethod
    def get_public_channels(cls):
        return Channels.query.filter_by(channel_type_id=1).all()

    @classmethod
    def get_owned_channels(cls, user_id):
        return Channels.query.filter_by(created_by_id=user_id).all()


class Memberships(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    members = db.relationship("Users", foreign_keys=[user_id], backref="user_membership", cascade="all")
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"), nullable=False)
    channels = db.relationship("Channels", foreign_keys=[channel_id], backref="channel_members", cascade="all")
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "Memberships(id ='%s', title = '%s', created_at = '%s')" % (self.id, self.title, self.created_at)


class AccessLevels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "AccessLevels(id ='%s', name = '%s', created_at = '%s')" % (self.id, self.name, self.created_at)
