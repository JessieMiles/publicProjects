from config import db, bcrypt
from sqlalchemy import func
import re
from flask import session
import os.path


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=True)
    last_name = db.Column(db.String(45), nullable=True)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    screen_name = db.Column(db.String(45), unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='default_pic.jpg')
    articles = db.relationship('Articles', backref='author', lazy=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "Users(id ='%s', screen_name = '%s', first_name ='%s', last_name ='%s', email='%s')" % \
               (self.id, self.screen_name, self.first_name, self.last_name, self.email)

    @classmethod
    def get_articles(cls):
        return cls.articles

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


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "Articles(id ='%s', title = '%s', content = '%s', user_id = '%s')" % (self.id, self.title, self.content,
                                                                                     self.user_id)

    @classmethod
    def add_to_db(cls, form, user_id):

        article = cls(title=form['post_title'],
                      content=form['post_content'],
                      user_id=user_id)

        db.session.add(article)
        db.session.commit()
        return article.id

    @classmethod
    def get_latest_articles(cls):
        return cls.query.all()

    @classmethod
    def validate(cls, form):

        errors = []
        if len(form['post_title']) < 2:
            errors.append("The title must contain at least 2 characters")
        if len(form['post_content']) < 2:
            errors.append("The content must contain at least 2 characters")
        return errors
